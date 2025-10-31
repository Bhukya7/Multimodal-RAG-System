"""
Configuration management
"""

import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config.yaml"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            default_config = {
                "app": {
                    "name": "Multimodal RAG System",
                    "version": "1.0.0"
                },
                "vector_db": {
                    "path": "./data/vector_db",
                    "collection_name": "multimodal_docs"
                },
                "embedding": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                },
                "processing": {
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "max_file_size_mb": 10,
                    "supported_extensions": [".txt", ".pdf", ".png", ".jpg", ".jpeg"]
                },
                "retrieval": {
                    "default_top_k": 5,
                    "similarity_threshold": 0.5
                },
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            }
            
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            return default_config
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)