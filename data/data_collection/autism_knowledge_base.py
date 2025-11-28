"""
Autism Knowledge Base Data Generation

This module generates a comprehensive, core dataset for the foundational 
knowledge fine-tuning of the AI model. It includes data across six critical 
domains of the autistic experience, ensuring the model's responses are accurate, 
empathetic, and neurodiversity-affirming.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

from data.data_collection.data_collector import FinetuningDataCollector

def create_sensory_processing_examples(collector):
    """Examples about sensory processing"""
    
    examples = [
        {
            'input': "What does sensory overload feel like?",
            'output': """Sensory overload varies for each autistic person, but common experiences include:

        **Physical sensations:**
        - Feeling like your skin is "crawling" or burning
        - Headaches or feeling pressure in your head
        - Increased heart rate and difficulty breathing
        - Physical exhaustion or feeling "drained"
        - Need to escape or shut down

        **Cognitive effects:**
        - Difficulty processing information or following conversation
        - Losing ability to speak (going nonverbal)
        - Difficulty making decisions
        - Mental fog or confusion
        - Executive function challenges increase

        **Emotional responses:**
        - Increased anxiety or panic
        - Irritability or emotional dysregulation
        - Feeling overwhelmed or out of control
        - Desire to flee or hide

        **Common triggers:**
        - Fluorescent lighting or bright lights
        - Background noise (especially unpredictable sounds)
        - Strong smells (perfumes, cleaners, food)
        - Crowded spaces with multiple inputs
        - Unexpected touch or physical contact
        - Multiple sensory inputs simultaneously

        **Important**: Overload isn't about "being sensitive" - it's about nervous system differences in processing sensory information. Prevention through accommodations is more effective than trying to "push through" overload.""",
            'category': 'sensory_processing'
        },
        {
            'input': "My child seeks sensory input constantly - spinning, crashing, chewing. What does this mean?",
            'output': """Sensory seeking behavior means your child's nervous system needs more intense input to reach optimal regulation. This is completely valid and common in autism.

            **Why it happens:**
            - Proprioceptive system (body awareness) needs more input
            - Vestibular system (movement/balance) is under-responsive
            - Oral motor seeking for regulation
            - Not getting enough sensory input in daily activities

            **How to support sensory seeking:**

            **Proprioceptive activities (deep pressure/heavy work):**
            - Pushing/pulling heavy objects (wagon, laundry basket)
            - Wall pushes, chair push-ups
            - Weighted blanket or compression vest
            - Carrying groceries, moving furniture
            - Climbing, hanging from bars

            **Vestibular activities (movement):**
            - Swinging (different speeds and directions)
            - Spinning in office chair (with supervision)
            - Trampoline with clear rules
            - Rocking chair or therapy ball
            - Rolling down hills, somersaults

            **Oral motor seeking:**
            - Chewy jewelry or toys
            - Crunchy foods (carrots, apples, pretzels)
            - Drinking through straw (thicker liquids)
            - Sugar-free gum (if age-appropriate)
            - Vibrating oral motor tools

            **Creating a sensory diet:**
            - Schedule sensory activities throughout day
            - BEFORE challenging tasks (homework, transitions)
            - Provide socially appropriate alternatives
            - Teach child to recognize when they need input

            **Important**: Sensory seeking is not "bad behavior" - it's the nervous system self-regulating. Providing appropriate outlets prevents unsafe seeking.""",
            'category': 'sensory_processing'
        },
        {
            'input': "How do I help someone during sensory overload?",
            'output': """During sensory overload, the person needs immediate support to reduce input and regulate:

            **Immediate steps:**

            1. **Reduce sensory input NOW:**
            - Move to quiet, dim space if possible
            - Turn off/remove noise sources
            - Remove visual clutter from view
            - Minimize talking (they may not process speech)
            - No physical touch unless they request it

            2. **Provide regulation tools:**
            - Noise-canceling headphones
            - Sunglasses or eye mask
            - Weighted blanket or deep pressure
            - Familiar comfort item
            - Cold water to drink
            - Fidget or stim toy

            3. **Communication adaptations:**
            - Use simple, short phrases or written words
            - Offer yes/no questions (thumbs up/down)
            - Respect if they can't/won't respond
            - Don't require eye contact
            - Give processing time

            4. **Create safety and predictability:**
            - Stay calm yourself
            - Explain what will happen next
            - Give timeline ("5 more minutes, then we leave")
            - Protect from well-meaning but overwhelming "help"
            - Don't force social interaction

            **After the immediate crisis:**
            - Allow recovery time (often need sleep/quiet)
            - Don't debrief immediately
            - Later, identify triggers together
            - Problem-solve prevention strategies
            - Update sensory accommodation plan

            **What NOT to do:**
            - Tell them to "calm down" or "it's not that bad"
            - Force them to continue the activity
            - Touch them without permission
            - Expect logical conversation
            - Punish meltdown behavior
            - Crowd them with multiple people

            **Prevention is key:** Work together when calm to identify early warning signs and create prevention plan.""",
            'category': 'sensory_processing'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


def create_social_communication_examples(collector):
    """Examples about social communication"""
    
    examples = [
        {
            'input': "Why don't autistic people make eye contact?",
            'output': """Eye contact can be uncomfortable or painful for many autistic people for several neurological reasons:

            **Why eye contact is difficult:**
            - **Sensory overload**: Faces and especially eyes contain intense visual information that can be overwhelming to process
            - **Divided attention**: Making eye contact requires so much conscious effort that it interferes with actually listening and processing conversation
            - **Physical discomfort**: Many describe eye contact as physically painful, anxiety-inducing, or intensely uncomfortable
            - **Information processing differences**: Autistic people may actually understand emotions and communication BETTER when not making eye contact because they can focus on voice tone and words

            **What eye contact means (and doesn't mean):**
            ✓ Looking away = Better listening and processing
            ✓ Not looking = Still engaged and caring
            ✗ Eye contact ≠ Honesty or trustworthiness
            ✗ Eye contact ≠ Attention or respect

            **How to support:**
            - **Never force eye contact** - it's counterproductive and uncomfortable
            - Accept "looking near" (forehead, nose, past shoulder)
            - Recognize that listening doesn't require eye contact
            - Value what person is saying over where they're looking
            - Understand accommodations in professional settings (interviews, meetings)

            **For autistic people navigating this:**
            - You don't owe anyone eye contact
            - "Looking near" is a valid accommodation
            - Explain preference when comfortable
            - In professional settings, can negotiate ("I listen better when looking at my notes")

            **Important**: Forcing eye contact doesn't improve communication - it makes it harder. Accept and accommodate individual communication styles.""",
            'category': 'social_communication'
        },
        {
            'input': "I always say the wrong thing in social situations. How do I know what to say?",
            'output': """Many autistic people struggle with implicit social rules that neurotypical people seem to know instinctively. You're not broken - you just need explicit instruction for unspoken rules.

            **Why this happens:**
            - Social rules aren't explicitly taught but are expected to be "absorbed"
            - Rules change based on context in ways that aren't always logical
            - Neurotypical communication relies heavily on implied meaning
            - Small talk follows patterns that aren't always obvious
            - Unspoken rules about topics, timing, and turn-taking

            **Strategies that help:**

            **1. Learn social scripts for common situations:**
            - Greetings: "Hi, how are you?" → "Good, how are you?"
            - Small talk topics: weather, weekend plans, local events
            - Exiting conversation: "It was nice talking to you, I need to go [reason]"
            - Declining: "Thanks for inviting me, but I can't make it"

            **2. Explicit rules for conversation:**
            - Ask questions to show interest (2-3 per conversation)
            - Share similar amount as other person
            - Watch for "wrapping up" signals (looking away, stepping back, checking watch)
            - Avoid correcting minor errors unless critical
            - Special interests: Share briefly unless they ask more

            **3. Topic guidelines:**
            - Safe topics: hobbies, pets, recommendations (movies/books), current non-controversial events
            - Avoid until close friends: politics, religion, health details, money, controversial opinions
            - Check interest: If person gives short answers, change topics

            **4. Recovery from mistakes:**
            - "Sorry, I realize that might have come across wrong"
            - "Let me rephrase that"
            - Don't over-apologize or ruminate
            - Most people forget small social mistakes quickly

            **5. Find understanding people:**
            - Seek friends who appreciate direct communication
            - Online communities with shared interests
            - Other autistic/neurodivergent people
            - Quality over quantity in friendships

            **Remember:** You're learning an implicit system explicitly. That's hard work. Give yourself credit for trying.""",
            'category': 'social_communication'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


def create_executive_function_examples(collector):
    """Examples about executive function"""
    
    examples = [
        {
            'input': "I can't seem to start tasks even when I want to. Why is this so hard?",
            'output': """Task initiation difficulty is a common executive function challenge in autism, not a willpower or motivation problem.

            **Why task initiation is hard:**
            - **Analysis paralysis**: Seeing all steps at once is overwhelming
            - **Perfectionism**: Fear of not doing it "right" prevents starting
            - **Energy assessment**: Unconsciously calculating if you have enough energy
            - **Transition difficulty**: Switching from current state to task requires significant mental energy
            - **Interest-based nervous system**: If not interesting, much harder to start
            - **Unclear steps**: Don't know exactly where/how to begin

            **Strategies that actually help:**

            **1. Break tasks into smallest possible steps:**
            Instead of: "Clean room"
            Break into:
            - Pick up 5 items from floor
            - Put dirty clothes in hamper
            - Make bed
            - Clear desk surface
            - Take out trash

            **2. Use external initiation:**
            - Body doubling (someone present while you work)
            - Accountability partner (text when starting)
            - Timer-based work (Pomodoro: 25 min work, 5 min break)
            - Scheduled start time with alarm
            - "Just 5 minutes" to overcome initial resistance

            **3. Reduce decision fatigue:**
            - Same routine/time for regular tasks
            - Pre-decide where to start
            - Use checklists (no thinking required)
            - Lay out everything needed in advance

            **4. Environment setup:**
            - Remove distractions before starting
            - Have all materials ready
            - Create "launching pad" for tasks
            - Use timers for time awareness

            **5. Pair with dopamine:**
            - Favorite music or podcast
            - Reward after completing
            - Make it a game (time challenges)
            - Work in preferred environment

            **6. Accept accommodation:**
            - Some tasks need external prompting (that's okay!)
            - Use apps/reminders without shame
            - Ask for help with initiation
            - Schedule tasks during peak energy

            **Important**: This is a neurodevelopmental difference, not laziness. Accommodations and support aren't "crutches" - they're necessary tools.""",
            'category': 'executive_function'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


def create_emotional_regulation_examples(collector):
    """Examples about emotional regulation"""
    
    examples = [
        {
            'input': "What's the difference between a meltdown and a tantrum?",
            'output': """Meltdowns and tantrums are fundamentally different - understanding this is crucial for appropriate support.

            **MELTDOWN (Neurological response to overload):**

            **What it is:**
            - Involuntary response to system overload
            - Loss of control over behavior
            - Nervous system overwhelm
            - Fight/flight/freeze/fawn response activated

            **Triggers:**
            - Sensory overload (too much input)
            - Emotional overwhelm
            - Cognitive overload (too much processing)
            - Accumulated stress ("last straw")
            - Change or unexpected events

            **Characteristics:**
            - Can't be stopped by giving in to "demands"
            - Person is not in control
            - May be dangerous to self/others
            - Followed by exhaustion/shame
            - Can't be reasoned with during episode
            - Person wants it to stop but can't

            **What helps:**
            - Reduce sensory input immediately
            - Ensure physical safety
            - Don't talk/reason during episode
            - Allow safe stimming/movement
            - Give space and time
            - Debrief prevention strategies later (not during)

            ---

            **TANTRUM (Behavioral response to not getting want):**

            **What it is:**
            - Intentional behavior to achieve goal
            - Person maintains some control
            - Stops when goal is achieved
            - Learned behavior

            **Triggers:**
            - Being told "no"
            - Not getting desired item/activity
            - Having to do non-preferred task
            - Testing boundaries

            **Characteristics:**
            - Stops when demand is met or removed
            - Person monitors audience reaction
            - Escalates if getting attention
            - Can be reasoned with (though may not listen)
            - Rarely followed by exhaustion

            **What helps:**
            - Consistent boundaries
            - Don't reinforce with giving in
            - Teach appropriate communication
            - Offer choices within limits
            - Follow through with consequences

            ---

            **CRITICAL DISTINCTIONS:**

            | Meltdown | Tantrum |
            |----------|---------|
            | Loss of control | Maintains control |
            | Neurological | Behavioral |
            | Can't stop it | Chooses when to stop |
            | Followed by shame/exhaustion | No aftermath |
            | Not attention-seeking | May be attention-seeking |
            | Needs support | Needs boundaries |

            **Why this matters:**
            - Punishing meltdowns increases trauma and overload
            - Rewarding tantrums reinforces them
            - Wrong response makes both worse
            - Autistic people need support for meltdowns, not discipline

            **Important**: Many autistic people experience both. Understanding the difference helps provide appropriate support.""",
            'category': 'emotional_regulation'
        },
        {
            'input': "How can I prevent meltdowns?",
            'output': """Meltdown prevention requires understanding triggers and recognizing early warning signs.

            **1. Identify early warning signs (yours are unique):**

            **Physical signs:**
            - Increased stimming
            - Difficulty with speech
            - Feeling "buzzy" or on edge
            - Muscle tension
            - Temperature changes
            - Appetite changes

            **Cognitive signs:**
            - Difficulty making decisions
            - Can't process information as quickly
            - Losing words or ability to speak
            - Executive function drops
            - More rigid thinking

            **Emotional signs:**
            - Increased irritability
            - Anxiety rising
            - Feeling overwhelmed
            - Wanting to escape
            - Everything feels "too much"

            **2. Create a prevention plan (when calm):**

            **Sensory accommodations:**
            - Noise-canceling headphones always available
            - Sunglasses for bright environments
            - Fidget/stim tools accessible
            - Comfortable clothing
            - Quiet retreat space identified

            **Energy management:**
            - Schedule breaks between activities
            - Limit high-demand situations
            - Plan recovery time after challenging events
            - Don't overschedule
            - Prioritize sleep and routine

            **Communication:**
            - Pre-teach "I need a break" signal
            - Use scaled responses (1-10 for stress level)
            - Allow exit strategy from situations
            - Minimize verbal demands when stressed

            **Environmental:**
            - Reduce unpredictability when possible
            - Advance notice of changes
            - Visual schedules for transitions
            - Control over some aspects of environment

            **3. Intervene at early warning stage:**

            **When you notice signs:**
            - Remove from triggering situation immediately
            - Reduce sensory input
            - Use calming strategies (deep pressure, movement, favorite sensory input)
            - Postpone non-essential demands
            - Give space and time

            **4. Teach self-advocacy:**
            - Recognize own warning signs
            - Practice asking for accommodations
            - Use tools without shame
            - Communicate needs before crisis
            - Know it's okay to leave situations

            **5. Track patterns:**
            - What times of day are harder?
            - What situations consistently trigger?
            - What's the "last straw" usually?
            - What helps in early stages?

            **Important**: Prevention isn't about never being overwhelmed - it's about catching it early and having tools ready. Some days are harder than others, and that's okay.""",
            'category': 'emotional_regulation'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


def create_neurodiversity_affirming_examples(collector):
    """Examples of neurodiversity-affirming language and concepts"""
    
    examples = [
        {
            'input': "Is autism a disability or just a difference?",
            'output': """Autism is both a disability AND a difference - this isn't contradictory.

            **The disability model (social/medical):**
            - **Disabling aspects**: Executive function challenges, sensory sensitivities, communication differences create real barriers in a world designed for neurotypical people
            - **Need for support**: Accommodations, services, and understanding are necessary
            - **Legal protections**: Disability status provides access to needed services and accommodations
            - **Medical needs**: Some autistic people have co-occurring conditions requiring medical support

            **The difference model (neurodiversity):**
            - **Neurological variation**: Autism is a natural variation in human neurology, not inherently broken
            - **Strengths included**: Pattern recognition, detail focus, deep interests, honesty, creativity, loyalty
            - **Society's role**: Many challenges come from lack of accommodation, not autism itself
            - **Identity**: Many autistic people see autism as core to who they are, not separate

            **Both are true:**
            ✓ Autism brings challenges that can be disabling
            ✓ Autism is a valid way of being human
            ✓ Autistic people need support AND acceptance
            ✓ Some aspects are differences, some are disabilities
            ✓ Each autistic person experiences it differently

            **What this means practically:**

            **Accommodate the challenges:**
            - Sensory accommodations
            - Communication supports
            - Executive function tools
            - Social understanding

            **Value the differences:**
            - Deep focus and expertise
            - Honest communication
            - Pattern thinking
            - Different perspectives

            **Neurodiversity-affirming approach:**
            - Support challenges without trying to "fix" autism
            - Accommodate rather than force conformity
            - Value autistic ways of being
            - Listen to autistic voices
            - Understand both needs and strengths

            **Important**: You can need accommodations AND be proud of being autistic. You can struggle with aspects AND embrace your neurotype. These aren't contradictions.""",
            'category': 'neurodiversity'
        },
        {
            'input': "Should I use person-first (person with autism) or identity-first (autistic person) language?",
            'output': """The autism community LARGELY prefers identity-first language ("autistic person"), though individual preferences matter most.

            **Why many autistic people prefer "autistic person":**
            - Autism isn't separate from who they are
            - It's an integral part of identity, like being tall or artistic
            - Person-first can imply autism is negative/something to distance from
            - Matches other identity language (deaf person, blind person, gay person)
            - Overwhelming preference in self-advocacy community

            **Survey data:**
            - In studies of autistic adults, 60-80% prefer "autistic person"
            - Only 11-20% prefer "person with autism"
            - Many find "person with autism" offensive or dismissive

            **Why person-first exists:**
            - Originally from disability rights movement
            - Intended to emphasize personhood
            - Often preferred by some parents and professionals
            - Required in some professional/medical settings

            **Best practice:**
            1. **Ask individual preference when possible**
            2. **Default to identity-first in general** ("autistic community," "autistic person")
            3. **Respect stated preferences** even if not majority choice
            4. **Never police autistic people's** language about themselves

            **Examples of identity-first:**
            ✓ "I'm autistic"
            ✓ "Autistic people"
            ✓ "My autistic child"
            ✓ "Autistic community"

            **When person-first might be appropriate:**
            - Individual specifically requests it
            - Clinical/medical documentation requirements
            - Speaking about someone who prefers it

            **What to avoid:**
            ✗ "Suffers from autism"
            ✗ "Afflicted with autism"
            ✗ "Autism sufferer"
            ✗ "High/low functioning" (use support needs instead)

            **Important**: Language reflects values. Identity-first acknowledges autism as integral to identity, not a defect to minimize.""",
            'category': 'neurodiversity'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


def create_practical_strategies_examples(collector):
    """Examples of practical, actionable strategies"""
    
    examples = [
        {
            'input': "How do I create a visual schedule that actually helps?",
            'output': """Effective visual schedules match the individual's needs and preferences - here's how to create one that works:

            **1. Choose the right format:**

            **For young children/concrete thinkers:**
            - Photographs of actual activities
            - Real objects representing activities
            - Simple drawings/icons
            - 3-5 items max at a time

            **For older children/teens:**
            - Written words with small pictures
            - Digital schedule on phone/tablet
            - Color-coded categories
            - More items, organized by time blocks

            **For adults:**
            - Digital calendar with notifications
            - Time-blocked schedule
            - Hybrid visual + written
            - Integration with productivity apps

            **2. Level of detail:**

            **Too vague:** "Morning routine"
            **Better:** "Breakfast → Brush teeth → Get dressed → Pack bag"

            **Match to executive function:**
            - Break tasks until each step is achievable
            - If they get stuck, add more detail
            - If overwhelming, reduce detail

            **3. Make it interactive:**

            **Physical schedules:**
            - Velcro pieces to move as completed
            - Checklist to cross off
            - Cards to flip over when done
            - Move to "finished" pocket

            **Digital schedules:**
            - Check off completed items
            - Notifications for transitions
            - Visual countdown timers
            - Reward animations for completion

            **4. Build in flexibility:**

            **Fixed elements:**
            - Regular daily activities
            - Non-negotiable tasks
            - Time-specific appointments

            **Flexible elements:**
            - Choice cards (pick activity)
            - "Break" slots
            - "Surprise" placeholder for unexpected
            - "Maybe" section for possibles

            **5. Handle transitions:**

            **Visual warnings:**
            - Timer showing time left
            - Countdown (3 minutes → 2 minutes → 1 minute)
            - Physical timer they can see
            - Transition object/song

            **6. Location and accessibility:**
            - Eye level in high-traffic area
            - Portable version for on-the-go
            - Multiple copies (home, school, work)
            - Easy to update when plans change

            **7. Teaching and practice:**

            **Introduce gradually:**
            - Start with 2-3 preferred activities
            - Add more as comfortable
            - Practice following schedule
            - Celebrate successes

            **Build independence:**
            - Initially guide through each step
            - Fade prompts gradually
            - Teach checking schedule without prompting
            - Problem-solve barriers together

            **What makes schedules fail:**
            - Too complex/overwhelming
            - Not matching communication level
            - Not accessible when needed
            - Too rigid (doesn't allow changes)
            - Not taught how to use it
            - Only used when convenient

            **Example complete schedule setup:**

            **Morning (7:00-9:00 AM):**
            □ Wake up + stretch [photo of bed]
            □ Bathroom [icon]
            □ Breakfast [photo of cereal]
            □ Medicine [pill icon]
            □ Get dressed [photo of clothes]
            □ Brush teeth [toothbrush icon]
            □ Pack backpack [checklist sub-items]
            □ Leave house [door icon]

            **Each item includes:**
            - Clear start/end point
            - Visual representation
            - Way to mark completion
            - Estimated time if helpful

            **Remember**: The best schedule is the one that actually gets used. Start simple and adjust based on what works.""",
            'category': 'practical_strategies'
        }
    ]
    
    for ex in examples:
        collector.add_example(
            input_text=ex['input'],
            output_text=ex['output'],
            category=ex['category']
        )


# Generate complete dataset
def generate_complete_dataset():
    """
    Generates a comprehensive fine-tuning dataset by calling all domain-specific 
    data creation functions.
    
    Returns:
        Path: The file path to the saved JSONL dataset.
    """
    
    collector = FinetuningDataCollector()
    
    print("Generating comprehensive autism knowledge dataset...")
    
    # Add all categories
    create_sensory_processing_examples(collector)
    print("Added sensory processing examples")
    
    create_social_communication_examples(collector)
    print("Added social communication examples")
    
    create_executive_function_examples(collector)
    print("Added executive function examples")
    
    create_emotional_regulation_examples(collector)
    print("Added emotional regulation examples")
    
    create_neurodiversity_affirming_examples(collector)
    print("Added neurodiversity examples")
    
    create_practical_strategies_examples(collector)
    print("Added practical strategies examples")
    
    # Save dataset
    output_path = collector.save_dataset("autism_knowledge_base.jsonl")
    
    # Print statistics
    stats = collector.get_statistics()
    print(f"\nDataset Statistics:")
    print(f"Total examples: {stats['total_examples']}")
    print(f"Categories: {stats['categories']}")
    print(f"Avg input length: {stats['avg_input_length']:.0f} chars")
    print(f"Avg output length: {stats['avg_output_length']:.0f} chars")
    
    return output_path


if __name__ == "__main__":
    dataset_path = generate_complete_dataset()
    print(f"\nDataset ready for fine-tuning: {dataset_path}")