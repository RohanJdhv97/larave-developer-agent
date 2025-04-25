"""
Tests for the config module
"""
import unittest
import os
from src.utils.config import Config

class TestConfig(unittest.TestCase):
    """Test cases for the Config class"""
    
    def test_default_values(self):
        """Test that default values are set correctly"""
        # Create a test config instance
        config = Config()
        
        # Test default values
        self.assertEqual(config.MODEL, "claude-3-7-sonnet-latest")
        self.assertEqual(config.MAX_TOKENS, 4000)
        self.assertEqual(config.TEMPERATURE, 0.7)
        self.assertEqual(config.DEBUG, False)
        self.assertEqual(config.LOG_LEVEL, "info")
    
    def test_environment_variables(self):
        """Test that environment variables are loaded correctly"""
        # Set test environment variables
        os.environ["MODEL"] = "test-model"
        os.environ["MAX_TOKENS"] = "1000"
        os.environ["TEMPERATURE"] = "0.5"
        os.environ["DEBUG"] = "true"
        os.environ["LOG_LEVEL"] = "debug"
        
        # Create a test config instance
        config = Config()
        
        # Test environment variable values
        self.assertEqual(config.MODEL, "test-model")
        self.assertEqual(config.MAX_TOKENS, 1000)
        self.assertEqual(config.TEMPERATURE, 0.5)
        self.assertEqual(config.DEBUG, True)
        self.assertEqual(config.LOG_LEVEL, "debug")
        
        # Reset environment variables
        for key in ["MODEL", "MAX_TOKENS", "TEMPERATURE", "DEBUG", "LOG_LEVEL"]:
            if key in os.environ:
                del os.environ[key]

if __name__ == "__main__":
    unittest.main() 