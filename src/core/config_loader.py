"""
Configuration file loader for servers.yaml
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    Loads and parses servers.yaml configuration file
    """
    
    def __init__(self, config_path: str = "config/servers.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            
            # Replace environment variables
            self._replace_env_vars(self.config)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def _replace_env_vars(self, obj: Any) -> Any:
        """
        Recursively replace ${VAR_NAME} with environment variable values
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._replace_env_vars(value)
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${" ) and obj.endswith("}"):
            var_name = obj[2:-1]
            value = os.getenv(var_name)
            if value is None:
                logger.warning(f"Environment variable not found: {var_name}")
            return value
        
        return obj
    
    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all server configurations
        
        Returns:
            Dictionary of server configurations
        """
        if not self.config:
            self.load()
        
        return self.config.get('servers', {})
    
    def get_server(self, server_name: str) -> Optional[Dict[str, Any]]:
        """
        Get specific server configuration
        
        Args:
            server_name: Name of the server
            
        Returns:
            Server configuration or None
        """
        servers = self.get_servers()
        return servers.get(server_name)
    
    def get_global_config(self) -> Dict[str, Any]:
        """
        Get global configuration
        
        Returns:
            Global configuration dictionary
        """
        if not self.config:
            self.load()
        
        return self.config.get('global', {})
