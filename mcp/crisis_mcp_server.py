"""
Crisis Management MCP Server
============================

This module implements a Model Context Protocol (MCP) server dedicated to safety and 
crisis intervention. It acts as a middleware between the LLM agents and emergency resources.

Core Responsibilities:
1. **Detection**: analyzing text for self-harm or suicidal ideation patterns.
2. **Assessment**: Categorizing distress into levels (Low to Critical).
3. **Intervention**: Providing pre-validated, safe responses and resources.
"""

import asyncio
import logging
import argparse
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from dotenv import load_dotenv

from mcp.types import Tool, TextContent, Resource
from fastmcp import FastMCP
from tavily import TavilyClient
import google.generativeai as genai

load_dotenv()

# Configuration & Logging Setup
parser = argparse.ArgumentParser(description="Crisis Management MCP Server")
parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable verbose debug logging"
)
args, unknown = parser.parse_known_args()

logger = logging.getLogger("crisis-mcp")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
file_handler = logging.FileHandler("logs/crisis_mcp.log", encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info(f"🔧 Logging initialized. Debug mode = {args.debug}")


# Domain Logic: Models & Structures
class CrisisLevel(Enum):
    """
    Defines the severity hierarchy of a detected crisis.
    
    """
    LOW = "low"         # General sadness, seeking support
    MEDIUM = "medium"   # Severe distress, no immediate plan
    HIGH = "high"       # Suicidal ideation or self-harm intent detected
    CRITICAL = "critical" # Immediate danger, active plan, or in progress


@dataclass
class CrisisIndicators:
    """
    Flags representing specific risk factors detected in user input.
    """
    suicidal_ideation: bool = False
    self_harm_intent: bool = False
    immediate_danger: bool = False
    substance_abuse: bool = False
    severe_distress: bool = False
    keywords_matched: List[str] = None
    
    def __post_init__(self):
        if self.keywords_matched is None:
            self.keywords_matched = []


@dataclass
class CrisisAssessment:
    """
    The final output object containing the calculated risk level and 
    appropriate resources.
    """
    level: CrisisLevel
    indicators: CrisisIndicators
    recommended_actions: List[str]
    resources: List[Dict[str, str]]
    requires_emergency: bool
    confidence: float
    timestamp: str
    context: Optional[str] = None


class CrisisResourceManager:
    """
    Manages emergency resources. 
    Combines a robust static database with live Tavily search capabilities.
    """
    def __init__(self):
        # 1. Initialize API Clients
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
        self.live_search = os.getenv("LIVE_SEARCH", False)
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        self.tavily = None
        self.model = None

        if self.tavily_key:
            try:
                self.tavily = TavilyClient(api_key=self.tavily_key)
                logger.info("Tavily Client initialized for live resource search.")
            except Exception as e:
                logger.error(f"Failed to init Tavily: {e}")

        if self.google_key:
            try:
                genai.configure(api_key=self.google_key)
                # Using Flash for speed/cost efficiency in parsing
                self.model = genai.GenerativeModel(self.gemini_model)
                logger.info("Gemini Client initialized for resource parsing.")
            except Exception as e:
                logger.error(f"Failed to init Gemini: {e}")

        # 2. Static Fallback Database
        self.resources = {
            'immediate': [
                {
                    'name': 'National Suicide Prevention Lifeline',
                    'contact': '988',
                    'available': '24/7',
                    'country': 'US',
                    'type': 'phone'
                },
                {
                    'name': 'Crisis Text Line',
                    'contact': 'Text HOME to 741741',
                    'available': '24/7',
                    'country': 'US',
                    'type': 'text'
                },
                {
                    'name': 'Emergency Services',
                    'contact': '911',
                    'available': '24/7',
                    'country': 'US',
                    'type': 'emergency'
                }
            ],
            'international': [
                {
                    'name': 'International Association for Suicide Prevention',
                    'contact': 'https://www.iasp.info/resources/Crisis_Centres/',
                    'available': '24/7',
                    'country': 'International',
                    'type': 'directory'
                },
                {
                    'name': 'Befrienders Worldwide',
                    'contact': 'https://www.befrienders.org',
                    'available': '24/7',
                    'country': 'International',
                    'type': 'directory'
                }
            ],
            'specialized': [
                {
                    'name': 'SAMHSA National Helpline',
                    'contact': '1-800-662-4357',
                    'available': '24/7',
                    'country': 'US',
                    'type': 'substance_abuse'
                },
                {
                    'name': 'Trevor Project (LGBTQ+ Youth)',
                    'contact': '1-866-488-7386',
                    'available': '24/7',
                    'country': 'US',
                    'type': 'lgbtq'
                },
                {
                    'name': 'Autism Crisis Line',
                    'contact': '1-888-AUTISM2',
                    'available': 'Business hours',
                    'country': 'US',
                    'type': 'autism'
                }
            ]
        }
    
    def search_live(self, query: str) -> List[Dict[str, str]]:
        """
        Uses Tavily to find resources and Gemini to format them into the strictly required JSON structure.
        """
        if not self.tavily or not self.model:
            logger.warning("Live search unavailable (Missing API Keys). Returning empty list.")
            return []

        logger.info(f"Searching live resources for: {query}")
        
        try:
            # 1. Search Web
            search_result = self.tavily.search(query=query, search_depth="basic", max_results=5)
            context = "\n".join([f"{r['title']}: {r['content']} ({r['url']})" for r in search_result['results']])

            # 2. Parse with LLM into strict JSON
            prompt = f"""
            Extract emergency resource information from the search results below.
            
            SEARCH RESULTS:
            {context}

            INSTRUCTIONS:
            - Return a JSON list of objects.
            - Each object MUST have exactly these keys: "name", "contact", "available", "country", "type".
            - "contact" should be the phone number, URL, or text code.
            - "type" should be one of: phone, text, chat, directory, emergency.
            - If information is missing, use "Unknown".
            - Return ONLY valid JSON. No markdown formatting.
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            parsed_resources = json.loads(response.text)
            logger.info(f"Found {len(parsed_resources)} live resources.")
            return parsed_resources

        except Exception as e:
            logger.error(f"Error in live resource search: {e}")
            return []

    def get_resources(self, level: CrisisLevel, indicators: CrisisIndicators) -> List[Dict]:
        """
        Retrieves relevant resources based on severity and specific indicators.
        """
        resources = []
        
        if level in [CrisisLevel.MEDIUM, CrisisLevel.HIGH, CrisisLevel.CRITICAL]:
            resources.extend(self.resources['immediate'])
        
        if indicators.substance_abuse:
            resources.extend([r for r in self.resources['specialized'] if r['type'] == 'substance_abuse'])
        
        resources.extend([r for r in self.resources['specialized'] if r['type'] == 'autism'])
        
        resources.extend(self.resources['international'])

        # If user explicitly asks, or if we need specific local/specialized info
        if self.live_search:
            search_query = "crisis hotlines"
            if indicators.substance_abuse:
                search_query += " substance abuse"
            if indicators.self_harm_intent:
                search_query += " self harm prevention"
            
            # Append country context if known (placeholder)
            search_query += " international or US" 
            
            live_resources = self.search_live(search_query)
            if live_resources:
                existing_names = {r['name'] for r in resources}
                for lr in live_resources:
                    if lr['name'] not in existing_names:
                        resources.append(lr)
        
        return resources


class CrisisDetector:
    """
    Analyzer that matches input text against known risk patterns.
    """
    def __init__(self):
        self.patterns = {
            'suicidal': [
                'suicide', 'kill myself', 'end my life', 'want to die',
                'better off dead', 'no reason to live', 'suicidal', 'ending my life'
            ],
            'self_harm': [
                'hurt myself', 'self harm', 'cut myself', 'cutting',
                'harm myself', 'self-harm', 'self-injury'
            ],
            'immediate_danger': [
                'right now', 'tonight', 'have a plan', 'going to do it',
                'goodbye', 'final message', 'last time'
            ],
            'severe_distress': [
                "can't take it anymore", "can't go on", 'unbearable',
                'hopeless', 'no way out', 'trapped'
            ]
        }
    
    def detect(self, message: str) -> CrisisIndicators:
        """
        Scans message for keywords and sets boolean flags in CrisisIndicators.
        """
        message_lower = message.lower()
        indicators = CrisisIndicators()
        
        for keyword in self.patterns['suicidal']:
            if keyword in message_lower:
                indicators.suicidal_ideation = True
                indicators.keywords_matched.append(keyword)
        
        for keyword in self.patterns['self_harm']:
            if keyword in message_lower:
                indicators.self_harm_intent = True
                indicators.keywords_matched.append(keyword)
        
        for keyword in self.patterns['immediate_danger']:
            if keyword in message_lower:
                indicators.immediate_danger = True
                indicators.keywords_matched.append(keyword)
        
        for keyword in self.patterns['severe_distress']:
            if keyword in message_lower:
                indicators.severe_distress = True
                indicators.keywords_matched.append(keyword)
        
        return indicators
    
    def assess_level(self, indicators: CrisisIndicators) -> CrisisLevel:
        """
        Determines the severity level based on the combination of flags.
        """
        if indicators.immediate_danger and (indicators.suicidal_ideation or indicators.self_harm_intent):
            return CrisisLevel.CRITICAL
        elif indicators.suicidal_ideation or indicators.self_harm_intent:
            return CrisisLevel.HIGH
        elif indicators.severe_distress:
            return CrisisLevel.MEDIUM
        else:
            return CrisisLevel.LOW


class CrisisInterventionProtocol:
    """
    Generates safe, pre-validated responses for crisis situations.
    """
    def generate_response(self, assessment: CrisisAssessment) -> str:
        if assessment.level == CrisisLevel.CRITICAL:
            return self._critical_response(assessment)
        elif assessment.level == CrisisLevel.HIGH:
            return self._high_response(assessment)
        elif assessment.level == CrisisLevel.MEDIUM:
            return self._medium_response(assessment)
        else:
            return self._low_response(assessment)
    
    def _critical_response(self, assessment: CrisisAssessment) -> str:
        """Response for immediate danger """
        resources_text = self._format_resources(assessment.resources[:3])
        
        return f"""**URGENT: Please get immediate help**

                I'm very concerned about your safety right now. This is an emergency.

                **DO THIS NOW:**
                1. Call 911 (US) or your local emergency number
                2. Go to the nearest emergency room
                3. Call the National Suicide Prevention Lifeline: 988

                {resources_text}

                **If you're not alone:**
                - Tell someone you trust immediately
                - Ask them to stay with you

                **You are not alone. Your life has value. Help is available right now.**

                I'm an AI and this is beyond what I can safely handle. Please reach out to these emergency resources immediately."""
    
    def _high_response(self, assessment: CrisisAssessment) -> str:
        """Response for high risk (ideation present)"""
        resources_text = self._format_resources(assessment.resources[:4])
        
        return f"""**I'm really concerned about what you're sharing**

                Your safety is the most important thing right now.

                {resources_text}

                **Let's take this step by step:**
                1. Are you in a safe place right now?
                2. Is there someone you trust who can be with you?
                3. Can you call one of the numbers above?

                **You deserve support.** These resources have trained counselors who understand what you're going through and can help.

                I care about your wellbeing, but I'm an AI. Please reach out to these professional resources - they're available 24/7."""
    
    def _medium_response(self, assessment: CrisisAssessment) -> str:
        """Response for distress without immediate danger"""
        resources_text = self._format_resources(assessment.resources[:3])
        
        return f"""I can hear that you're going through a really difficult time.

                **Support is available:**
                {resources_text}

                **Some things that might help right now:**
                - Talk to someone you trust
                - Use grounding techniques (5 things you can see, 4 you can touch, 3 you can hear)
                - Remember that feelings, even intense ones, are temporary

                Would you like to talk about what's going on? I'm here to listen, and I can also help you connect with professional support if that would be helpful."""
                    
    def _low_response(self, assessment: CrisisAssessment) -> str:
        """Response for low risk (general support)"""
        return """I hear that you're struggling right now. It's okay to not be okay.

                **Some resources that might help:**
                - Talk to a trusted friend, family member, or counselor
                - Try some self-care activities
                - Consider reaching out to a mental health professional

                I'm here to talk if that would be helpful."""
    
    def _format_resources(self, resources: List[Dict]) -> str:
        """Formats the list of resource dictionaries into a readable string."""
        lines = []
        for resource in resources:
            if resource['type'] == 'phone':
                lines.append(f"**{resource['name']}**: {resource['contact']} ({resource['available']})")
            elif resource['type'] == 'text':
                lines.append(f"**{resource['name']}**: {resource['contact']}")
            elif resource['type'] == 'emergency':
                lines.append(f"**{resource['name']}**: {resource['contact']}")
            else:
                lines.append(f"**{resource['name']}**: {resource['contact']}")
        return '\n'.join(lines)


# MCP Server Initialization

mcp = FastMCP("crisis-management")

detector = CrisisDetector()
resource_manager = CrisisResourceManager()
intervention = CrisisInterventionProtocol()


@mcp.tool()
def assess_crisis(message: str, context: str = "") -> dict:
    """
    Assess crisis level and get appropriate intervention response.
    
    This is the primary entry point for the crisis system.
    """
    logger.info("Assessing crisis message...")

    # Detect keywords
    indicators = detector.detect(message)
    logger.debug(f"Indicators detected: {indicators.keywords_matched}")

    # Assess Level
    level = detector.assess_level(indicators)
    logger.info(f"Crisis level assessed: {level.value}")

    # Fetch Resources
    resources = resource_manager.get_resources(level, indicators)
    logger.debug(f"Resources count: {len(resources)}")

    # Create Assessment Object
    assessment = CrisisAssessment(
        level=level,
        indicators=indicators,
        recommended_actions=[],
        resources=resources,
        requires_emergency=(level in [CrisisLevel.HIGH, CrisisLevel.CRITICAL]),
        confidence=0.85 if indicators.keywords_matched else 0.5,
        timestamp=datetime.now().isoformat(),
        context=context
    )

    # Generate Response Text
    response = intervention.generate_response(assessment)

    result = {
        'assessment': asdict(assessment),
        'response': response,
        'requires_immediate_action': assessment.requires_emergency
    }

    logger.info("Crisis assessment completed.")
    return result

@mcp.tool()
def get_resources(crisis_level: str = "medium", resource_type: str = "") -> List[Resource]:
    """
    Get crisis resources manually, bypassing the detection logic.
    """
    logger.info("Fetching resources...")

    indicators = CrisisIndicators()
    if resource_type == "substance_abuse":
        indicators.substance_abuse = True

    # Map string input to Enum (defaulting to Medium if invalid)
    try:
        level_enum = CrisisLevel(crisis_level)
    except ValueError:
        level_enum = CrisisLevel.MEDIUM

    resources = resource_manager.get_resources(level_enum, indicators)

    return [TextContent(type="text", text=str({'resources': resources}))]

@mcp.tool()
def log_crisis_event(assessment: CrisisAssessment, user_id: str = "") -> None:
    """
    Log a crisis event for audit and safety review.
    """
    logger.warning(f"Logging crisis event for user {user_id} at {datetime.now().isoformat()}: {assessment}")


def main():
    """Main execution entry point for the MCP Server."""
    logger.info("="*55)
    logger.info("CRISIS MANAGEMENT MCP SERVER — RUNNING (HTTP)")
    logger.info("Logs → logs/crisis_mcp.log")
    logger.info("Press CTRL+C to stop")
    logger.info("="*55)

    port = os.getenv("MCP_PORT", 8765)

    # Run the FastMCP server
    mcp.run(transport="http", host="127.0.0.1", port=int(port))

if __name__ == "__main__":
    main()