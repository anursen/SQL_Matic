import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._load_environment()
        self._load_yaml_config()
        self._validate_config()

    def _load_environment(self):
        """Load environment variables"""
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.environment = os.getenv("ENVIRONMENT", "development")
        
    def _load_yaml_config(self):
        """Load YAML configuration"""
        config_path = Path(__file__).parent / "config.yaml"
        try:
            with open(config_path) as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load config.yaml: {str(e)}")

    def _validate_config(self):
        """Validate required configuration"""
        if not self.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY not found in environment variables")

    @property
    def llm_config(self) -> Dict[str, Any]:
        return self._config.get('llm', {})

    @property
    def database_config(self) -> Dict[str, Any]:
        return self._config.get('database', {})

    @property
    def api_config(self) -> Dict[str, Any]:
        return self._config.get('api', {})

    @property
    def evaluation_config(self) -> Dict[str, Any]:
        return self._config.get('evaluation', {})

    @property
    def templates_config(self) -> Dict[str, Any]:
        return self._config.get('templates', {})
    
    @property
    def tool_get_data_dictionary(self) -> Dict[str, Any]:
        return self._config.get('tool_get_data_dictionary', {})
    
    @property
    def tool_execute_sql(self) -> Dict[str, Any]:
        return self._config.get('tool_execute_sql', {})
    
    @property
    def tool_get_schema(self) -> Dict[str, Any]:
        return self._config.get('tool_get_schema', {})

    @property
    def assistant_config(self) -> Dict[str, Any]:
        return self._config.get('assistant', {})

# Global config instance
config = Config()
