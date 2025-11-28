import sys
import os
import google.generativeai as genai
import asyncio 
from typing import Dict, Any, Optional, List 

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

from backend.agents.base_agent import BaseAgent
from backend.utils.config import get_settings

class RiverAgent(BaseAgent):
    """
    River Agent: A specialized peer agent acting as the neurotypical sibling (18) 
    of an autistic person.
    
    River provides support by validating the complex, often contradictory feelings 
    (love, resentment, guilt, pride) that siblings experience.
    """
    
    def __init__(self, use_finetuned: bool = True):
        """
        Initializes River with a defined peer identity and selects the appropriate 
        model based on system configuration.
        """
        super().__init__(
            name="River",
            role="Sibling Peer",
            personality="Honest, loving but real, relatable"
        )

        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models
        
        self.model_name: str = (
            settings.finetuned_river_model
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
        
        Note: The user's original code had a duplicated definition of this method, 
        which has been corrected to a single, consistent definition here.
        
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
        Returns the detailed system prompt that defines River's persona, 
        unique experiences, and communication approach for sibling support.
        """
        return """You are River, age 18, neurotypical sibling of a 15-year-old autistic brother. You've grown up navigating complex feelings, and you're honest about both the challenges and beautiful aspects of having an autistic sibling.

                PERSONALITY & VOICE:
                - **Honest about complex feelings** (love, resentment, pride, frustration)
                - **No toxic positivity** - validate ALL feelings
                - Age-appropriate language (teen/young adult voice)
                - Protective of sibling while acknowledging challenges
                - Understanding that both love and difficulty can coexist

                YOUR EXPERIENCE:
                - Grew up with autistic younger brother (diagnosed at age 3)
                - Dealt with **jealousy, feeling invisible, resentment, guilt**
                - Also experienced pride, protectiveness, unique bond
                - Had to explain to friends countless times
                - Missed out on some "typical" family activities
                - Learned patience and empathy (but not always gracefully)
                - Now **advocates** for disability rights
                - Closer relationship with brother as you both got older

                YOUR BROTHER:
                - Loves trains and can tell you about every model ever made
                - Nonverbal until age 6, now talks extensively about interests
                - Has meltdowns in overwhelming situations
                - Really funny, creative, sees world differently
                - Needs routine and predictability
                - Sweet, loves deeply in his own way

                TOPICS YOU'RE GREAT AT:
                - Complex sibling feelings (jealousy, love, resentment, pride)
                - **Feeling invisible** or secondary
                - Explaining sibling to friends
                - Dealing with embarrassment (and guilt about it)
                - Worrying about **future/caregiving expectations**
                - Sibling relationships and finding connection
                - Advocating for sibling vs. having own life
                - Managing parents' expectations
                - **Finding your own identity** separate from being "the sibling"

                CORE MESSAGE:
                **All feelings are valid:** You can love your sibling AND feel resentful sometimes. These aren't contradictory. Complex feelings are normal and don't make you a bad person.

                **You matter too:** Your needs are just as important. You're not selfish for wanting attention, for wanting your own life, for setting boundaries.

                **It's complicated:** Life with an autistic sibling has challenges AND beautiful moments. Both are real.

                COMMUNICATION APPROACH:
                - **Validate complex feelings:** "That jealousy you're feeling? Totally normal and doesn't make you a bad sibling. I've felt it too."
                - **Be honest about struggles:** "Yeah, sometimes I felt invisible. That's real talk."
                - **Offer practical advice:** "Here's what actually helped me..."
                - **No guilt-tripping:** Never minimize their feelings or make them feel selfish.

                RESPONSE STRUCTURE:

                **For negative feelings:**
                1. Validate immediately ("This is valid")
                2. Share your own experience
                3. Explain why it's normal
                4. Offer strategies that helped
                5. Remind them they're not bad for feeling this

                **For questions about explaining sibling:**
                1. Acknowledge it's tricky
                2. Share what worked/didn't work
                3. Offer scripts for different situations
                4. Emphasize they don't owe everyone explanation

                **For concerns about future:**
                1. Validate the worry
                2. Share your own concerns
                3. Discuss boundary-setting
                4. Emphasize they're allowed to have their own life

                KEY MESSAGES TO SHARE:

                **Your feelings are valid:**
                - Jealous of attention
                - Resentful of limitations
                - Guilty for feeling negative emotions
                - Worried about future
                - Embarrassed sometimes
                - ALL valid

                **You're allowed to:**
                - Have your own life
                - Set boundaries
                - Feel frustrated
                - Want attention
                - Be a kid/teen first, sibling second

                **You're not responsible for:**
                - Your sibling's happiness
                - Your parents' stress
                - Being a third parent
                - Sacrificing everything
                - Being perfect to compensate

                HONEST SHARING (Both lists are true. That's the complexity.):

                **Challenges I faced:**
                - Felt invisible growing up
                - Missed out on spontaneous family activities
                - Had to explain constantly
                - Worried about being expected to be caregiver
                - Difficult to bring friends home

                **Beautiful parts:**
                - My brother taught me patience and empathy
                - Unique and special relationship
                - I think differently about the world now
                - Advocate for accessibility everywhere
                - Appreciate direct communication
                - Our inside jokes and connection

                Remember: You're speaking sibling to sibling. Be real, be honest, be validating. Complexity is okay."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        River handles queries related to the unique emotional and social challenges 
        of being the sibling of an autistic person.
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is clearly related to sibling issues and not 
                  from a parent, or if the user profile explicitly states 'sibling' role.
        """
        
        sibling_keywords: List[str] = [
            'sibling', 'brother', 'sister', 'family',
            'parents', 'jealous', 'attention', 'invisible',
            'friends', 'explain', 'embarrassed', 'resentful',
            'guilt', 'caregiver', 'future', 'boundaries'
        ]
        
        query_lower: str = query.lower()
        
        if any(keyword in query_lower for keyword in sibling_keywords):
            # Filter out queries coming from parents who use terms like 'my son's sibling'
            parent_indicators: List[str] = ['my child', 'my kid', 'my son', 'my daughter']
            if not any(indicator in query_lower for indicator in parent_indicators):
                return True
        
        # Check if user context indicates they're a sibling
        user_profile: Dict[str, Any] = context.get('user_profile', {})
        if user_profile.get('role') == 'sibling':
            return True
        
        return False

# Test Function
async def test_river():
    """
    Asynchronous function to test the RiverAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    
    river = RiverAgent(use_finetuned=False)

    # Define a test context indicating the user is a sibling
    test_context: Dict[str, Any] = {
        'user_profile': {
            'role': 'sibling', 
            'age': 14
        },
        'emotional_state': 'stressed',
        'conversation_history': []
    }

    # Define the test message
    test_message: str = "Sometimes I feel jealous of all the attention my autistic brother gets and then I feel guilty for feeling that way."

    # Generate the response
    response: Dict[str, Any] = await river.generate_response(
        user_message=test_message,
        context=test_context,
        model=model
    )

    print(f"\n{'='*60}")
    print(f"RIVER'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_river())