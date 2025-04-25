import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration manager for the Laravel Developer Agent."""
    
    @property
    def ANTHROPIC_API_KEY(self) -> str:
        return os.getenv("ANTHROPIC_API_KEY", "")
    
    @property
    def MODEL(self) -> str:
        return os.getenv("MODEL", "claude-3-7-sonnet-latest")
    
    @property
    def MAX_TOKENS(self) -> int:
        return int(os.getenv("MAX_TOKENS", "4000"))
    
    @property
    def TEMPERATURE(self) -> float:
        return float(os.getenv("TEMPERATURE", "0.7"))
    
    @property
    def DEBUG(self) -> bool:
        return os.getenv("DEBUG", "false").lower() == "true"
    
    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv("LOG_LEVEL", "info")
    
    def validate(self) -> bool:
        """
        Validate the configuration is complete and valid.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not self.ANTHROPIC_API_KEY:
            print("Error: ANTHROPIC_API_KEY is not set in .env file")
            return False
            
        return True

# Provide a simple way to access configuration
config = Config() 