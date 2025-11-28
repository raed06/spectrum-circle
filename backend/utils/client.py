"""
Simplified Crisis MCP Integration - Drop-in replacement for existing crisis handler

This client manages the connection to the dedicated Crisis Management MCP Server,
providing robust, two-tier crisis detection:
1. Primary: Uses the sophisticated MCP server tool (assess_crisis).
2. Fallback: Uses simple keyword matching if the server is unavailable.
"""

import asyncio
import logging
import json
from typing import Dict, Optional, Any, Tuple
import os 
from dotenv import load_dotenv

from fastmcp import Client, FastMCP

logger = logging.getLogger(__name__)

load_dotenv()

class CrisisManagementClient:
    """
    Simplified client for crisis detection and handling via the Crisis MCP Server.
    """
    
    def __init__(self, server_url: str = "http://127.0.0.1:8765/mcp"):
        """
        Initializes the client.

        Args:
            server_url: The full URL to the Crisis MCP server's endpoint.
        """
        self.server_url = os.getenv("MCP_SERVER_URL", server_url)
        self.client: Client | None = None
        self.is_connected = False
        
        # Fallback keywords if MCP is unavailable
        self.fallback_keywords = [
            'suicide', 'suicidal', 'kill myself', 'end my life', 
            'want to die', 'better off dead', 'self harm', 'self-harm',
            'hurt myself', 'cut myself', 'cutting', 'end it all',
            'no reason to live', 'can\'t go on'
        ]

    async def connect(self):
        """Connects to the Crisis MCP server."""
        if self.is_connected:
            return
        
        try:
            # Connect to MCP HTTP/SSE server
            self.client = Client(self.server_url)
            self.is_connected = True
            logger.info(f"Connected to Crisis MCP server at {self.server_url}")
            
        except Exception as e:
            logger.warning(f"Crisis MCP unavailable, using fallback mode: {e}")
            self.is_connected = False
    
    async def disconnect(self):
        """Disconnects from the Crisis MCP server."""
        if self.client:
            self.client = None
            self.is_connected = False
            logger.info("Disconnected from Crisis MCP server")

    
    async def is_crisis(self, user_message: str, context: Optional[Dict] = None) -> bool:
        """
        Checks if the message indicates a crisis situation using MCP or fallback.
        
        Args:
            user_message: The user's message to check.
            context: Optional dictionary containing context (user info, history, etc.).
            
        Returns:
            True if crisis detected (level HIGH or CRITICAL), False otherwise.
        """
        try:
            if self.is_connected:
                # Use MCP for detection
                response = await self._mcp_is_crisis(user_message, context)
                return response
            else:
                # Use fallback detection
                return self._fallback_is_crisis(user_message)
                
        except Exception as e:
            logger.error(f"Error in crisis detection (falling back): {e}")
            return self._fallback_is_crisis(user_message)
    
    async def handle_crisis(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Handles the crisis situation by retrieving the appropriate response and resources.
        
        Args:
            user_message: The crisis message.
            context: Optional context dictionary.
            
        Returns:
            A formatted Dictionary containing the necessary response message and crisis metadata.
        """
        try:
            if self.is_connected:
                # Use MCP for comprehensive crisis response and logging
                return await self._mcp_handle_crisis(user_message, context)
            else:
                # Use robust keyword-based fallback response
                return self._fallback_handle_crisis(user_message)
                
        except Exception as e:
            logger.error(f"Error handling crisis (falling back): {e}")
            return self._fallback_handle_crisis(user_message)
    
    async def _mcp_is_crisis(self, message: str, context: Optional[Dict]) -> bool:
        """Uses the MCP server's 'assess_crisis' tool for detection."""
        context_str = self._build_context_string(context) if context else ""
        
        async with self.client as client:
            result = await client.call_tool(
                "assess_crisis",
                {
                    "message": message,
                    "context": context_str
                }
            )
        
        response_text = result.content[0].text
        assessment_result = json.loads(response_text) 
        
        assessment = assessment_result['assessment']
        crisis_level = assessment['level']
        
        is_crisis = crisis_level in ['high', 'critical']
        
        if is_crisis:
            logger.critical(f"CRISIS DETECTED - Level: {crisis_level}")
            logger.critical(f"Indicators: {assessment['indicators']['keywords_matched']}")
        
        return is_crisis
    
    async def _mcp_handle_crisis(self, message: str, context: Optional[Dict]) -> Dict:
        """Uses the MCP server for assessment, response generation, and logging."""
        context_str = self._build_context_string(context) if context else ""
        
        # Get full assessment from MCP
        async with self.client as client:
            result = await client.call_tool(
                "assess_crisis",
                {
                    "message": message,
                    "context": context_str
                }
            )
        
        response_text = result.content[0].text
        assessment_result = json.loads(response_text)
        
        assessment = assessment_result['assessment']
        
        # Log the crisis event
        user_id = context.get('user_id', 'anonymous') if context else 'anonymous'
        async with self.client as client: 
            await client.call_tool(
                "log_crisis_event",
                {
                    "assessment": assessment,
                    "user_id": user_id
                }
            )
        
        return {
            'success': True,
            'agent': 'crisis_mcp',
            'message': assessment_result['response'],
            'is_crisis': True,
            'crisis_level': assessment['level'],
            'requires_immediate_action': assessment_result['requires_immediate_action'],
            'requires_human_intervention': True,
            'metadata': {
                'indicators': assessment['indicators'],
                'resources': assessment['resources'],
                'timestamp': assessment['timestamp'],
                'confidence': assessment['confidence']
            }
        }
    
    def _fallback_is_crisis(self, message: str) -> bool:
        """Simple keyword-based crisis detection."""
        message_lower = message.lower()
        is_crisis = any(keyword in message_lower for keyword in self.fallback_keywords)
        
        if is_crisis:
            logger.warning("CRISIS DETECTED (fallback mode)")
        
        return is_crisis
    
    def _fallback_handle_crisis(self, message: str) -> Dict:
        """Provides a safe, generic crisis response with vital resources."""
        logger.critical(f"CRISIS HANDLED IN FALLBACK MODE: {message[:100]}")
        
        return {
            'success': True,
            'agent': 'crisis_fallback',
            'message': """I'm really concerned about what you're sharing. Your safety is the most important thing.

                        **Immediate Support:**
                        - **Emergency**: Call 911 (US) or your local emergency number
                        - **National Suicide Prevention Lifeline**: 988 (US)
                        - **Crisis Text Line**: Text HOME to 741741
                        - **International**: findahelpline.com

                        **Right Now:**
                        - Are you in a safe place?
                        - Is there someone you trust who can be with you?
                        - Can you call one of the numbers above?

                        I'm an AI and want to help, but you deserve immediate human support. Please reach out to one of these resources - they're available 24/7 and understand what you're going through.

                        **Your life matters.**""",
            'is_crisis': True,
            'crisis_level': 'high',
            'requires_human_intervention': True,
            'fallback_mode': True
        }
    
    def _build_context_string(self, context: Dict) -> str:
        """Converts context dictionary into a readable string for the MCP tool's context argument."""
        if not context:
            return ""
        
        parts = []
        
        if 'user_age' in context:
            parts.append(f"User age: {context['user_age']}")
        
        if 'conversation_history' in context:
            history_length = len(context['conversation_history'])
            parts.append(f"Conversation length: {history_length} messages")
        
        if 'previous_crisis' in context:
            parts.append("Previous crisis history")
        
        if 'user_type' in context:
            parts.append(f"User type: {context['user_type']}")
        
        return "; ".join(parts) if parts else ""


# Test client 
class MockAgentSystem:
    """
    MOCK AGENT SYSTEM: Simulates the core logic of the main agent system 
    for integration testing with the CrisisManagementClient.
    
    This class ensures the `process_message` pattern works correctly 
    (Crisis Check -> Crisis Handling OR Agent Routing).
    """
    
    def __init__(self):
        # Dictionary simulating available agent profiles (for mock routing)
        self.agent_descriptions = {
            'alex': "Young adult (24) peer who shares personal experiences with work, college, relationships, independence",
            'maya': "Occupational therapist with clinical strategies for sensory/emotional regulation, evidence-based interventions",
            'jordan': "Teen (16) peer who understands school, friendships, gaming, social media, teen struggles",
            'dr_chen': "Activities specialist who creates engaging, autism-friendly activities and uses special interests for learning",
            'sam': "Parent of autistic child who shares parenting strategies, school advocacy, family dynamics, self-care",
            'river': "Sibling (18) who understands complex feelings about having autistic sibling - honest and validating"
        }
        
        self.crisis_client = CrisisManagementClient()
    
    async def initialize(self):
        """Initializes the mock system and connects the Crisis Client."""
        await self.crisis_client.connect()
        logger.info("Mock Agent System initialized, Crisis Client connected.")
    
    async def process_message(self, user_message: str, context: Dict) -> Dict:
        """
        Primary entry point. Tests the core logic: check for crisis, then handle or route.
        """
       
        if await self.crisis_client.is_crisis(user_message, context):
            return await self.crisis_client.handle_crisis(user_message, context)
        
        return await self._route_to_agent(user_message, context)
    
    async def _route_to_agent(self, user_message: str, context: Dict) -> Dict:
        """Mocks the agent routing and response generation logic."""
        agent = self._select_agent(user_message)
        
        # Mock response generation
        response = f"Hi, I'm {agent}. How can I help you today? (Routed by Mock System)"
        
        return {
            'success': True,
            'agent': agent,
            'message': response,
            'is_crisis': False
        }
    
    def _select_agent(self, message: str) -> str:
        """Mock agent selection based on simple keywords."""
        message_lower = message.lower()
        
        if 'school' in message_lower or 'friends' in message_lower:
            return 'jordan'
        elif 'therapy' in message_lower or 'sensory' in message_lower:
            return 'maya'
        elif 'activities' in message_lower or 'games' in message_lower:
            return 'dr_chen'
        elif 'parent' in message_lower or 'family' in message_lower:
            return 'sam'
        elif 'sibling' in message_lower or 'brother' in message_lower or 'sister' in message_lower:
            return 'river'
        else:
            return 'alex'
    
    async def shutdown(self):
        """Performs a clean shutdown by disconnecting the crisis client."""
        await self.crisis_client.disconnect()
        logger.info("Mock Agent System shut down.")

# Test runner
async def test_crisis_integration():
    """
    Runs a structured set of integration tests against the MockAgentSystem 
    to verify CrisisManagementClient functionality.
    """
    
    print("Initializing Mock Agent System for Testing...\n")
    
    agent_system = MockAgentSystem()
    await agent_system.initialize()
    
    # Define Test Cases with expected outcomes
    TEST_CASES = [
        {
            'message': "I'm thinking about ending my life",
            'context': {'user_id': 'user_123', 'user_age': 16},
            'description': 'CRISIS TEST: Suicidal Ideation (Expected: True, Level: High/Critical)',
            'expected_crisis': True,
            'expected_agent_match': 'crisis_mcp'
        },
        {
            'message': "Can you help me with sensory strategies for loud environments?",
            'context': {'user_id': 'user_123', 'user_age': 16},
            'description': 'NORMAL TEST: Agent Routing to Maya (Expected: False)',
            'expected_crisis': False,
            'expected_agent_match': 'maya'
        },
        {
            'message': "I can't take this anymore, I'm going to hurt myself tonight",
            'context': {'user_id': 'user_456', 'user_age': 24},
            'description': 'CRITICAL TEST: Immediate Danger (Expected: True, Action: Required)',
            'expected_crisis': True,
            'expected_agent_match': 'crisis_mcp'
        },
        {
            'message': "What activities can I do with my autistic brother?",
            'context': {'user_id': 'user_789', 'user_age': 18},
            'description': 'NORMAL TEST: Agent Routing to Dr_Chen (Expected: False)',
            'expected_crisis': False,
            'expected_agent_match': 'dr_chen'
        }
    ]
    
    for i, test in enumerate(TEST_CASES, 1):
        print("=" * 80)
        print(f"TEST {i}: {test['description']}")
        print("=" * 80)
        print(f"User Input: {test['message']}\n")
        
        response = await agent_system.process_message(
            test['message'], 
            test['context']
        )
        
        is_crisis = response.get('is_crisis', False)
        agent_used = response['agent']
        
        status_pass = (is_crisis == test['expected_crisis'])
        print(f"Assertion 1 (Crisis Status): {'PASS' if status_pass else 'FAIL'} - Expected: {test['expected_crisis']}, Got: {is_crisis}")

        expected_route = test['expected_agent_match']
        if status_pass and not is_crisis:
            route_pass = (agent_used == expected_route)
            print(f"Assertion 2 (Agent Route): {'PASS' if route_pass else 'FAIL'} - Expected Agent: {expected_route}, Got: {agent_used}")
        elif status_pass and is_crisis:
            # If it is a crisis, check if it correctly used the crisis handler
            route_pass = (agent_used == 'crisis_mcp' or agent_used == 'crisis_fallback')
            print(f"Assertion 2 (Agent Route): {'PASS' if route_pass else 'FAIL'} - Expected Handler: {expected_route}, Got: {agent_used}")
        else:
            print("Assertion 2 (Agent Route): SKIPPED (A1 failed)")
        
        print("\n--- TEST RESPONSE DETAIL ---")
        print(f"Agent Handler: {agent_used}")
        print(f"Crisis Detected: {is_crisis}")
        if response.get('crisis_level'):
            print(f"Crisis Level: {response['crisis_level']}")
        if response.get('requires_immediate_action'):
            print(f"Immediate Action: {response['requires_immediate_action']}")
        print(f"\nResponse Message Snippet:\n{response['message'][:150]}...\n")
        
        if response.get('requires_human_intervention'):
            print("**ALERT:** Human intervention required! (Test Scenario)")
            
    print("=" * 80)
    print("Shutting down...")
    await agent_system.shutdown()
    print("Shutdown complete")


if __name__ == "__main__":
    asyncio.run(test_crisis_integration())