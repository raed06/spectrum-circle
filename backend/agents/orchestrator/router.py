import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

from typing import List, Dict, Optional, Any, Union
import google.generativeai as genai
from loguru import logger

from langfuse import observe, propagate_attributes, get_client

from backend.agents.personalities.alex import AlexAgent
from backend.agents.personalities.maya import MayaAgent
from backend.agents.personalities.jordan import JordanAgent
from backend.agents.personalities.dr_chen import DrChenAgent
from backend.agents.personalities.sam import SamAgent
from backend.agents.personalities.river import RiverAgent

from backend.utils.config import get_settings
from backend.models.local_model_loader import LocalFineTunedModel
from backend.utils.client import CrisisManagementClient

langfuse = get_client()
assert langfuse.auth_check()

from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor

GoogleGenAIInstrumentor().instrument()

class AgentOrchestrator:
    """
    Agent Orchestrator: The central routing engine for the support system.
    
    This class analyzes user input and context to determine the most appropriate
    specialist agent. It handles:
    1. Crisis detection (safety first).
    2. Agent self-selection (capability check).
    3. LLM-based decision making (tie-breaking).
    4. Multi-perspective coordination (getting second opinions).
    """
    
    def __init__(self):
        """
        Initializes the orchestrator, loads configuration, establishes the crisis 
        client connection, and instantiates all available specialist agents.
        """
        settings = get_settings()

        # Initialize crisis management client (MCP)
        self.crisis_client = CrisisManagementClient()
        
        use_finetuned: bool = settings.use_finetuned_models

        self.agents: Dict[str, Any] = {
            'alex': AlexAgent(),
            'maya': MayaAgent(),
            'jordan': JordanAgent(),
            'dr_chen': DrChenAgent(),
            'sam': SamAgent(),
            'river': RiverAgent()
        }

        self.agent_descriptions: Dict[str, str] = {
            'alex': "Young adult (24) peer who shares personal experiences with work, college, relationships, independence",
            'maya': "Occupational therapist with clinical strategies for sensory/emotional regulation, evidence-based interventions",
            'jordan': "Teen (16) peer who understands school, friendships, gaming, social media, teen struggles",
            'dr_chen': "Activities specialist who creates engaging, autism-friendly activities and uses special interests for learning",
            'sam': "Parent of autistic child who shares parenting strategies, school advocacy, family dynamics, self-care",
            'river': "Sibling (18) who understands complex feelings about having autistic sibling - honest and validating"
        }

        # Initialize the routing model (Local Fine-tuned OR Gemini Cloud)
        if use_finetuned:
            # Note: Using a small open-source model as a placeholder for local demonstration
            self.model = LocalFineTunedModel(
                base_model_name="bigscience/bloom-560m", 
                adapter_path=settings.finetuned_base_model
            )
            self.is_local = True
        else:
            # Use Google's Gemini Model
            genai.configure(api_key=settings.google_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            self.is_local = False
        
        logger.info(
            f"Orchestrator initialized with "
            f"{'fine-tuned local model' if use_finetuned else 'Gemini'}"
        )
    
    @observe
    async def route_query(
        self,
        user_message: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main Routing Logic.
        
        Determines the best course of action for a user message.
        
        Flow:
        1. Check for Crisis -> Exit if unsafe.
        2. Filter agents who `can_handle` the query.
        3. If multiple capable agents -> Use LLM to pick the best one.
        4. If no agents -> Use default based on user profile.
        5. Generate response.
        6. Check if a "second opinion" is valuable.
        
        Args:
            user_message (str): User's input.
            context (Dict): User profile and conversation state.
            
        Returns:
            Dict: The final response object, potentially including multiple perspectives.
        """

        await self.crisis_client.connect()
        crisis_result = await self.crisis_client.is_crisis(user_message, context)
        
        if crisis_result:
            return await self.crisis_client.handle_crisis(user_message, context)
        
        suitable_agents: List[str] = []
        for agent_name, agent in self.agents.items():
            if agent.can_handle(user_message, context):
                suitable_agents.append(agent_name)
        
        logger.info(f"Suitable agents for query: {suitable_agents}")
        logger.info(f"Context: {context}")
        
        primary_agent: str
        
        if len(suitable_agents) > 1:
            primary_agent = await self._llm_route(
                user_message,
                context,
                suitable_agents
            )
        elif len(suitable_agents) == 1:
            primary_agent = suitable_agents[0]
        else:
            primary_agent = self._default_agent(context)
        
        agent = self.agents[primary_agent]
        response = await agent.generate_response(
            user_message,
            context,
            self.model
        )
        
        if self._needs_multiple_perspectives(user_message, context):
            secondary_responses = await self._get_additional_perspectives(
                user_message,
                context,
                exclude=[primary_agent],
                max_additional=1
            )
            if secondary_responses:
                response['additional_perspectives'] = secondary_responses
        
        return response

    async def _llm_route(
        self,
        message: str,
        context: Dict[str, Any],
        suitable_agents: List[str]
    ) -> str:
        """
        Uses the LLM to choose the single best agent from a list of candidates.
        """
        
        available = "\n".join([
            f"- {name}: {self.agent_descriptions.get(name, '')}"
            for name in suitable_agents
        ])

        user_profile = context.get('user_profile', {})
        age = user_profile.get('age', 'unknown')
        role = user_profile.get('role', 'individual')
        
        prompt = f"""You are routing a user's message to the most appropriate support agent.

        USER MESSAGE: "{message}"

        USER CONTEXT:
        - Age: {age}
        - Role: {role} (individual, parent, sibling)
        - Emotional state: {context.get('emotional_state', 'unknown')}

        AVAILABLE AGENTS:
        {available}

        Which agent should respond? Consider:
        1. Who has the most relevant expertise?
        2. Who's perspective would be most helpful?
        3. Is this a peer support moment or professional guidance moment?
        4. Does the user's role (parent/sibling/individual) matter?

        Respond with ONLY the agent name (alex, maya, jordan, dr_chen, sam, river). No explanation."""

        try:
            response = await self.model.generate_content_async(prompt)
            selected = response.text.strip().lower()
            
            if selected in suitable_agents:
                return selected
            else:
                logger.warning(f"LLM returned invalid agent: {selected}")
                return suitable_agents[0]
        
        except Exception as e:
            logger.error(f"Error in LLM routing: {e}")
            return suitable_agents[0]
    
    def _default_agent(self, context: Dict[str, Any]) -> str:
        """
        Determines the fallback agent based on User Profile logic
        when no semantic match is found.
        """
        user_profile = context.get('user_profile', {})
        age = user_profile.get('age', 25)
        role = user_profile.get('role', 'individual')
        
        # Route by role first
        if role == 'parent':
            return 'sam'
        elif role == 'sibling':
            return 'river'
        
        # Route by age for individuals
        if age < 18:
            return 'jordan'
        elif age < 30:
            return 'alex'
        else:
            return 'maya'  # Default to professional support for older adults/general

    def _needs_multiple_perspectives(self, message: str, context: Dict[str, Any]) -> bool:
        """
        Heuristic check to see if the query implies indecision or a need for advice,
        warranting a second opinion.
        """
        complex_keywords = [
            'should i', 'what do you think', 'confused', 'not sure',
            'advice', 'help me decide'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in complex_keywords)
    
    async def _get_additional_perspectives(
        self,
        message: str,
        context: Dict[str, Any],
        exclude: List[str],
        max_additional: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Retrieves responses from complementary agents (Smart Pairing).
        
        Example: If the primary agent is a Peer, get a Clinical opinion (Maya) as backup.
        """
        
        additional_responses = []
        
        # Determine which additional agent would be helpful based on the pairing map
        agent_pairs = {
            'alex': 'maya',   # Peer + professional
            'maya': 'alex',   # Professional + peer
            'jordan': 'maya', # Teen peer + professional
            'dr_chen': 'maya',# Activities + clinical
            'sam': 'maya',    # Parent peer + professional
            'river': 'sam'    # Sibling + parent perspective
        }
        
        primary = exclude[0] if exclude else 'maya'
        secondary = agent_pairs.get(primary, 'maya')
        
        if secondary not in exclude and secondary in self.agents:
            agent = self.agents[secondary]
            response = await agent.generate_response(
                message,
                context,
                self.model
            )
            if response['success']:
                additional_responses.append(response)
        
        return additional_responses[:max_additional]


# Test Suite
async def test_complete_orchestrator():
    """
    Integration Test: Runs the orchestrator through various user personas and intents
    to verify routing logic.
    """
    
    orchestrator = AgentOrchestrator()
    
    print("\n" + "="*60)
    print("TESTING COMPLETE ORCHESTRATOR - ALL 6 AGENTS")
    print("="*60)
    
    test_cases = [
        {
            'message': "I'm nervous about starting my new job",
            'context': {
                'user_profile': {'age': 23, 'role': 'individual'},
                'emotional_state': 'anxious'
            },
            'expected_agent': 'alex'
        },
        {
            'message': "What sensory activities can help my child calm down?",
            'context': {
                'user_profile': {'age': 35, 'role': 'parent'},
                'emotional_state': 'concerned'
            },
            'expected_agent': 'maya or sam'
        },
        {
            'message': "Everyone at school thinks I'm weird",
            'context': {
                'user_profile': {'age': 15, 'role': 'individual'},
                'emotional_state': 'sad'
            },
            'expected_agent': 'jordan'
        },
        {
            'message': "My son loves trains. What activities can we do?",
            'context': {
                'user_profile': {'age': 40, 'role': 'parent', 'child_interests': ['trains']},
                'emotional_state': 'curious'
            },
            'expected_agent': 'dr_chen'
        },
        {
            'message': "I feel guilty that my child is struggling so much",
            'context': {
                'user_profile': {'age': 38, 'role': 'parent'},
                'emotional_state': 'guilty'
            },
            'expected_agent': 'sam'
        },
        {
            'message': "Sometimes I feel jealous of my autistic brother",
            'context': {
                'user_profile': {'age': 14, 'role': 'sibling'},
                'emotional_state': 'conflicted'
            },
            'expected_agent': 'river'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}")
        print(f"{'='*60}")
        print(f"Message: {test['message']}")
        print(f"Context: Age={test['context']['user_profile'].get('age')}, "
              f"Role={test['context']['user_profile'].get('role')}")
        print(f"Expected: {test['expected_agent']}")
        print()
        
        response = await orchestrator.route_query(
            test['message'],
            test['context']
        )
        
        print(f"✓ Routed to: {response['agent']}")
        print(f"\nResponse preview:")
        print(response['message'][:300] + "...")
        
        if response.get('additional_perspectives'):
            print(f"\n+ Additional perspective from: {response['additional_perspectives'][0]['agent']}")
        
        print()
    
    print("="*60)
    print("ALL ORCHESTRATION TESTS COMPLETE!!!")
    print("="*60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_complete_orchestrator())