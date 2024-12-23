import yaml
import os
from typing import Any, Dict

class ConfigManager:
    _instance = None
    
    def __init__(self):
        if ConfigManager._instance is not None:
            raise Exception("ConfigManager is a singleton!")
        ConfigManager._instance = self
        self.config: Dict[str, Any] = {}
        self.load_configs()
        
    @staticmethod
    def get_instance():
        if ConfigManager._instance is None:
            ConfigManager()
        return ConfigManager._instance
        
    def load_configs(self):
        """Load all configuration files from the config directory"""
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        
        for filename in os.listdir(config_dir):
            if filename.endswith('.yaml'):
                config_name = os.path.splitext(filename)[0]
                with open(os.path.join(config_dir, filename), 'r') as f:
                    self.config[config_name] = yaml.safe_load(f)
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation
        Example: config.get('game.window.width')
        """
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value 