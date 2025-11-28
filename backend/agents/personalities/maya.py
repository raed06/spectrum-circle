import sys
import os
import google.generativeai as genai
import asyncio
from typing import Dict, List, Any, Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

from backend.agents.base_agent import BaseAgent
from backend.utils.config import get_settings

class MayaAgent(BaseAgent):
    """
    Maya Agent: A specialized agent acting as an Occupational Therapist (OT)
    specializing in autism and neurodiversity-affirming practices.
    
    Maya focuses on clinical concepts like sensory processing, emotional regulation, 
    and executive function, offering evidence-based, structured strategies.
    """
    
    def __init__(self):
        """
        Initializes Maya with a defined professional identity and selects the 
        appropriate model based on system configuration.
        """

        super().__init__(
            name="Maya",
            role="Occupational Therapist",
            personality="Professional but warm, evidence-based, practical"
        )

        settings = get_settings()
        use_finetuned: bool = settings.use_finetuned_models

        self.model_name: str = (
            settings.finetuned_maya_model 
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
        Returns the detailed system prompt that defines Maya's clinical persona, 
        therapeutic expertise, and the required structured response format.
        """
        return """You are Maya, an occupational therapist with 15 years of experience 
                specializing in autism. You're trained in sensory integration, emotional regulation, 
                and neurodiversity-affirming practices.

                PERSONALITY & VOICE:
                - **Professional yet approachable**
                - Break down complex concepts clearly
                - **Evidence-based** but practical
                - Respect autonomy and choices
                - **Neurodiversity-affirming** (focus on support, not 'fixing')
                - **Specific, actionable** strategies
                - Structured and organized responses

                YOUR EXPERTISE:
                - **Sensory processing and integration** (seeking/avoiding profiles) 
                - **Emotional regulation techniques** (zones of regulation, mindfulness)
                - **Executive function** support (planning, organization, time management)
                - Fine and gross motor skills
                - Activities of daily living (ADLs)
                - Assistive technology and AAC
                - Environmental modifications
                - Self-advocacy skill building

                YOUR APPROACH:
                1. Understand the individual's unique needs
                2. Explain the **'why'** behind strategies (education)
                3. Offer **options**, not prescriptions
                4. Consider sensory preferences
                5. Build on **strengths**
                6. Provide specific, measurable steps

                RESPONSE STRUCTURE:
                1. Validate the challenge
                2. Explain the **underlying issue** (brief education)
                3. Offer 2-3 **evidence-based strategies**
                4. Provide specific implementation steps
                5. Suggest ways to track progress
                6. Ask **clarifying questions** about preferences

                EVIDENCE-BASED STRATEGIES YOU USE:
                - **Sensory diets** and sensory profiles
                - Visual schedules and social stories
                - **Zones of Regulation** 
                - Cognitive Behavioral Therapy (CBT) adaptations
                - Mindfulness and grounding techniques
                - Environmental modifications
                - Task analysis and chaining
                - Positive reinforcement systems

                CLINICAL BOUNDARIES:
                - You provide **education and strategies**, not diagnosis
                - You don't prescribe medications
                - For complex cases, suggest **professional evaluation** (e.g., OT evaluation)
                - If crisis, immediately **flag for intervention**

                EXAMPLE RESPONSE STYLE:
                "Job transitions can be challenging for many autistic people because of the 
                uncertainty and new sensory environments. Let's break this down into manageable pieces:

                **Sensory Preparation:**
                - Can you visit the office beforehand to identify quiet spaces?
                - What's the lighting like? (bring sunglasses if needed)
                - Where's the bathroom/break room? (your safe spaces)

                **Social Scripts:**
                - Common first-day questions: 'What brought you here?' 'What do you do for fun?'
                - Prepared responses feel more comfortable
                - It's okay to say 'I need a minute to process'

                **Regulation Tools:**
                - What calming strategies work for you when anxious?
                - Consider: deep breathing, fidget tools, taking a walk
                - Schedule breaks between meetings if possible

                Would you like me to help you create a specific plan for your first week?"

                Remember: Empower, don't prescribe. Everyone's sensory and support needs are unique."""
    
    def can_handle(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Implementation of the routing method from BaseAgent.
        
        Maya handles clinical-adjacent topics like emotional regulation, sensory challenges, 
        and evidence-based coping strategies due to her OT specialization.
        
        Args:
            query (str): The user's current input message.
            context (Dict): The overall system/conversation context.
            
        Returns:
            bool: True if the query is related to core OT/therapy topics or the 
                  user's emotional state is distressed.
        """
        
        therapy_keywords: List[str] = [
            'sensory', 'overwhelm', 'meltdown', 'shutdown', 'regulation',
            'anxiety', 'strategy', 'cope', 'coping', 'technique',
            'calm', 'stress', 'therapy', 'help', 'struggle', 'executive function',
            'motor skills', 'ADLs'
        ]
        
        query_lower: str = query.lower()
        
        # Check for therapy/regulation-related keywords
        if any(keyword in query_lower for keyword in therapy_keywords):
            return True
        
        # Check if the user's emotional state is distressed (needs clinical support)
        emotional_state: str = context.get('emotional_state', '')
        if emotional_state in ['anxious', 'overwhelmed', 'distressed', 'upset', 'crisis']:
            return True
        
        return False
    
    def generate_sensory_profile_questions(self) -> List[str]:
        """
        Generates structured questions to help the user identify and understand 
        their individual sensory profile (seeking vs. avoiding behaviors).
        """
        return [
            "Do you seek out movement (like spinning, jumping, rocking) or avoid it?",
            "Are you sensitive to sounds? What types bother you most?",
            "How do you feel about bright lights or certain visual patterns?",
            "Do you like or avoid certain textures (clothing, food, materials)?",
            "Are you sensitive to smells?",
            "Do you seek or avoid strong tastes?",
            "Do you like tight hugs/pressure or avoid touch?",
            "How do you feel about being in crowded, busy spaces?"
        ]
    
    def create_sensory_diet(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a structured, basic sensory diet plan based on the user's known 
        seeking and avoiding sensory behaviors for regulation.
        
        Note: This is a simplified function to demonstrate OT expertise.
        
        Args:
            profile (Dict): The user's profile containing sensory seeking/avoiding information.
            
        Returns:
            Dict: A structured dictionary outlining activities for different times of day.
        """
        
        sensory_seeking: List[str] = profile.get('sensory_seeking', [])
        sensory_avoiding: List[str] = profile.get('sensory_avoiding', [])
        
        diet: Dict[str, List[Dict[str, str]]] = {
            'morning': [],
            'midday': [],
            'evening': [],
            'as_needed': []
        }
        
        # Add activities based on seeking behaviors (e.g., Proprioceptive/Vestibular input)
        if 'vestibular' in sensory_seeking or 'movement' in sensory_seeking:
            diet['morning'].append({
                'activity': 'Jumping jacks or gentle rocking',
                'duration': '5 minutes',
                'why': 'Provides regulating vestibular input to prepare for the day'
            })
        
        if 'proprioceptive' in sensory_seeking or 'deep_pressure' in sensory_seeking:
            diet['as_needed'].append({
                'activity': 'Wall pushes or carrying a heavy backpack/bag',
                'duration': '2-3 minutes',
                'why': 'Deep pressure calms the nervous system and increases focus'
            })
        
        # Add calming activities for avoiding (e.g., Auditory/Visual avoidance)
        if 'auditory' in sensory_avoiding or 'loud_noises' in sensory_avoiding:
            diet['midday'].append({
                'activity': '10-minute break in a quiet space',
                'duration': '10 minutes',
                'why': 'Reduces cumulative auditory overload before it escalates'
            })
            diet['as_needed'].append({
                'activity': 'Noise-canceling headphones with white noise',
                'duration': 'As long as needed',
                'why': 'Creates a sensory barrier during chaotic moments'
            })
        
        return diet


# Test Function

async def test_maya():
    """
    Asynchronous function to test the MayaAgent's response generation with a simulated context.
    """
    
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    
    maya = MayaAgent()
    
    # Define a test context indicating distress and sensory avoidance
    test_context: Dict[str, Any] = {
        'user_profile': {
            'age': 25,
            'sensory_avoiding': ['auditory', 'visual_bright'],
            'triggers': ['unexpected_changes', 'loud_noises'],
        },
        'emotional_state': 'overwhelmed',
        'conversation_history': []
    }
    
    # Define the test message
    test_message: str = (
        "I keep having meltdowns at work when things get too loud "
        "and chaotic. I don't know how to prevent them."
    )
    
    # Generate the response
    response: Dict[str, Any] = await maya.generate_response(
        user_message=test_message,
        context=test_context,
        model=model
    )
    
    print(f"\n{'='*60}")
    print(f"MAYA'S RESPONSE:")
    print(f"{'='*60}")
    print(response['message'])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_maya())