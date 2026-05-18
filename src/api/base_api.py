"""
Base API class for plugin repositories
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PluginInfo:
    """
    Represents plugin information from a repository
    """
    
    def __init__(
        self,
        name: str,
        current_version: str,
        latest_version: str,
        source: str,
        source_id: str,
        download_url: Optional[str] = None,
        description: Optional[str] = None,
        supported_versions: Optional[List[str]] = None,
        changelog: Optional[str] = None
    ):
        self.name = name
        self.current_version = current_version
        self.latest_version = latest_version
        self.source = source
        self.source_id = source_id
        self.download_url = download_url
        self.description = description
        self.supported_versions = supported_versions or []
        self.changelog = changelog
    
    def has_update(self) -> bool:
        """Check if update is available"""
        return self.current_version != self.latest_version
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'current_version': self.current_version,
            'latest_version': self.latest_version,
            'source': self.source,
            'source_id': self.source_id,
            'download_url': self.download_url,
            'description': self.description,
            'supported_versions': self.supported_versions,
            'changelog': self.changelog,
            'has_update': self.has_update()
        }

class BaseAPI(ABC):
    """
    Abstract base class for plugin repository APIs
    """
    
    def __init__(self):
        self.name = "BaseAPI"
        self.base_url = ""
    
    @abstractmethod
    async def search(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a plugin by name
        
        Args:
            plugin_name: Name of the plugin to search
            
        Returns:
            Plugin information or None if not found
        """
        pass
    
    @abstractmethod
    async def get_plugin_info(
        self,
        plugin_id: str,
        minecraft_version: str
    ) -> Optional[PluginInfo]:
        """
        Get plugin information
        
        Args:
            plugin_id: ID of the plugin in the repository
            minecraft_version: Target Minecraft version
            
        Returns:
            PluginInfo or None if not found
        """
        pass
    
    @abstractmethod
    async def download(self, download_url: str, save_path: str) -> bool:
        """
        Download plugin file
        
        Args:
            download_url: URL to download from
            save_path: Path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    def is_version_compatible(
        self,
        target_version: str,
        supported_versions: List[str]
    ) -> bool:
        """
        Check if target version is compatible with supported versions
        
        Args:
            target_version: Target Minecraft version
            supported_versions: List of supported versions (e.g., ["1.20+"])
            
        Returns:
            True if compatible, False otherwise
        """
        # TODO: Implement proper version comparison
        for supported in supported_versions:
            if target_version in supported or supported.endswith("+"):
                return True
        return False
