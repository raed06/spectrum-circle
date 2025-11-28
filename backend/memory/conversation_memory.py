"""
Manages the conversation history using a dual-memory approach:
1. Short-Term Memory (STM): An in-memory deque for fast access to recent messages.
2. Long-Term Memory (LTM): A ChromaDB vector store for semantic search of past, non-recent interactions.
"""
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import chromadb
from chromadb.config import Settings
import json
from loguru import logger

class ConversationMemory:
    """
    Manages conversation history using a combination of fast, in-memory short-term 
    memory and a persistent, semantically searchable long-term memory (ChromaDB).
    """
    
    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        max_short_term: int = 10
    ):
        """
        Initializes the memory system.
        
        Args:
            persist_directory: The file path for the ChromaDB persistence.
            max_short_term: The maximum number of messages to keep in the in-memory short-term history.
        """
        # Initialize ChromaDB Client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Collection for long-term memory (stores message content vectors)
        self.collection = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Conversation history"}
        )
        
        # Short-term memory (in-memory deque for fast, recent context)
        self.short_term: Dict[str, deque] = {}  # user_id -> deque of recent messages
        self.max_short_term = max_short_term
        
        logger.info("ConversationMemory initialized with dual-memory architecture.")
    
    def add_message(
        self,
        user_id: str,
        role: str,  # 'user' or 'agent'
        content: str,
        agent_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Adds a message to both short-term (in-memory) and long-term (vector store) memory.
        
        Args:
            user_id: User identifier.
            role: The source of the message ('user' or 'agent').
            content: The message text.
            agent_name: Name of the responding agent (if role='agent').
            metadata: Structured data about the message (e.g., emotional state, topics).
        """
        
        message = {
            'role': role,
            'content': content,
            'agent': agent_name,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }
        
        if user_id not in self.short_term:
            self.short_term[user_id] = deque(maxlen=self.max_short_term)
        self.short_term[user_id].append(message)
        
        conversation_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        
        chroma_metadata = {
            'user_id': user_id,
            'role': role,
            'agent': agent_name or 'none',
            'timestamp': message['timestamp'],
            'emotional_state': message['metadata'].get('emotional_state', 'unknown'),
            'topics': json.dumps(message['metadata'].get('topics', []))
        }
        
        self.collection.add(
            ids=[conversation_id],
            documents=[content],
            metadatas=[chroma_metadata]
        )
        
        logger.debug(f"Added message to dual memory for {user_id}")
    
    def get_recent_history(
        self,
        user_id: str,
        n_messages: int = 5
    ) -> List[Dict]:
        """
        Retrieves the most recent conversation history from short-term memory.
        
        Args:
            user_id: User identifier.
            n_messages: Number of messages to retrieve.
            
        Returns:
            A list of the most recent message dictionaries.
        """
        if user_id not in self.short_term:
            return []
        
        recent = list(self.short_term[user_id])[-n_messages:]
        return recent
    
    def search_conversations(
        self,
        user_id: str,
        query: str,
        n_results: int = 3
    ) -> List[Dict]:
        """
        Performs a semantic search on the long-term memory for relevant past messages.
        
        Args:
            user_id: User identifier (used for filtering).
            query: The current query/context used for semantic matching.
            n_results: The number of top relevant results to retrieve.
            
        Returns:
            A list of relevant past conversation segments.
        """
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id},
            include=['documents', 'metadatas', 'distances']
        )
        
        if not results['ids'] or not results['ids'][0]:
            return []
        
        conversations = []
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            
            conv = {
                'content': results['documents'][0][i],
                'role': metadata.get('role'),
                'agent': metadata.get('agent'),
                'timestamp': metadata.get('timestamp'),
                'emotional_state': metadata.get('emotional_state'),
                'topics': json.loads(metadata.get('topics', '[]')), 
                'relevance': results['distances'][0][i]
            }
            conversations.append(conv)
        
        return conversations
    
    def get_conversation_summary(self, user_id: str) -> Dict:
        """
        Analyzes the user's entire conversation history to extract pattern statistics.
        
        Returns:
            A dictionary containing summary statistics (e.g., total messages, most common agent/emotion).
        """
        
        all_convs = self.collection.get(
            where={"user_id": user_id},
            include=['metadatas']
        )
        
        if not all_convs['ids']:
            return {'total_messages': 0}
        
        agents_used = {}
        emotional_states = {}
        
        for metadata in all_convs['metadatas']:
            agent = metadata.get('agent', 'unknown')
            agents_used[agent] = agents_used.get(agent, 0) + 1
            
            emotion = metadata.get('emotional_state', 'unknown')
            emotional_states[emotion] = emotional_states.get(emotion, 0) + 1
        
        def get_most_common(data_dict, default='none'):
            if not data_dict:
                return default
            return max(data_dict, key=data_dict.get)

        return {
            'total_messages': len(all_convs['ids']),
            'agents_used': agents_used,
            'emotional_states': emotional_states,
            'most_common_agent': get_most_common(agents_used),
            'most_common_emotion': get_most_common(emotional_states)
        }
    
    def get_context_for_query(
        self,
        user_id: str,
        current_query: str
    ) -> Dict:
        """
        Combines STM and LTM to provide a rich context for the LLM's next response.
        
        Returns:
            A context dictionary containing recent history and semantically relevant past conversations.
        """
        
        # Get recent history (STM)
        recent = self.get_recent_history(user_id, n_messages=5)
        
        # Search for relevant past conversations (LTM)
        relevant = self.search_conversations(user_id, current_query, n_results=3)
        
        return {
            'recent_history': recent,
            'relevant_past': relevant
        }


# Test Runner
def test_conversation_memory():
    """Demonstrates adding messages, retrieving recent history, searching LTM, and getting summaries."""
    
    memory = ConversationMemory(persist_directory="./test_chroma")
    
    try:
        memory.client.delete_collection(name="conversations")
        memory = ConversationMemory(persist_directory="./test_chroma")
        logger.info("Cleaned and re-initialized store for testing.")
    except Exception:
        pass

    user_id = "test_user_123"
    
    # Simulate conversation messages
    conversations = [
        {
            'role': 'user',
            'content': "I'm nervous about my new job starting next week, I hate surprises.",
            'metadata': {'emotional_state': 'anxious', 'topics': ['work', 'anxiety']}
        },
        {
            'role': 'agent',
            'agent': 'alex',
            'content': "I totally get it! We can create a visual schedule for your first day.",
            'metadata': {'emotional_state': 'supportive', 'topics': ['work', 'strategy']}
        },
        {
            'role': 'user',
            'content': "The social part worries me most, like what to say during lunch.",
            'metadata': {'emotional_state': 'worried', 'topics': ['social', 'work']}
        },
        {
            'role': 'agent',
            'agent': 'maya',
            'content': "Let's create some simple social scripts for common lunch situations.",
            'metadata': {'emotional_state': 'helpful', 'topics': ['social_skills', 'strategy']}
        }
    ]
    
    # Add messages
    for msg in conversations:
        memory.add_message(
            user_id=user_id,
            role=msg['role'],
            content=msg['content'],
            agent_name=msg.get('agent'),
            metadata=msg.get('metadata')
        )
    
    print("\nAdded conversation history")
    
    # Get recent history (STM)
    recent = memory.get_recent_history(user_id, n_messages=3)
    print("\n--- 1. Short-Term History (STM) ---")
    print(f"Retrieved {len(recent)} messages from recent history:")
    for msg in recent:
        print(f"  [{msg['role'].upper()}] {msg['content'][:35]}...")
    
    # Search conversations (LTM)
    search_query = "how to handle unexpected changes at work"
    results = memory.search_conversations(user_id, search_query, n_results=2)
    print("\n--- 2. Long-Term Search (LTM) ---")
    print(f"Search results for semantic query: **'{search_query}'**")
    for result in results:
        print(f"  → [{result['role'].upper()}] (Agent: {result['agent']}) Relevance: {result['relevance']:.4f}")
        print(f"    Content: {result['content'][:50]}...")
    
    # Get summary
    summary = memory.get_conversation_summary(user_id)
    print("\n--- 3. Conversation Summary ---")
    print(f"  Total messages: {summary['total_messages']}")
    print(f"  Most used agent: **{summary['most_common_agent']}**")
    print(f"  Most common emotion: **{summary['most_common_emotion']}**")
    
    # Get combined context
    context_query = "I'm still worried about the social part of the job"
    context = memory.get_context_for_query(user_id, context_query)
    print("\n--- 4. Combined Context for New Query ---")
    print(f"Query: **{context_query}**")
    print(f"  Recent messages (STM): {len(context['recent_history'])}")
    print(f"  Relevant past (LTM): {len(context['relevant_past'])}")


if __name__ == "__main__":
    import sys
    logger.add(sys.stderr, level="INFO") 
    test_conversation_memory()