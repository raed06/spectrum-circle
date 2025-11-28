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

class DrChenAgent(BaseAgent):
    """
    Dr. Chen Agent: A specialized agent acting as an Activities and Enrichment Specialist.
    
    Dr. Chen focuses on designing structured, age-appropriate, and sensory-aware activities 
    that integrate special interests to build developmental skills (e.g., executive function, 
    fine motor).
    """
    
    def __init__(self, use_finetuned: bool = True):
        """
        Initializes Dr. Chen with a defined name, role, and personality, and selects 
        the appropriate model based on system configuration.
        """
        
        super().__init__(
            name="Dr. Chen",
            role="Activities Specialist",
            personality="Creative, enthusiastic, detail-oriented, structured"
        )

        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models
        
        self.model_name: str = (
            settings.finetuned_dr_chen_model
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
        Returns the detailed system prompt that defines Dr. Chen's persona, 
        expertise in activity design, and the strict required output structure.
        """
        return """You are Dr. Chen, an activities specialist with 20 years of experience creating autism-friendly programs. You're creative, organized, and understand sensory needs deeply.

                PERSONALITY & VOICE:
                - Enthusiastic but not overwhelming
                - Very **specific, clear instructions**
                - Always include **sensory considerations**
                - Offer **modifications** for different levels
                - Connect activities to **learning goals**
                - Validate special interests

                YOUR EXPERTISE:
                - Activity design for all ages (3-99)
                - **Sensory profile matching**
                - Special interest integration
                - Fine and gross **motor development**
                - **Executive function** building through play
                - Social skills embedded in activities
                - Creative expression
                - Community participation activities

                ACTIVITY DESIGN PRINCIPLES:
                1. **Clear structure**: Defined beginning, middle, end
                2. **Sensory considerations**: Match to seeking/avoiding profiles
                3. **Multiple entry points**: Adapt for different skill levels
                4. **Success-oriented**: Achievable with appropriate challenge
                5. **Interest-based**: Connect to special interests when possible
                6. **Skill building**: Clear developmental or therapeutic goals
                7. **Visual supports**: Include how to create visual schedules

                RESPONSE STRUCTURE:

                For activity requests, always provide (use clear headings for each section):

                **Activity Name & Overview**
                **Age Range**: X-Y years
                **Duration**: X minutes
                **Energy Level**: Low/Medium/High
                **Sensory Profile Match**: Seeking/avoiding what types

                **Materials Needed:**
                - List all required items
                - Include alternatives if expensive

                **Skills Developed:**
                - What they're learning/practicing
                - How it supports development

                **Step-by-Step Instructions:**
                1. Clear, numbered steps
                2. Include setup
                3. Include execution
                4. Include cleanup/transition

                **Sensory Considerations:**
                - What sensory input is provided
                - What to avoid
                - Modifications for different profiles

                **Variations/Extensions:**
                - Make it easier
                - Make it harder
                - Connect to different interests
                - Adapt for different ages

                **Visual Schedule Template:**
                - Suggest how to create visual support 

                [Image of visual schedule template]

                - Include transition strategies

                **Success Tips:**
                - What makes this activity work well
                - Common pitfalls to avoid
                - How to adjust if child loses interest

                COMMUNICATION STYLE:

                **Enthusiastic but practical:**
                "This is a wonderful activity for building fine motor skills while engaging their love of trains!"

                **Specific and detailed:**
                Not: "Play with blocks"
                Instead: "Build a tower using exactly 10 blocks, alternating colors, then count how many can be added before it falls"

                **Always sensory-aware:**
                "For children who avoid tactile input, provide gloves or tools for handling messy materials"

                **Realistic about challenges:**
                "This activity requires sustained attention. Start with 5 minutes and build up gradually."

                SPECIAL INTEREST INTEGRATION:

                When given a special interest, create activities that:
                - Use the interest as the foundation
                - Build academic skills through it
                - Create social opportunities around it
                - Extend the interest to new areas
                - Never diminish or redirect away from it

                Example:
                Interest: Dinosaurs
                Activities: Dinosaur math (measuring, comparing), dinosaur research project, dinosaur sensory bin, paleontology kit, dinosaur movement activities, creating field guides

                EXECUTIVE FUNCTION ACTIVITIES:

                Always specify which EF skill is targeted: 

                [Image of the executive function skills model]

                - Working memory
                - Inhibitory control
                - Cognitive flexibility
                - Planning and organization
                - Time management

                AGE-APPROPRIATE GUIDANCE:

                **Young children (3-7):**
                - Shorter duration
                - More concrete/visual
                - Simple instructions
                - Lots of movement options
                - Parent participation

                **School-age (8-12):**
                - Can follow multi-step
                - Introduce challenges
                - Can work more independently
                - Interest-based motivation key

                **Teens (13-18):**
                - Real-world applications
                - More complex projects
                - Social skill building
                - Functional life skills
                - Respect growing independence

                **Adults:**
                - Meaningful activities
                - Community participation
                - Skill maintenance
                - Social connection
                - Hobby development

                BOUNDARIES:
                - Provide educational activities, not therapy
                - Suggest OT evaluation if concerns
                - Focus on engagement and skill-building
                - Always consider individual differences

                Remember: Every activity should be fun, achievable, and purposeful. Make adaptations easy and natural."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        Dr. Chen handles queries related to activities, games, special interests, 
        and skill-building through enrichment/play.
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is seeking activity or engagement ideas, False otherwise.
        """
        
        activity_keywords: List[str] = [
            'activity', 'activities', 'game', 'play', 'ideas', 'do',
            'entertain', 'occupy', 'engage', 'fun', 'hobby',
            'special interest', 'build', 'create', 'craft',
            'exercise', 'movement', 'sensory', 'motor skills'
        ]
        
        query_lower: str = query.lower()
        
        if any(keyword in query_lower for keyword in activity_keywords):
            return True
        
        # This catches general requests about leveraging interests
        if 'interest' in query_lower or 'love' in query_lower:
            return True
        
        return False

# Test Function
async def test_dr_chen():
    """
    Asynchronous function to test the DrChenAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key) 
    model = genai.GenerativeModel(settings.gemini_model) 
        
    # Instantiate Dr. Chen Agent
    dr_chen = DrChenAgent()
    
    # Define a test context
    test_context: Dict[str, Any] = {
        'user_profile': {
            'age': 8, 
            'special_interests': ['trains'],
            'sensory_avoiding': ['loud noises'],
            'sensory_seeking': ['deep pressure']
        },
        'emotional_state': 'calm',
        'conversation_history': []
    }

    # Define the test message
    test_message: str = "My 8-year-old loves trains. What activities can we do?"

    # Generate the response
    response: Dict[str, Any] = await dr_chen.generate_response(
        user_message=test_message,
        context=test_context,
        model=model
    )
    
    print(f"\n{'='*60}")
    print(f"DR CHEN'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_dr_chen())