"""
Manages the persistence, retrieval, and dynamic updating (learning) of user profiles
in the PostgreSQL database using SQLAlchemy. Each profile stores essential personal,
sensory, and behavioral data critical for personalized agent responses.
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

Base = declarative_base()

class UserProfile(Base):
    """
    SQLAlchemy model for user profiles. 
    Uses JSON columns to store complex, structured arrays (e.g., interests, strategies).
    """
    
    __tablename__ = 'user_profiles'
    
    # Primary Fields
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    diagnosis = Column(String)  # e.g., "autism_level1", "self_identified"
    communication_preference = Column(String)  # "direct", "gentle", "visual"
    
    # Complex Profile Data (Stored as JSON)
    sensory_profile = Column(JSON)  # {"seeking": [...], "avoiding": [...]}
    special_interests = Column(JSON)  # [{"topic": "trains", "intensity": "high"}]
    triggers = Column(JSON)  # [{"trigger": "loud_noises", "severity": "high"}]
    strengths = Column(JSON)  # ["pattern_recognition", "memory"]
    challenges = Column(JSON)  # ["executive_function", "social_communication"]
    successful_strategies = Column(JSON)  # ["visual_schedules", "noise_canceling"]
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """Converts the SQLAlchemy model instance to a standard dictionary."""
        return {
            'user_id': self.user_id,
            'age': self.age,
            'diagnosis': self.diagnosis,
            'communication_preference': self.communication_preference,
            'sensory_profile': self.sensory_profile or {},
            'special_interests': self.special_interests or [],
            'triggers': self.triggers or [],
            'strengths': self.strengths or [],
            'challenges': self.challenges or [],
            'successful_strategies': self.successful_strategies or []
        }

class ProfileManager:
    """
    Manages CRUD operations and dynamic learning for user profiles.
    Connects to the specified PostgreSQL database.
    """
    
    def __init__(self, database_url: str):
        """Initializes the database connection and ensures the table exists."""
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        logger.info("ProfileManager initialized and connected to database.")
    
    def create_profile(self, user_id: str, initial_data: Dict) -> UserProfile:
        """Creates and persists a new user profile."""
        
        # Instantiate the model with default fallbacks for JSON fields
        profile = UserProfile(
            user_id=user_id,
            age=initial_data.get('age'),
            diagnosis=initial_data.get('diagnosis'),
            communication_preference=initial_data.get('communication_preference', 'direct'),
            sensory_profile=initial_data.get('sensory_profile', {}),
            special_interests=initial_data.get('special_interests', []),
            triggers=initial_data.get('triggers', []),
            strengths=initial_data.get('strengths', []),
            challenges=initial_data.get('challenges', []),
            successful_strategies=initial_data.get('successful_strategies', [])
        )
        
        self.session.add(profile)
        self.session.commit()
        
        logger.info(f"Created profile for user {user_id}")
        return profile
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        """Retrieves a user profile by user_id and returns it as a dictionary."""
        profile = self.session.query(UserProfile).filter_by(user_id=user_id).first()
        return profile.to_dict() if profile else None
    
    def update_profile(self, user_id: str, updates: Dict) -> UserProfile:
        """Updates an existing user profile with new key-value pairs."""
        profile = self.session.query(UserProfile).filter_by(user_id=user_id).first()
        
        if not profile:
            raise ValueError(f"Profile not found for user {user_id}")
        
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        self.session.commit()
        logger.info(f"Updated profile for user {user_id} with keys: {list(updates.keys())}")
        
        return profile
    
    def learn_from_interaction(self, user_id: str, interaction_data: Dict):
        """
        Dynamically updates the user's profile based on successful interactions 
        or newly identified data points (e.g., successful strategies, triggers).
        
        Args:
            user_id: User identifier.
            interaction_data: Dictionary containing learning signals 
                              (e.g., 'successful_strategy', 'trigger_identified').
        """
        profile = self.session.query(UserProfile).filter_by(user_id=user_id).first()
        
        if not profile:
            logger.warning(f"Cannot learn - profile not found for {user_id}")
            return
        
        if 'successful_strategy' in interaction_data:
            strategy = interaction_data['successful_strategy']
            if profile.successful_strategies is None:
                profile.successful_strategies = []
            
            if strategy not in profile.successful_strategies:
                new_strategies = profile.successful_strategies + [strategy]
                profile.successful_strategies = new_strategies
                logger.info(f"Learned new strategy for {user_id}: {strategy}")
        
        if 'trigger_identified' in interaction_data:
            trigger = interaction_data['trigger_identified']
            if profile.triggers is None:
                profile.triggers = []
            
            trigger_names = [t.get('trigger') for t in profile.triggers if isinstance(t, dict)]
            if trigger not in trigger_names:
                new_trigger_entry = {
                    'trigger': trigger,
                    'severity': interaction_data.get('trigger_severity', 'medium'),
                    'discovered_at': datetime.utcnow().isoformat()
                }
                new_triggers = profile.triggers + [new_trigger_entry]
                profile.triggers = new_triggers
                logger.info(f"Learned new trigger for {user_id}: {trigger}")
        
        if 'interest_mentioned' in interaction_data:
            interest = interaction_data['interest_mentioned']
            if profile.special_interests is None:
                profile.special_interests = []
            
            interest_topics = [i.get('topic') for i in profile.special_interests if isinstance(i, dict)]
            if interest not in interest_topics:
                new_interest_entry = {
                    'topic': interest,
                    'intensity': 'medium',
                    'first_mentioned': datetime.utcnow().isoformat()
                }
                new_interests = profile.special_interests + [new_interest_entry]
                profile.special_interests = new_interests
                logger.info(f"Learned new interest for {user_id}: {interest}")
        
        self.session.commit()
    
    def get_sensory_recommendations(self, user_id: str) -> Dict:
        """
        Generates general sensory recommendations based on the user's current sensory profile.
        This provides generic advice which the LLM agent can further tailor.
        """
        profile = self.get_profile(user_id)
        
        if not profile:
            return {'recommendations': []}
        
        sensory_profile = profile.get('sensory_profile', {})
        seeking = sensory_profile.get('seeking', [])
        avoiding = sensory_profile.get('avoiding', [])
        
        recommendations = {
            'seeking_activities': [],
            'avoiding_accommodations': []
        }
        
        # Recommendations for sensory seeking
        if 'vestibular' in seeking:
            recommendations['seeking_activities'].extend([
                'Swinging or rocking',
                'Trampoline jumping',
                'Spinning in an office chair',
                'Dance or movement activities'
            ])
        
        if 'proprioceptive' in seeking:
            recommendations['seeking_activities'].extend([
                'Heavy lifting or carrying (e.g., books)',
                'Wall pushes or joint compressions',
                'Weighted blanket/vest use',
                'Deep pressure hugs or compression'
            ])
        
        if 'tactile' in seeking:
            recommendations['seeking_activities'].extend([
                'Sensory bins (rice, beans, sand, water)',
                'Play-doh or clay activities',
                'Fidget toys with different textures',
                'Textured materials exploration'
            ])
        
        # Accommodations for sensory avoiding
        if 'auditory' in avoiding:
            recommendations['avoiding_accommodations'].extend([
                'Noise-canceling headphones or earplugs',
                'Requesting quiet spaces for breaks',
                'Advance warning of loud events',
                'Maintaining volume control on devices'
            ])
        
        if 'visual' in avoiding:
            recommendations['avoiding_accommodations'].extend([
                'Sunglasses or tinted glasses indoors if needed',
                'Dimmer lighting or using lamps instead of overheads',
                'Reducing screen brightness and contrast',
                'Avoidance of flickering/fluorescent lights'
            ])
        
        if 'tactile' in avoiding:
            recommendations['avoiding_accommodations'].extend([
                'Tagless, seam-free, or soft clothing',
                'Avoiding sudden or unexpected touch',
                'Control over personal space boundaries',
                'Gloves for messy or textured activities'
            ])
        
        return recommendations


# Test runner
def test_profile_manager():
    """
    Performs basic CRUD and learning tests on the ProfileManager class.
    """
    try:
        from backend.utils.config import get_settings
        settings = get_settings()
        manager = ProfileManager(settings.postgres_url)
    except ImportError:
        DB_URL = os.getenv("POSTGRES_URL", "sqlite:///:memory:")
        manager = ProfileManager(DB_URL)
        print("Using in-memory SQLite for testing.")
        
    print("--- Profile Manager Test Sequence ---")
    
    user_id = f"test_user_{datetime.utcnow().timestamp()}"
    initial_data = {
        'age': 24,
        'diagnosis': 'autism_level1',
        'communication_preference': 'direct',
        'sensory_profile': {
            'seeking': ['proprioceptive', 'tactile'],
            'avoiding': ['auditory', 'visual']
        },
        'special_interests': [{'topic': 'trains', 'intensity': 'high'}],
        'triggers': [{'trigger': 'unexpected_changes', 'severity': 'high'}],
        'successful_strategies': ['visual_schedules']
    }
    
    try:
        profile = manager.create_profile(user_id, initial_data)
        print(f"Created profile for {user_id}")
    except Exception as e:
        print(f"Error creating profile: {e}")
        return
    
    retrieved = manager.get_profile(user_id)
    print(f"Retrieved profile. Interests: {len(retrieved.get('special_interests', []))}")
    
    manager.learn_from_interaction(user_id, {
        'successful_strategy': 'noise_canceling_headphones',
        'trigger_identified': 'crowded_spaces',
        'trigger_severity': 'critical',
        'interest_mentioned': 'astronomy'
    })
    print("Learned from interaction signals.")
    
    updated = manager.get_profile(user_id)
    print("\n--- LEARNING ASSERTIONS ---")
    
    strategies = updated.get('successful_strategies', [])
    strategy_check = 'noise_canceling_headphones' in strategies
    print(f"Strategy check: {'PASS' if strategy_check else 'FAIL'} (Count: {len(strategies)})")
    
    triggers = updated.get('triggers', [])
    trigger_names = [t['trigger'] for t in triggers if isinstance(t, dict)]
    trigger_check = 'crowded_spaces' in trigger_names
    print(f"Trigger check: {'PASS' if trigger_check else 'FAIL'} (Count: {len(triggers)})")

    interests = updated.get('special_interests', [])
    interest_topics = [i['topic'] for i in interests if isinstance(i, dict)]
    interest_check = 'astronomy' in interest_topics
    print(f"Interest check: {'PASS' if interest_check else 'FAIL'} (Count: {len(interests)})")
    
    recs = manager.get_sensory_recommendations(user_id)
    print("\n--- SENSORY RECOMMENDATIONS ---")
    print(f"Proprioceptive seeking activities: {recs['seeking_activities'][:2]}")
    print(f"Auditory avoiding accommodations: {recs['avoiding_accommodations'][:2]}")
    print("---------------------------------")

if __name__ == "__main__":
    test_profile_manager()