"""
Primary entry point for the SpectrumCircle REST and WebSocket API.
Initializes the FastAPI application, middleware, global services, and defines 
all core user-facing endpoints for profile management, chat, and activity recommendations.
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
from loguru import logger

from backend.agents.orchestrator.router import AgentOrchestrator
from backend.memory.user_profiles.profile_manager import ProfileManager
from backend.memory.conversation_memory import ConversationMemory
from backend.utils.config import get_settings

# FastAPI app initialization
app = FastAPI(
    title="SpectrumCircle API",
    description="AI-powered support community for autism and neurodiversity.",
    version="1.0.0"
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instances
settings = get_settings()
orchestrator = AgentOrchestrator()
profile_manager = ProfileManager(settings.postgres_url)
memory = ConversationMemory()

# Dictionary to hold active WebSocket connections {user_id: WebSocket}
active_connections: Dict[str, WebSocket] = {}

# Models
class UserProfileCreate(BaseModel):
    """Data model for creating or updating a user profile."""
    user_id: str
    age: Optional[int] = None
    diagnosis: Optional[str] = None
    communication_preference: str = "direct"
    sensory_profile: Optional[Dict] = {}
    special_interests: Optional[List[Dict]] = []
    triggers: Optional[List[Dict]] = []


class MessageRequest(BaseModel):
    """Data model for a message sent via the REST /chat endpoint."""
    user_id: str
    message: str
    emotional_state: Optional[str] = None


# API Endpoints (REST)
@app.get("/")
async def root():
    """Returns the API health status and version information."""
    return {
        "status": "healthy",
        "service": "SpectrumCircle API",
        "version": "1.0.0"
    }

# Profile Management
@app.post("/profiles")
async def create_profile(profile_data: UserProfileCreate):
    """Creates a new user profile in the database."""
    try:

        # Check if profile exists
        if not profile_manager.get_profile(profile_data.user_id):
            profile_manager.create_profile(
                user_id=profile_data.user_id,
                initial_data=profile_data.dict()
            )
        
        return {
            "success": True,
            "user_id": profile_data.user_id,
            "message": "Profile created successfully"
        }
    
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles/{user_id}")
async def get_profile(user_id: str):
    """Retrieves an existing user profile."""
    profile = profile_manager.get_profile(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {
        "success": True,
        "profile": profile
    }

# User Statistics
@app.get("/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Retrieves aggregated statistics and progress metrics for a user."""
    try:
        # Get conversation summary
        conv_summary = memory.get_conversation_summary(user_id)
        
        # Get profile
        profile = profile_manager.get_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "success": True,
            "stats": {
                "total_conversations": conv_summary.get('total_messages', 0),
                "most_used_agent": conv_summary.get('most_common_agent', 'none'),
                "most_common_emotion": conv_summary.get('most_common_emotion', 'unknown'),
                "special_interests_count": len(profile.get('special_interests', [])),
                "strategies_learned": len(profile.get('successful_strategies', [])), 
                "triggers_identified": len(profile.get('triggers', []))
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket Endpoint (Real-time Chat)
@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """
    Handles real-time, bi-directional chat communication.
    Manages connection state, receiving messages, sending typing indicators, 
    routing to agents, and storing conversation history.
    """
    await websocket.accept()
    active_connections[user_id] = websocket
    
    logger.info(f"WebSocket connection established for user {user_id}")
    
    try:
        user_profile = profile_manager.get_profile(user_id)
        
        if not user_profile:
            profile_manager.create_profile(user_id, {
                'age': 25,
                'communication_preference': 'direct'
            })
            user_profile = profile_manager.get_profile(user_id)
        
        await websocket.send_json({
            "type": "system",
            "message": "Connected! Your support circle is here to help. 💙"
        })
        
        while True:
            try:
                data = await websocket.receive_json()
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                break # Exit loop on receive error
            
            message = data.get('message')
            emotional_state = data.get('emotional_state', 'unknown')
            age = int(data.get('age', user_profile.get('age', 25)))
            role = data.get('role', 'Individual')
            
            if not message:
                continue
            
            logger.info(f"Received message from {user_id}: {message[:50]}...")
            
            context_data = memory.get_context_for_query(user_id, message)
            
            full_context = {
                'user_profile': user_profile, 
                'emotional_state': emotional_state,
                'user_data_from_ws': {'age': age, 'role': role}, 
                'conversation_history': context_data.get('recent_history', [])
            }
            
            try:
                await websocket.send_json({"type": "typing", "agent": "thinking..."})
                logger.debug("Sent typing indicator")
            except Exception as e:
                logger.error(f"Error sending typing indicator: {e}")
            
            try:
                response = await orchestrator.route_query(
                    user_message=message,
                    context=full_context
                )
                logger.info(f"Got response from agent: {response.get('agent')}")
            except Exception as e:
                logger.error(f"Error getting agent response: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Sorry, something went wrong with the AI agent. Please try again."
                })
                continue
            
            try:
                memory.add_message(
                    user_id=user_id,
                    role='user',
                    content=message,
                    metadata={'emotional_state': emotional_state}
                )
                
                memory.add_message(
                    user_id=user_id,
                    role='agent',
                    content=response.get('message', ''),
                    agent_name=response.get('agent', 'unknown'),
                    metadata=response.get('metadata', {})
                )
                logger.debug("Saved messages to memory")
            except Exception as e:
                logger.error(f"Error saving to memory: {e}")
            
            try:
                response_data = {
                    "type": "message",
                    "agent": response.get('agent', 'system'),
                    "message": response.get('message', 'I apologize, I encountered an error.'),
                    "suggestions": response.get('suggestions', []),
                    "metadata": response.get('metadata', {}),
                    "is_crisis": response.get('is_crisis', False)
                }
                
                await websocket.send_json(response_data)
                logger.info("Successfully sent primary response to frontend")
            except Exception as e:
                logger.error(f"Error sending primary response to frontend: {e}")
                logger.exception(e)
            
            # Send additional perspectives for multi-agent response
            if response.get('additional_perspectives'):
                logger.info(f"Sending {len(response['additional_perspectives'])} additional perspectives")
                for perspective in response['additional_perspectives']:
                    await asyncio.sleep(1)
                    try:
                        await websocket.send_json({
                            "type": "message",
                            "agent": perspective['agent'],
                            "message": perspective['message'],
                            "is_additional": True
                        })
                        logger.info(f"Sent additional perspective from {perspective['agent']}")
                    except Exception as e:
                        logger.error(f"Error sending additional perspective: {e}")
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
        if user_id in active_connections:
            del active_connections[user_id]
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        logger.exception(e)
        try:
            await websocket.send_json({
                "type": "error",
                "message": "A critical server error occurred. Please refresh."
            })
        except:
            pass
        
        if user_id in active_connections:
            del active_connections[user_id]


# Application Startup
if __name__ == "__main__":
    import uvicorn

    # Configure logging for file output
    logger.add(
        "logs/app.log",
        rotation="500 MB",  
        retention="10 days",
        level="DEBUG"
    )
    
    logger.info("Starting SpectrumCircle API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.environment == 'development'}")

    # Run the Uvicorn server
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=False,
        log_level="info"
    )