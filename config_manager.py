"""Centralized configuration manager for admin settings."""

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path
from supabase import Client
from dotenv import load_dotenv
import config

load_dotenv()


@dataclass
class TrendingConfig:
    """Configuration for trending skills calculation."""
    max_mention_rate: float = 0.3
    min_baseline_score: int = 50
    trending_threshold: int = 70
    mention_weight: float = 0.5
    github_weight: float = 0.3
    linkedin_weight: float = 0.2
    trend_window_days: int = 30
    recency_decay_factor: float = 0.1


@dataclass
class AIModelConfig:
    """Configuration for AI models."""
    llm_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 2000
    embeddings_model: str = "text-embedding-3-small"


@dataclass
class AgentConfig:
    """Configuration for AI agents."""
    content_scraper_enabled: bool = True
    trend_analyzer_enabled: bool = True
    max_search_results: int = 10
    max_trend_items: int = 15
    search_depth: str = "advanced"
    content_types: List[str] = None
    trend_sources: List[str] = None

    def __post_init__(self):
        if self.content_types is None:
            self.content_types = ["tutorial", "course", "article", "video", "documentation"]
        if self.trend_sources is None:
            self.trend_sources = ["github", "linkedin"]


@dataclass
class SystemConfig:
    """Complete system configuration."""
    ai_models: AIModelConfig
    agents: AgentConfig
    trending: TrendingConfig
    api_endpoints: Dict[str, Any]
    database: Dict[str, Any]
    rag_workflow: Dict[str, Any]

    def __post_init__(self):
        if self.api_endpoints is None:
            self.api_endpoints = {
                "github_api": "https://api.github.com",
                "tavily_enabled": True
            }
        if self.database is None:
            self.database = {
                "query_timeout": 30,
                "max_results": 100
            }
        if self.rag_workflow is None:
            self.rag_workflow = {
                "enable_reasoning": True,
                "enable_refinement": True,
                "confidence_threshold": 0.7,
                "max_refinement_iterations": 2
            }


