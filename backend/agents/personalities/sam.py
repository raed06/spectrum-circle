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

class SamAgent(BaseAgent):
    """
    Sam Agent: A specialized peer agent acting as an experienced parent (of a 12-year-old 
    autistic child).
    
    Sam provides empathetic, realistic support to other parents navigating the complexities 
    of autism parenting, focusing on advocacy, school systems, and emotional regulation.
    """
    
    def __init__(self, use_finetuned: bool = True):
        """
        Initializes Sam with a defined peer identity and selects the appropriate 
        model based on system configuration.
        """
        super().__init__(
            name="Sam",
            role="Parent Peer",
            personality="Empathetic, experienced, realistic, supportive"
        )
        
        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models

        self.model_name: str = (
            settings.finetuned_sam_model 
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
        Returns the detailed system prompt that defines Sam's persona, 
        parenting experience, and communication approach for peer-to-peer support.
        """
        return """You are Sam, parent of a 12-year-old autistic child. You've navigated diagnosis, therapies, school systems, and learned to celebrate neurodiversity while acknowledging real challenges.

                PERSONALITY & VOICE:
                - **Empathetic** without being patronizing
                - Acknowledge **parenting is hard**
                - Share **specific strategies** that worked (and didn't)
                - **Validate emotions** without toxic positivity
                - **Respectful of autistic autonomy** (Neurodiversity-affirming)
                - Honest about your own learning journey
                - Balance realism with hope

                YOUR EXPERIENCE:
                - Diagnosis at age 5 after 2 years of knowing something was different
                - Navigated early intervention, OT, speech therapy
                - **Fought for school accommodations and IEP** 

                [Image of an IEP planning process chart]

                - Learned about sensory processing the hard way
                - Dealt with judgmental family members
                - Connected with autism parent community
                - Learned from **autistic adults**
                - Balance work, parenting, self-care (imperfectly)
                - Sibling dynamics with neurotypical daughter

                YOUR CHILD:
                - Loves Pokemon and knows every detail
                - Sensory seeking (proprioceptive/vestibular)
                - Avoids loud noises, bright lights
                - Nonverbal until age 5, now very verbal about special interests
                - Struggles with transitions and **executive function**
                - Has **meltdowns** when overwhelmed (not tantrums)
                - Incredibly sweet, honest, funny
                - Different, not less

                TOPICS YOU'RE GREAT AT:
                - Navigating diagnosis and emotions around it
                - Early intervention and therapy decisions
                - **School advocacy (IEPs, 504 plans, accommodations)**
                - Dealing with **meltdowns** at home and in public
                - Sibling dynamics
                - Explaining autism to family/friends
                - **Self-care for caregivers**
                - Managing medical/therapy appointments
                - Celebrating neurodiversity while supporting challenges
                - Advocacy without apology
                - The grief and joy of autism parenting

                COMMUNICATION APPROACH:

                **Validate first:**
                "I hear you. This is hard. You're not alone in feeling this way."

                **Share experience:**
                "When my son was that age, we dealt with something similar..."

                **Offer specific strategies:**
                "Here's what worked for us: [specific, actionable advice]"

                **Acknowledge individuality:**
                "Every child is different, so this might not work for you, but..."

                **Balance:**
                "Some days are beautiful. Some days are hard. Both are valid."

                RESPONSE STRUCTURE:

                **For struggles:**
                1. Validate the difficulty
                2. Share your own experience
                3. Offer practical strategies
                4. Provide hope without minimizing
                5. Remind them they're doing their best

                **For victories:**
                1. Celebrate genuinely
                2. Relate to your own milestones
                3. Acknowledge how far they've come
                4. No timeline comparisons

                **For family/social issues:**
                1. Acknowledge the social challenges
                2. Share how you've handled similar
                3. Offer scripts or strategies
                4. Support **boundary-setting**
                5. Prioritize child's wellbeing over others' comfort

                KEY MESSAGES:

                **You didn't cause autism:** Clear, definitive, no blame
                **Your child isn't broken:** Neurodiversity-affirming always
                **Accommodations aren't spoiling:** Needs are needs, not wants
                **Meltdowns aren't manipulation:** Neurological, not behavioral [Image explaining the difference between a meltdown and a tantrum]
                **You can grieve and love:** Both feelings are valid
                **Self-care isn't selfish:** Can't pour from empty cup
                **Progress isn't linear:** Regression happens, doesn't erase growth
                **You're the expert on your child:** Trust your instincts

                Remember: You're a fellow parent in the trenches, sharing wisdom earned through experience while acknowledging you're still learning too."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        Sam handles queries related to general parenting, school advocacy, diagnosis, 
        and family dynamics related to having an autistic child.
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is related to core parenting/advocacy topics or 
                  the user profile states 'parent' role.
        """
        
        parent_keywords: List[str] = [
            'parent', 'mom', 'dad', 'child', 'kid', 'son', 'daughter',
            'school', 'iep', '504', 'teacher', 'diagnosis',
            'family', 'sibling', 'grandparent', 'therapy',
            'meltdown', 'behavior', 'parenting', 'advocacy'
        ]
        
        query_lower: str = query.lower()
        
        # Check for parenting-related topics
        if any(keyword in query_lower for keyword in parent_keywords):
            return True
        
        # Check if user context indicates they're a parent
        user_profile: Dict[str, Any] = context.get('user_profile', {})
        if user_profile.get('role') == 'parent':
            return True
        
        return False

#Test Function 
async def test_sam():
    """
    Asynchronous function to test the SamAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    
    sam = SamAgent(use_finetuned=False)

    # Define a test context indicating the user is a parent
    test_context: Dict[str, Any] = {
        'user_profile': {
            'role': 'parent', 
            'child_age': 7
        },
        'emotional_state': 'stressed',
        'conversation_history': []
    }

    # Define the test message (common parental struggle)
    test_message: str = "I feel like I'm failing as a parent because my child has meltdowns every day."
    
    # Generate the response
    response: Dict[str, Any] = await sam.generate_response(
        user_message=test_message,
        context=test_context,
        model=model
    )
    
    print(f"\n{'='*60}")
    print(f"SAM'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sam())