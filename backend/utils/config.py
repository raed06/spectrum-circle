from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings class. Reads configuration variables from environment 
    variables or a '.env' file. 
    
    This class organizes all necessary credentials, endpoints, and flags 
    for the application's different services (AI, Database, Security, etc.).
    """
    
    # Google AI
    google_api_key: str # Required API key for accessing Google Generative AI services.
    gemini_model: str = "gemini-2.0-flash-exp" # The default Gemini model name for chat responses.
    
    # External API keys
    tavily_api_key: str # Required API key for accessing Tavily API.
    live_search: bool = False # Flag to enable/disable live search.

    # Database
    postgres_url: str # Connection URL for the PostgreSQL database.
    
    # Application
    environment: str = "development" # Application environment ('development', 'staging', 'production').
    log_level: str = "INFO" # Logging verbosity level (e.g., 'DEBUG', 'INFO', 'WARNING').
    enable_analytics: bool = True # Flag to enable/disable user analytics tracking.

    # Fine-tuned models
    use_finetuned_models: bool = True # Flag to enable/disable the use of fine-tuned models.
    finetuned_base_model: str = "models/autism-knowledge-base-v1"
    finetuned_alex_model: str = "tunedModels/alex-peer-support-v1"
    finetuned_maya_model: str = "tunedModels/maya-therapist-v1"
    finetuned_jordan_model: str = "tunedModels/jordan-teen-support-v1"
    finetuned_dr_chen_model: str = "tunedModels/dr-chen-activities-specialist-v1"
    finetuned_sam_model: str = "tunedModels/sam-parent-support-v1"
    finetuned_river_model: str = "tunedModels/river-sibling-support-v1"
    
    # Fallback to base model if fine-tuned not available
    fallback_to_base_model: bool = True

    # MCP
    mcp_port: int = 8765 # Port for the MCP server.
    mcp_server_url: str = "http://localhost:8765" # URL for the MCP server.

    # API
    api_port: int = 8000 # Port for the API server.

    # Monitoring
    langfuse_secret_key: str | None = None # API key for LangSmith.
    langfuse_public_key: str | None = None # API key for LangSmith.
    langfuse_base_url: str | None = None # API key for LangSmith.

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """
    Retrieves the global settings instance.
    
    Returns:
        Settings: The cached configuration object.
    """
    return Settings()