class ConfigManager:
    """Manages system configuration with file and database support."""
    
    def __init__(self, db_client: Optional[Client] = None):
        """Initialize configuration manager.
        
        Args:
            db_client: Optional Supabase client for runtime overrides
        """
        self.db_client = db_client
        self.config_file = Path("admin_config.json")
        self._default_config: Optional[SystemConfig] = None
        self._cached_config: Optional[SystemConfig] = None
    
    def load_default_config(self) -> SystemConfig:
        """Load configuration from files.
        
        Returns:
            System configuration
        """
        if self._default_config:
            return self._default_config
        
        # Load from admin_config.json if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
            except Exception as e:
                print(f"Error loading {self.config_file}: {e}")
                config_data = {}
        else:
            # Create default config file
            config_data = self._create_default_config()
            self.save_config_to_file(config_data)
        
        # Build configuration objects
        self._default_config = self._build_config(config_data)
        return self._default_config
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration structure.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "ai_models": {
                "llm_model": os.getenv("LLM_MODEL", "gpt-4-turbo-preview"),
                "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
                "max_tokens": 2000,
                "embeddings_model": "text-embedding-3-small"
            },
            "agents": {
                "content_scraper": {
                    "enabled": True,
                    "max_search_results": 10,
                    "search_depth": "advanced"
                },
                "trend_analyzer": {
                    "enabled": True,
                    "max_trend_items": 15,
                    "sources": ["github", "linkedin"]
                },
                "content_types": ["tutorial", "course", "article", "video", "documentation"]
            },
            "api_endpoints": {
                "github_api": "https://api.github.com",
                "tavily_enabled": True
            },
            "database": {
                "query_timeout": 30,
                "max_results": 100
            },
            "rag_workflow": {
                "enable_reasoning": True,
                "enable_refinement": True,
                "confidence_threshold": 0.7,
                "max_refinement_iterations": 2
            },
            "trending": {
                "max_mention_rate": 0.3,
                "min_baseline_score": 50,
                "trending_threshold": 70,
                "mention_weight": 0.5,
                "github_weight": 0.3,
                "linkedin_weight": 0.2,
                "trend_window_days": 30,
                "recency_decay_factor": 0.1
            }
        }
    
    def _build_config(self, config_data: Dict[str, Any]) -> SystemConfig:
        """Build SystemConfig from dictionary.
        
        Args:
            config_data: Configuration data dictionary
            
        Returns:
            SystemConfig object
        """
        # Extract AI models config
        ai_data = config_data.get("ai_models", {})
        ai_models = AIModelConfig(
            llm_model=ai_data.get("llm_model", "gpt-4-turbo-preview"),
            temperature=ai_data.get("temperature", 0.7),
            max_tokens=ai_data.get("max_tokens", 2000),
            embeddings_model=ai_data.get("embeddings_model", "text-embedding-3-small")
        )
        
        # Extract agents config
        agents_data = config_data.get("agents", {})
        agents = AgentConfig(
            content_scraper_enabled=agents_data.get("content_scraper", {}).get("enabled", True),
            trend_analyzer_enabled=agents_data.get("trend_analyzer", {}).get("enabled", True),
            max_search_results=agents_data.get("content_scraper", {}).get("max_search_results", 10),
            max_trend_items=agents_data.get("trend_analyzer", {}).get("max_trend_items", 15),
            search_depth=agents_data.get("content_scraper", {}).get("search_depth", "advanced"),
            content_types=agents_data.get("content_types", ["tutorial", "course", "article", "video", "documentation"]),
            trend_sources=agents_data.get("trend_analyzer", {}).get("sources", ["github", "linkedin"])
        )
        
        # Extract trending config
        trending_data = config_data.get("trending", {})
        trending = TrendingConfig(
            max_mention_rate=trending_data.get("max_mention_rate", 0.3),
            min_baseline_score=trending_data.get("min_baseline_score", 50),
            trending_threshold=trending_data.get("trending_threshold", 70),
            mention_weight=trending_data.get("mention_weight", 0.5),
            github_weight=trending_data.get("github_weight", 0.3),
            linkedin_weight=trending_data.get("linkedin_weight", 0.2),
            trend_window_days=trending_data.get("trend_window_days", 30),
            recency_decay_factor=trending_data.get("recency_decay_factor", 0.1)
        )
        
        return SystemConfig(
            ai_models=ai_models,
            agents=agents,
            trending=trending,
            api_endpoints=config_data.get("api_endpoints", {}),
            database=config_data.get("database", {}),
            rag_workflow=config_data.get("rag_workflow", {})
        )
    
    def get_config(self, use_cache: bool = True) -> SystemConfig:
        """Get current system configuration with database overrides.
        
        Args:
            use_cache: Whether to use cached configuration
            
        Returns:
            System configuration with runtime overrides applied
        """
        if use_cache and self._cached_config:
            return self._cached_config
        
        # Start with default config
        config = self.load_default_config()
        
        # Apply database overrides if available
        if self.db_client:
            overrides = self._get_database_overrides()
            if overrides:
                config = self._apply_overrides(config, overrides)
        
        self._cached_config = config
        return config
    
    def _get_database_overrides(self) -> Dict[str, Any]:
        """Get configuration overrides from database.
        
        Returns:
            Dictionary of overrides by category
        """
        if not self.db_client:
            return {}
        
        try:
            result = self.db_client.table('system_settings').select('*').execute()
            overrides = {}
            
            for row in result.data:
                category = row.get('category', 'default')
                key = row.get('key')
                value = row.get('value')
                
                if category not in overrides:
                    overrides[category] = {}
                overrides[category][key] = value
            
            return overrides
        except Exception as e:
            print(f"Error loading database overrides: {e}")
            return {}
    
    def _apply_overrides(self, config: SystemConfig, overrides: Dict[str, Any]) -> SystemConfig:
        """Apply database overrides to configuration.
        
        Args:
            config: Base configuration
            overrides: Override values by category
            
        Returns:
            Configuration with overrides applied
        """
        # Create a mutable copy
        import copy
        new_config = copy.deepcopy(config)
        
        # Apply overrides by category
        for category, values in overrides.items():
            if category == 'trending' and 'trending' in config.__dict__:
                for key, value in values.items():
                    if hasattr(new_config.trending, key):
                        setattr(new_config.trending, key, value)
            elif category == 'ai_models' and 'ai_models' in config.__dict__:
                for key, value in values.items():
                    if hasattr(new_config.ai_models, key):
                        setattr(new_config.ai_models, key, value)
            elif category == 'agents' and 'agents' in config.__dict__:
                for key, value in values.items():
                    if hasattr(new_config.agents, key):
                        setattr(new_config.agents, key, value)
        
        return new_config
    
    def save_config_to_file(self, config_data: Dict[str, Any]):
        """Save configuration to file.
        
        Args:
            config_data: Configuration data to save
        """
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    def update_database_override(self, category: str, key: str, value: Any):
        """Update a configuration override in database.
        
        Args:
            category: Configuration category
            key: Setting key
            value: New value
        """
        if not self.db_client:
            return
        
        try:
            self.db_client.table('system_settings').upsert({
                'category': category,
                'key': key,
                'value': value,
                'data_type': self._infer_type(value),
                'updated_at': 'NOW()'
            }, on_conflict='key').execute()
            
            # Invalidate cache
            self._cached_config = None
        except Exception as e:
            print(f"Error updating database override: {e}")
    
    def _infer_type(self, value: Any) -> str:
        """Infer data type of a value.
        
        Args:
            value: Value to infer type for
            
        Returns:
            Type string
        """
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'unknown'
    
    def get_trending_config(self) -> TrendingConfig:
        """Get trending configuration.
        
        Returns:
            Trending configuration
        """
        return self.get_config().trending
    
    def get_ai_model_config(self) -> AIModelConfig:
        """Get AI model configuration.
        
        Returns:
            AI model configuration
        """
        return self.get_config().ai_models


# Global instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(db_client: Optional[Client] = None) -> ConfigManager:
    """Get or create global config manager instance.
    
    Args:
        db_client: Optional Supabase client
        
    Returns:
        ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(db_client)
    return _config_manager

