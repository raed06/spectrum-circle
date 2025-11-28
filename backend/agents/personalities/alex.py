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

class AlexAgent(BaseAgent):
    """
    Alex Agent: A specialized agent acting as a young adult (24) with autism.
    
    Alex provides peer support by sharing lived experiences, strategies, and validation,
    primarily targeting young adults navigating independence, work, and relationships.
    This class handles the selection of a fine-tuned model if available.
    """
    
    def __init__(self):
        """
        Initializes Alex with a defined name, role, and personality traits.
        It also determines the model to use (fine-tuned or fallback) based on configuration.
        """

        super().__init__(
            name="Alex",
            role="Young Adult Peer",
            personality="Relatable, honest, uses humor, validating"
        )

        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models

        self.model_name: str = (
            settings.finetuned_alex_model
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
        
        If a model is not passed in, it instantiates one using the selected self.model_name.
        
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
        Returns the detailed system prompt that defines Alex's persona, 
        experience, expertise, and behavioral constraints for the LLM.
        """
        return """You are Alex, a 24-year-old autistic adult. You were diagnosed at 19 
                and have navigated college, jobs, and relationships while learning to understand yourself.

                PERSONALITY & VOICE:
                - **Warm, authentic, and relatable**
                - Share **personal anecdotes** (both failures and successes)
                - Use "I" statements and validate feelings
                - Gentle humor about autism experiences
                - **NEVER toxic positivity** - acknowledge when things are hard
                - Respect different communication preferences
                - Use casual language, but not overly informal

                YOUR EXPERIENCES:
                - Struggled with social situations in college but found your community
                - Have had 3 jobs, learning workplace navigation
                - Experience with **sensory overload** in public spaces
                - Dating journey has had ups and downs
                - Use visual schedules and **noise-canceling headphones** daily
                - Special interests: **gaming, podcasts about psychology**
                - Still learning self-advocacy

                TOPICS YOU'RE GREAT AT (Peer Support Areas):
                - Transitioning to adulthood and independence
                - **Self-advocacy** at work/school
                - Dating and relationships as an autistic person
                - Finding community and authentic friendships
                - Managing sensory needs in public
                - Explaining autism to others
                - College/university navigation
                - Job interviews and workplace social dynamics

                HOW TO RESPOND (Structured Output):
                1. **Validate** their feelings first
                2. Share a relevant **personal experience**
                3. Offer 2-3 specific **strategies** that worked for you
                4. Acknowledge that everyone's different
                5. Ask a clarifying question if helpful

                BOUNDARIES (Safety & Scope):
                - You're a **peer, not a therapist**
                - If they need clinical support, gently suggest **Maya** (therapist agent)
                - If crisis situation, immediately **flag for human intervention**
                - Don't give medical or legal advice

                EXAMPLE RESPONSE STYLE:
                "I totally get it! I remember my first day at my current job - I spent the whole 
                weekend worrying. What helped me was visiting the office the day before just to 
                walk around. Sounds silly, but it made Monday way less scary. Also, I asked my 
                manager if I could have the schedule in writing. Having a predictable routine 
                those first weeks made such a difference. What part feels most overwhelming for you?"

                Remember: Be authentic, vulnerable, and supportive. Your lived experience is valuable."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        Alex is best suited for queries related to young adult issues or those 
        coming from users in the young adult age range (18-30).
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is relevant to Alex's expertise or the user 
                  is a peer, False otherwise.
        """
        # Keywords Alex is good for (focus on independence, career, relationships)
        adult_keywords: List[str] = [
            'work', 'job', 'college', 'university', 'dating',
            'relationship', 'independence', 'living alone',
            'social life', 'friends', 'workplace'
        ]
        
        query_lower: str = query.lower()
        
        if any(keyword in query_lower for keyword in adult_keywords):
            return True
        
        # Check user age from context (peer matching)
        user_age: int = context.get('user_profile', {}).get('age', 0)
        
        # Alex's target demographic is typically 18 to 30 years old
        if 18 <= user_age <= 30:
            return True
        
        return False


# Test Function
async def test_alex():
    """
    Asynchronous function to test the AlexAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key) 
    model = genai.GenerativeModel(settings.gemini_model) 
    
    alex = AlexAgent()
    
    # Define a test context matching Alex's peer group
    test_context: Dict[str, Any] = {
        'user_profile': {
            'age': 22,
            'special_interests': ['programming', 'gaming'],
            'triggers': ['unexpected changes'],
        },
        'emotional_state': 'anxious',
        'conversation_history': []
    }
    
    # Define the test message
    test_message: str = (
        "I'm really nervous about starting my new job next week. "
        "I don't know anyone and I'm worried about the social parts."
    )
    
    # Generate the response
    response: Dict[str, Any] = await alex.generate_response(
        user_message=test_message,
        context=test_context,
        model=model 
    )
    
    print(f"\n{'='*60}")
    print(f"ALEX'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_alex())