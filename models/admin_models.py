"""Pydantic models for admin configuration system."""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class ModelEnum(str, Enum):
    """Supported LLM models."""
    GPT_4 = "gpt-4-turbo-preview"
    GPT_4O = "gpt-4o"
    GPT_35 = "gpt-3.5-turbo"
    OLLAMA = "ollama"


class SearchDepthEnum(str, Enum):
    """Search depth options."""
    BASIC = "basic"
    ADVANCED = "advanced"


# AI Models Configuration
class AIModelConfig(BaseModel):
    """Configuration for AI models."""
    llm_model: str = Field(default="gpt-4-turbo-preview", description="LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for LLM responses")
    max_tokens: int = Field(default=2000, ge=100, le=4000, description="Maximum tokens per response")
    embeddings_model: str = Field(default="text-embedding-3-small", description="Embeddings model")

    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v

    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        if not 100 <= v <= 4000:
            raise ValueError('Max tokens must be between 100 and 4000')
        return v


# Agent Configuration
class ContentScraperConfig(BaseModel):
    """Configuration for content scraper agent."""
    enabled: bool = Field(default=True, description="Enable content scraper")
    max_search_results: int = Field(default=10, ge=5, le=50, description="Max search results")
    search_depth: str = Field(default="advanced", description="Search depth")

    @validator('search_depth')
    def validate_search_depth(cls, v):
        if v not in ['basic', 'advanced']:
            raise ValueError('Search depth must be basic or advanced')
        return v


class TrendAnalyzerConfig(BaseModel):
    """Configuration for trend analyzer agent."""
    enabled: bool = Field(default=True, description="Enable trend analyzer")
    max_trend_items: int = Field(default=15, ge=5, le=50, description="Max trend items")
    sources: List[str] = Field(default=["github", "linkedin"], description="Trend sources")


class AgentConfig(BaseModel):
    """Configuration for AI agents."""
    content_scraper: ContentScraperConfig
    trend_analyzer: TrendAnalyzerConfig
    content_types: List[str] = Field(
        default=["tutorial", "course", "article", "video", "documentation"],
        description="Content types to retrieve"
    )


# Trending Configuration
class TrendingConfig(BaseModel):
    """Configuration for trending skills algorithm."""
    max_mention_rate: float = Field(default=0.3, ge=0.1, le=1.0, description="Max mention rate assumption")
    min_baseline_score: int = Field(default=50, ge=0, le=100, description="Minimum baseline score")
    trending_threshold: int = Field(default=70, ge=0, le=100, description="Trending threshold")
    mention_weight: float = Field(default=0.5, ge=0.0, le=1.0, description="Weight for mentions")
    github_weight: float = Field(default=0.3, ge=0.0, le=1.0, description="Weight for GitHub")
    linkedin_weight: float = Field(default=0.2, ge=0.0, le=1.0, description="Weight for LinkedIn")
    trend_window_days: int = Field(default=30, ge=7, le=90, description="Trend window in days")
    recency_decay_factor: float = Field(default=0.1, ge=0.0, le=1.0, description="Recency decay factor")

    @validator('mention_weight', 'github_weight', 'linkedin_weight')
    def validate_weights(cls, v, values):
        total = v + values.get('mention_weight', 0) + values.get('github_weight', 0) + values.get('linkedin_weight', 0)
        if not (0.5 <= total <= 1.5):  # Allow flexibility
            raise ValueError('Weights should sum to approximately 1.0')
        return v


# API Endpoints Configuration
class APIEndpointsConfig(BaseModel):
    """Configuration for API endpoints."""
    github_api: str = Field(default="https://api.github.com", description="GitHub API URL")
    tavily_enabled: bool = Field(default=True, description="Enable Tavily search")
    custom_endpoints: Dict[str, str] = Field(default_factory=dict, description="Custom endpoints")


# Database Configuration
class DatabaseConfig(BaseModel):
    """Configuration for database settings."""
    query_timeout: int = Field(default=30, ge=10, le=300, description="Query timeout in seconds")
    max_results: int = Field(default=100, ge=10, le=1000, description="Max query results")
    enable_caching: bool = Field(default=True, description="Enable caching")


# RAG Workflow Configuration
class RAGWorkflowConfig(BaseModel):
    """Configuration for RAG workflow."""
    enable_reasoning: bool = Field(default=True, description="Enable reasoning step")
    enable_refinement: bool = Field(default=True, description="Enable refinement step")
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Confidence threshold")
    max_refinement_iterations: int = Field(default=2, ge=1, le=5, description="Max refinement iterations")
    search_result_limit: int = Field(default=10, ge=5, le=50, description="Search result limit")


# Complete System Configuration
class SystemConfig(BaseModel):
    """Complete system configuration."""
    ai_models: AIModelConfig
    agents: AgentConfig
    trending: TrendingConfig
    api_endpoints: APIEndpointsConfig
    database: DatabaseConfig
    rag_workflow: RAGWorkflowConfig


# API Request/Response Models
class SettingsRequest(BaseModel):
    """Request model for updating settings."""
    category: str
    key: str
    value: Any
    description: Optional[str] = None


class SettingsResponse(BaseModel):
    """Response model for settings."""
    category: str
    key: str
    value: Any
    data_type: str
    updated_at: str
    description: Optional[str] = None


class SettingsByCategoryResponse(BaseModel):
    """Response model for settings grouped by category."""
    category: str
    settings: List[SettingsResponse]


class ValidateConfigResponse(BaseModel):
    """Response model for configuration validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]


class AuditLogEntry(BaseModel):
    """Entry in configuration audit log."""
    id: str
    setting_key: str
    category: str
    old_value: Optional[Any]
    new_value: Any
    changed_by: Optional[str]
    changed_at: str
    change_reason: Optional[str]


class HealthCheckResponse(BaseModel):
    """System health check response."""
    status: str
    database: str
    config_loaded: bool
    agents_status: Dict[str, bool]


# Export all models
__all__ = [
    'AIModelConfig',
    'AgentConfig',
    'TrendingConfig',
    'APIEndpointsConfig',
    'DatabaseConfig',
    'RAGWorkflowConfig',
    'SystemConfig',
    'SettingsRequest',
    'SettingsResponse',
    'SettingsByCategoryResponse',
    'ValidateConfigResponse',
    'AuditLogEntry',
    'HealthCheckResponse',
    'ModelEnum',
    'SearchDepthEnum',
    'ContentScraperConfig',
    'TrendAnalyzerConfig',
]

