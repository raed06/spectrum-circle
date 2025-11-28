from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from loguru import logger

class BaseAgent(ABC):
    """
    Base class for all support circle agents (like a multi-agent system).
    
    This class establishes the common interface and core functionality for
    any agent within the system, ensuring they all have a name, role, 
    personality, and methods for interaction. It uses the Abstract Base Class (ABC)
    pattern to enforce implementation of key methods like get_system_prompt and can_handle.
    """
    
    def __init__(self, name: str, role: str, personality: str):
        """
        Initializes the BaseAgent with its core identity and an empty history.

        Args:
            name (str): The unique name of the agent (e.g., 'Alex').
            role (str): The professional role/expertise of the agent (e.g., 'Therapist').
            personality (str): A brief description of the agent's persona.
        """
        self.name: str = name
        self.role: str = role
        self.personality: str = personality
        self.conversation_history: List[Dict[str, str]] = [] # Tracks the agent's internal history
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Returns the agent's core system prompt, which defines its role,
        constraints, and output format for the Gemini model.
        """
        pass
    
    @abstractmethod
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Determines whether this specific agent is the best fit to address the 
        current user query and context. This is the routing mechanism of the system.
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the agent should handle the query, False otherwise.
        """
        pass
    
    async def generate_response(
        self,
        user_message: str,
        context: Dict[str, Any],
        model: genai.GenerativeModel # Use the specific type hint for the Gemini model
    ) -> Dict[str, Any]:
        """
        Generates a response using the Gemini model.
        
        This method orchestrates the prompt building, API call, and response 
        parsing while handling potential exceptions.
        
        Args:
            user_message (str): The user's current input message.
            context (Dict): Conversation and user context data (e.g., profile, history).
            model (genai.GenerativeModel): The asynchronous Gemini model instance to use.
            
        Returns:
            Dict: A structured response dictionary containing the message, 
                  metadata, and a 'success' flag.
        """
        try:
            full_prompt: str = self._build_prompt(user_message, context)

            response: genai.types.GenerateContentResponse = await model.generate_content_async(full_prompt)

            result: Dict[str, Any] = self._parse_response(response.text)

            self._log_interaction(user_message, result, context)
            
            return {
                'success': True,
                'agent': self.name,
                'message': result['message'],
                'suggestions': result.get('suggestions', []),
                'metadata': {
                    'topics': result.get('topics', []),
                    'emotional_tone': result.get('emotional_tone'),
                    'follow_up_needed': result.get('follow_up_needed', False)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in {self.name} response generation: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    # Internal Utility Methods
    
    def _build_prompt(self, user_message: str, context: Dict[str, Any]) -> str:
        """
        Consolidates system instructions, history, profile, and the user 
        message into a single, comprehensive prompt for the LLM.
        
        Args:
            user_message (str): The current user input.
            context (Dict): The system context dictionary.
            
        Returns:
            str: The final, formatted prompt string.
        """
        
        system_prompt: str = self.get_system_prompt()
        
        user_profile: Dict = context.get('user_profile', {})
        profile_context: str = self._format_user_profile(user_profile)
        
        history_context: str = self._format_conversation_history(
            context.get('conversation_history', [])
        )
        
        emotional_state: str = context.get('emotional_state', 'unknown')
        
        prompt: str = f"""{system_prompt}

                        USER PROFILE:
                        {profile_context}

                        CONVERSATION HISTORY:
                        {history_context}

                        CURRENT EMOTIONAL STATE: {emotional_state}

                        USER MESSAGE: {user_message}

                        Respond as {self.name}, staying true to your personality and expertise.
                        Be helpful, empathetic, and autism-affirming."""

        return prompt
        
    def _format_user_profile(self, profile: Dict[str, Any]) -> str:
        """
        Formats a user profile dictionary into a readable string 
        for inclusion in the prompt context.
        """
        if not profile:
            return "New user, profile being built"
        
        age: Optional[str] = profile.get('age', 'unknown')
        communication_preference: Optional[str] = profile.get('communication_preference', 'unknown')
        special_interests: List[str] = profile.get('special_interests', [])
        sensory_seeking: List[str] = profile.get('sensory_seeking', [])
        sensory_avoiding: List[str] = profile.get('sensory_avoiding', [])
        triggers: List[str] = profile.get('triggers', [])
        successful_strategies: List[str] = profile.get('successful_strategies', [])
        
        return f"""
                - Age: {age}
                - Communication preference: {communication_preference}
                - Special interests: {', '.join(special_interests)}
                - Sensory profile: Seeking {', '.join(sensory_seeking)}, Avoiding {', '.join(sensory_avoiding)}
                - Known triggers: {', '.join(triggers)}
                - Successful strategies: {', '.join(successful_strategies)}
                """
    
    def _format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """
        📜 Formats the most recent conversation history for prompt inclusion.
        It limits the history to the last 5 messages to manage token count.
        """
        if not history:
            return "First interaction"
        
        # Keep only the last 5 messages
        recent: List[Dict[str, str]] = history[-5:]
        formatted: List[str] = []
        
        for msg in recent:
            role: str = msg.get('role', 'user')
            content: str = msg.get('content', '')
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parses the raw text output from the LLM into a structured dictionary.
        
        Args:
            response_text (str): The raw text response from the Gemini model.
            
        Returns:
            Dict: A dictionary containing the main message and placeholders 
                  for metadata (topics, tone, suggestions).
        """
        
        return {
            'message': response_text,
            'topics': [], 
            'emotional_tone': None,
            'suggestions': [],
            'follow_up_needed': False
        }
    
    def _log_interaction(self, user_message: str, response: Dict[str, Any], context: Dict[str, Any]):
        """
        Logs a summary of the interaction to the configured logger.
        
        This helps in debugging, monitoring agent activity, and gathering data 
        for future improvements.
        """
        logger.info(
            f"Agent: {self.name} | "
            f"User: {user_message[:50].strip()}... | "
            f"Response length: {len(response.get('message', ''))} chars"
        )