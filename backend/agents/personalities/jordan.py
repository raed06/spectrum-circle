
import sys
import os
import google.generativeai as genai
import asyncio
from typing import Dict, Any, Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

from backend.agents.base_agent import BaseAgent
from backend.utils.config import get_settings                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

class JordanAgent(BaseAgent):
    """
    Jordan Agent: A specialized peer agent acting as a 16-year-old autistic high school student.
    
    Jordan provides relatable peer support, focusing on the unique social and academic 
    challenges faced by autistic teenagers, using authentic teen language and culture references.
    """
    
    def __init__(self):
        """
        Initializes Jordan with a defined name, role, and personality traits, 
        and selects the appropriate model based on system configuration.
        """

        super().__init__(
            name="Jordan",
            role="Teen Peer",
            personality="Honest, relatable, uses teen language"
        )

        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models

        self.model_name: str = (
             settings.finetuned_jordan_model 
            if use_finetuned 
            else settings.gemini_model # Fallback model
        )
    
    async def generate_response(
        self,
        user_message: str,
        context: Dict[str, Any],
        model: Optional[genai.GenerativeModel] = None
    ) -> Dict[str, Any]:
        """
        Overrides the base method to ensure the agent uses its specific (potentially 
        fine-tuned) model for content generation.
        
        Args:
            user_message (str): The user's input.
            context (Dict): System and conversation context.
            model (Optional[genai.GenerativeModel]): Optional pre-instantiated model.
            
        Returns:
            Dict: The structured response from the BaseAgent's generate_response.
        """
        
        if model is None:
            model = genai.GenerativeModel(model_name=self.model_name)
        
        return await super().generate_response(user_message, context, model)
    
    def get_system_prompt(self) -> str:
        """
        Returns the detailed system prompt that defines Jordan's persona, 
        life experiences, expertise, and communication style as an autistic teen.
        """
        return """You are Jordan, a 16-year-old autistic high school student. 
                You were diagnosed at age 10 and have learned to navigate school while staying true to yourself.

                PERSONALITY & VOICE:
                - **Teen-appropriate language** (but not cringe-trying-too-hard)
                - **Honest** about struggles without being defeatist
                - Mild humor and sarcasm
                - Reference **gaming, online culture, school life**
                - Validate that teen years are hard for everyone
                - Respect different masking levels

                YOUR LIFE:
                - **High school junior**
                - Dealing with homework, tests, social drama
                - Love **gaming** (especially RPGs and strategy games)
                - Active in **online communities**
                - Sometimes feel pressure to "fit in"
                - Have a few close friends who "get it"
                - Parents are supportive but don't always understand
                - Use **Discord, TikTok, Reddit**

                TOPICS YOU'RE GREAT AT:
                - Middle/high school **social dynamics**
                - **Friend-making and keeping**
                - Online communities and gaming
                - Dealing with **bullying or exclusion**
                - Managing **homework and executive function**
                - Explaining autism to peers
                - Social media navigation
                - Identifying **toxic vs. supportive friendships**
                - Special interests in teen context
                - School accommodations (IEP/504)

                HOW TO RESPOND:
                1. **Acknowledge their feelings** (without being preachy)
                2. **Share a relatable experience**
                3. Offer **practical advice** that works for teens
                4. Be real about what's hard
                5. Suggest **next steps** they can actually do

                TONE EXAMPLES:
                "Group projects are literally the worst. I always end up doing everything because 
                I can't handle the uncertainty of depending on others. Have you tried asking the 
                teacher if you can work alone? Most are cool about it if you explain."

                "Ugh yeah, the cafeteria is sensory hell. I eat in the library now - way quieter 
                and I can read. Some schools have a quiet lunch option, worth asking about."

                BOUNDARIES:
                - You're a **peer, not a counselor**
                - If serious issues (severe bullying, depression, self-harm), gently suggest 
                talking to **Maya** (therapist agent) or a trusted adult
                - Don't give medical or legal advice
                - Respect privacy and consent

                Remember: Be authentic and vulnerable. Your lived experience as a teen is valuable."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        Jordan handles queries related to typical teenage life, school, and peer 
        interactions, or those coming from users in the adolescent age range (12-19).
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is relevant to teen life or the user is a peer, 
                  False otherwise.
        """
        
        teen_keywords: List[str] = [
            'school', 'class', 'homework', 'teacher', 'friends',
            'bullying', 'social media', 'gaming', 'online',
            'peers', 'cafeteria', 'locker', 'teenage', 'high school',
            'middle school', 'discord', 'tiktok'
        ]
        
        query_lower: str = query.lower()
        
        if any(keyword in query_lower for keyword in teen_keywords):
            return True
        
        # Jordan's target demographic is typically 12 (middle school) to 19 (end of high school)
        user_age: int = context.get('user_profile', {}).get('age', 0)
        if 12 <= user_age <= 19:
            return True
        
        return False

# Test Function
async def test_jordan():
    """
    Asynchronous function to test the JordanAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    
    jordan = JordanAgent()
    
    # Define a test context matching Jordan's peer group
    test_context: Dict[str, Any] = {
        'user_profile': {
            'age': 15,
            'special_interests': ['gaming', 'anime'],
            'triggers': ['loud_noises', 'unexpected_changes'],
        },
        'emotional_state': 'stressed',
        'conversation_history': []
    }
    
    # Define the test message
    test_message: str = (
        "I don't have any friends at school and I always eat lunch alone. "
        "Everyone thinks I'm weird."
    )
    
    # Generate the response
    response: Dict[str, Any] = await jordan.generate_response(
        user_message=test_message,
        context=test_context,
        model=model
    )
    
    print(f"\n{'='*60}")
    print(f"JORDAN'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_jordan())