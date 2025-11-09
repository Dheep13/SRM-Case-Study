"""Agent Access Control System for University Administration."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

class AccessLevel(Enum):
    """Access control levels."""
    BLOCKED = "blocked"
    RESTRICTED = "restricted"  # Limited access
    ALLOWED = "allowed"       # Full access

@dataclass
class PlatformConfig:
    """Configuration for a specific platform."""
    name: str
    domain: str
    access_level: AccessLevel
    api_endpoints: List[str]
    rate_limit: Optional[int] = None  # requests per hour
    allowed_content_types: List[str] = None
    blocked_keywords: List[str] = None

@dataclass
class AgentConfig:
    """Configuration for agent access control."""
    agent_name: str
    enabled: bool
    allowed_platforms: List[str]
    max_search_results: int
    timeout_seconds: int
    require_approval: bool = False

class AgentAccessController:
    """Central controller for managing agent access to external sources."""
    
    def __init__(self):
        """Initialize with default configurations."""
        self.platforms = self._load_default_platforms()
        self.agents = self._load_default_agents()
        self.audit_log = []
    
    def _load_default_platforms(self) -> Dict[str, PlatformConfig]:
        """Load default platform configurations."""
        return {
            "github": PlatformConfig(
                name="GitHub",
                domain="api.github.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=[
                    "https://api.github.com/search/repositories",
                    "https://api.github.com/search/topics"
                ],
                rate_limit=5000,
                allowed_content_types=["repositories", "topics"],
                blocked_keywords=["private", "internal"]
            ),
            "tavily": PlatformConfig(
                name="Tavily Search",
                domain="api.tavily.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://api.tavily.com/search"],
                rate_limit=1000,
                allowed_content_types=["web", "news"],
                blocked_keywords=["adult", "gambling", "illegal"]
            ),
            "coursera": PlatformConfig(
                name="Coursera",
                domain="coursera.org",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://www.coursera.org/search"],
                rate_limit=100,
                allowed_content_types=["courses", "specializations"],
                blocked_keywords=[]
            ),
            "udemy": PlatformConfig(
                name="Udemy",
                domain="udemy.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://www.udemy.com/courses/search"],
                rate_limit=100,
                allowed_content_types=["courses"],
                blocked_keywords=[]
            ),
            "microsoft": PlatformConfig(
                name="Microsoft Learn",
                domain="learn.microsoft.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://learn.microsoft.com/en-us/search"],
                rate_limit=200,
                allowed_content_types=["documentation", "courses"],
                blocked_keywords=[]
            ),
            "openai": PlatformConfig(
                name="OpenAI",
                domain="platform.openai.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://platform.openai.com/docs"],
                rate_limit=1000,
                allowed_content_types=["documentation"],
                blocked_keywords=[]
            ),
            "langchain": PlatformConfig(
                name="LangChain",
                domain="python.langchain.com",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://python.langchain.com/docs"],
                rate_limit=500,
                allowed_content_types=["documentation"],
                blocked_keywords=[]
            ),
            "huggingface": PlatformConfig(
                name="Hugging Face",
                domain="huggingface.co",
                access_level=AccessLevel.ALLOWED,
                api_endpoints=["https://huggingface.co/learn"],
                rate_limit=500,
                allowed_content_types=["courses", "models"],
                blocked_keywords=[]
            ),
            "linkedin": PlatformConfig(
                name="LinkedIn",
                domain="linkedin.com",
                access_level=AccessLevel.RESTRICTED,
                api_endpoints=["https://www.linkedin.com/search"],
                rate_limit=50,
                allowed_content_types=["professional_posts"],
                blocked_keywords=["personal", "private"]
            ),
            "reddit": PlatformConfig(
                name="Reddit",
                domain="reddit.com",
                access_level=AccessLevel.BLOCKED,
                api_endpoints=[],
                rate_limit=0,
                allowed_content_types=[],
                blocked_keywords=["all"]
            ),
            "twitter": PlatformConfig(
                name="Twitter/X",
                domain="twitter.com",
                access_level=AccessLevel.BLOCKED,
                api_endpoints=[],
                rate_limit=0,
                allowed_content_types=[],
                blocked_keywords=["all"]
            )
        }
    
    def _load_default_agents(self) -> Dict[str, AgentConfig]:
        """Load default agent configurations."""
        return {
            "content_scraper": AgentConfig(
                agent_name="Content Scraper Agent",
                enabled=True,
                allowed_platforms=["tavily", "coursera", "udemy", "microsoft", "openai", "langchain", "huggingface"],
                max_search_results=10,
                timeout_seconds=30
            ),
            "trend_analysis": AgentConfig(
                agent_name="Trend Analysis Agent",
                enabled=True,
                allowed_platforms=["github", "linkedin"],
                max_search_results=15,
                timeout_seconds=20
            ),
            "orchestrator": AgentConfig(
                agent_name="Orchestrator Agent",
                enabled=True,
                allowed_platforms=["content_scraper", "trend_analysis"],
                max_search_results=25,
                timeout_seconds=60
            )
        }
    
    def check_access(self, agent_name: str, platform: str, endpoint: str, content_type: str = None) -> bool:
        """Check if an agent can access a specific platform endpoint."""
        # Check if agent is enabled
        if agent_name not in self.agents or not self.agents[agent_name].enabled:
            self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
            return False
        
        # Check if platform is allowed for this agent
        if platform not in self.agents[agent_name].allowed_platforms:
            self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
            return False
        
        # Check platform access level
        if platform not in self.platforms:
            self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
            return False
        
        platform_config = self.platforms[platform]
        
        if platform_config.access_level == AccessLevel.BLOCKED:
            self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
            return False
        
        # Check if endpoint is allowed
        if endpoint not in platform_config.api_endpoints:
            self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
            return False
        
        # Check content type restrictions
        if content_type and platform_config.allowed_content_types:
            if content_type not in platform_config.allowed_content_types:
                self._log_access_attempt(agent_name, platform, endpoint, content_type, False)
                return False
        
        # Log successful access
        self._log_access_attempt(agent_name, platform, endpoint, content_type, True)
        return True
    
    def get_allowed_platforms(self, agent_name: str) -> List[str]:
        """Get list of allowed platforms for an agent."""
        if agent_name not in self.agents:
            return []
        
        return self.agents[agent_name].allowed_platforms
    
    def update_platform_access(self, platform: str, access_level: AccessLevel, 
                             blocked_keywords: List[str] = None) -> bool:
        """Update platform access level."""
        if platform not in self.platforms:
            return False
        
        self.platforms[platform].access_level = access_level
        if blocked_keywords:
            self.platforms[platform].blocked_keywords = blocked_keywords
        
        self._log_config_change(f"Updated {platform} access to {access_level.value}")
        return True
    
    def update_agent_config(self, agent_name: str, enabled: bool = None,
                           allowed_platforms: List[str] = None,
                           max_search_results: int = None) -> bool:
        """Update agent configuration."""
        if agent_name not in self.agents:
            return False
        
        if enabled is not None:
            self.agents[agent_name].enabled = enabled
        
        if allowed_platforms is not None:
            self.agents[agent_name].allowed_platforms = allowed_platforms
        
        if max_search_results is not None:
            self.agents[agent_name].max_search_results = max_search_results
        
        self._log_config_change(f"Updated {agent_name} configuration")
        return True
    
    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log of access attempts and configuration changes."""
        return self.audit_log[-limit:]
    
    def _log_access_attempt(self, agent_name: str, platform: str, endpoint: str, content_type: str, allowed: bool):
        """Log an access attempt."""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "access_attempt",
            "agent": agent_name,
            "platform": platform,
            "endpoint": endpoint,
            "content_type": content_type,
            "allowed": allowed
        })
    
    def _log_config_change(self, description: str):
        """Log a configuration change."""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "config_change",
            "description": description
        })
    
    def export_config(self) -> Dict[str, Any]:
        """Export current configuration."""
        return {
            "platforms": {
                name: {
                    "name": config.name,
                    "domain": config.domain,
                    "access_level": config.access_level.value,
                    "api_endpoints": config.api_endpoints,
                    "rate_limit": config.rate_limit,
                    "allowed_content_types": config.allowed_content_types,
                    "blocked_keywords": config.blocked_keywords
                }
                for name, config in self.platforms.items()
            },
            "agents": {
                name: {
                    "agent_name": config.agent_name,
                    "enabled": config.enabled,
                    "allowed_platforms": config.allowed_platforms,
                    "max_search_results": config.max_search_results,
                    "timeout_seconds": config.timeout_seconds,
                    "require_approval": config.require_approval
                }
                for name, config in self.agents.items()
            }
        }
    
    def import_config(self, config_data: Dict[str, Any]) -> bool:
        """Import configuration from external source."""
        try:
            # Update platforms
            if "platforms" in config_data:
                for name, data in config_data["platforms"].items():
                    self.platforms[name] = PlatformConfig(
                        name=data["name"],
                        domain=data["domain"],
                        access_level=AccessLevel(data["access_level"]),
                        api_endpoints=data["api_endpoints"],
                        rate_limit=data.get("rate_limit"),
                        allowed_content_types=data.get("allowed_content_types"),
                        blocked_keywords=data.get("blocked_keywords")
                    )
            
            # Update agents
            if "agents" in config_data:
                for name, data in config_data["agents"].items():
                    self.agents[name] = AgentConfig(
                        agent_name=data["agent_name"],
                        enabled=data["enabled"],
                        allowed_platforms=data["allowed_platforms"],
                        max_search_results=data["max_search_results"],
                        timeout_seconds=data["timeout_seconds"],
                        require_approval=data.get("require_approval", False)
                    )
            
            self._log_config_change("Configuration imported successfully")
            return True
        except Exception as e:
            self._log_config_change(f"Configuration import failed: {str(e)}")
            return False

# Global instance
access_controller = AgentAccessController()
