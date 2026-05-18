"""
Plugin detector for scanning and analyzing installed plugins
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import zipfile

logger = logging.getLogger(__name__)

class PluginInfo:
    """
    Represents information about an installed plugin
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        file_path: str,
        description: Optional[str] = None,
        authors: Optional[List[str]] = None,
        main_class: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self.name = name
        self.version = version
        self.file_path = file_path
        self.description = description
        self.authors = authors or []
        self.main_class = main_class
        self.api_version = api_version
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'version': self.version,
            'file_path': self.file_path,
            'description': self.description,
            'authors': self.authors,
            'main_class': self.main_class,
            'api_version': self.api_version,
        }

class PluginDetector:
    """
    Detects and analyzes plugins in a Minecraft server directory
    """
    
    def __init__(self, plugin_path: str):
        """
        Initialize plugin detector
        
        Args:
            plugin_path: Path to the plugins directory
        """
        self.plugin_path = Path(plugin_path)
        self.plugins: List[PluginInfo] = []
    
    def scan(self) -> List[PluginInfo]:
        """
        Scan plugins directory and detect all plugins
        
        Returns:
            List of detected plugins
        """
        self.plugins = []
        
        if not self.plugin_path.exists():
            logger.warning(f"Plugin path does not exist: {self.plugin_path}")
            return self.plugins
        
        try:
            # Find all JAR files
            jar_files = list(self.plugin_path.glob("*.jar"))
            logger.info(f"Found {len(jar_files)} JAR files in {self.plugin_path}")
            
            for jar_file in jar_files:
                try:
                    plugin_info = self._analyze_jar(jar_file)
                    if plugin_info:
                        self.plugins.append(plugin_info)
                        logger.debug(f"Detected plugin: {plugin_info.name} v{plugin_info.version}")
                except Exception as e:
                    logger.warning(f"Failed to analyze {jar_file.name}: {e}")
            
            logger.info(f"Successfully detected {len(self.plugins)} plugins")
            return self.plugins
        
        except Exception as e:
            logger.error(f"Error scanning plugin directory: {e}")
            return self.plugins
    
    def _analyze_jar(self, jar_path: Path) -> Optional[PluginInfo]:
        """
        Analyze a JAR file and extract plugin information
        
        Args:
            jar_path: Path to the JAR file
            
        Returns:
            PluginInfo or None if analysis fails
        """
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar:
                # Try to read plugin.yml (Bukkit/Spigot/Paper plugins)
                if 'plugin.yml' in jar.namelist():
                    return self._parse_bukkit_plugin(jar, jar_path)
                
                # Try to read fabric.mod.json (Fabric mods)
                if 'fabric.mod.json' in jar.namelist():
                    return self._parse_fabric_mod(jar, jar_path)
                
                # Try to read mcmod.info (Forge mods)
                if 'mcmod.info' in jar.namelist():
                    return self._parse_forge_mod(jar, jar_path)
                
                # Try to read META-INF/MANIFEST.MF for fallback info
                if 'META-INF/MANIFEST.MF' in jar.namelist():
                    return self._parse_manifest(jar, jar_path)
        
        except zipfile.BadZipFile:
            logger.warning(f"{jar_path.name} is not a valid ZIP file")
        except Exception as e:
            logger.error(f"Error analyzing {jar_path.name}: {e}")
        
        return None
    
    def _parse_bukkit_plugin(self, jar: zipfile.ZipFile, jar_path: Path) -> Optional[PluginInfo]:
        """
        Parse Bukkit/Spigot/Paper plugin.yml
        """
        try:
            import yaml
            
            with jar.open('plugin.yml') as f:
                config = yaml.safe_load(f)
            
            if not config or 'name' not in config:
                return None
            
            return PluginInfo(
                name=config.get('name', jar_path.stem),
                version=config.get('version', 'unknown'),
                file_path=str(jar_path),
                description=config.get('description'),
                authors=config.get('authors', []),
                main_class=config.get('main'),
                api_version=config.get('api-version'),
            )
        except Exception as e:
            logger.warning(f"Failed to parse plugin.yml in {jar_path.name}: {e}")
            return None
    
    def _parse_fabric_mod(self, jar: zipfile.ZipFile, jar_path: Path) -> Optional[PluginInfo]:
        """
        Parse Fabric mod fabric.mod.json
        """
        try:
            with jar.open('fabric.mod.json') as f:
                config = json.load(f)
            
            if not config or 'name' not in config:
                return None
            
            return PluginInfo(
                name=config.get('name', jar_path.stem),
                version=config.get('version', 'unknown'),
                file_path=str(jar_path),
                description=config.get('description'),
                authors=[config.get('contact', {}).get('sources', '')],
            )
        except Exception as e:
            logger.warning(f"Failed to parse fabric.mod.json in {jar_path.name}: {e}")
            return None
    
    def _parse_forge_mod(self, jar: zipfile.ZipFile, jar_path: Path) -> Optional[PluginInfo]:
        """
        Parse Forge mod mcmod.info
        """
        try:
            with jar.open('mcmod.info') as f:
                content = f.read().decode('utf-8')
                # mcmod.info is often not valid JSON, try to parse it
                config = json.loads(content)
            
            if isinstance(config, list) and len(config) > 0:
                mod_info = config[0]
            else:
                mod_info = config
            
            if not mod_info or 'name' not in mod_info:
                return None
            
            return PluginInfo(
                name=mod_info.get('name', jar_path.stem),
                version=mod_info.get('version', 'unknown'),
                file_path=str(jar_path),
                description=mod_info.get('description'),
                authors=[mod_info.get('authorList', '')],
            )
        except Exception as e:
            logger.warning(f"Failed to parse mcmod.info in {jar_path.name}: {e}")
            return None
    
    def _parse_manifest(self, jar: zipfile.ZipFile, jar_path: Path) -> Optional[PluginInfo]:
        """
        Fallback: Parse MANIFEST.MF
        """
        try:
            with jar.open('META-INF/MANIFEST.MF') as f:
                manifest = f.read().decode('utf-8')
            
            lines = manifest.split('\n')
            manifest_dict = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    manifest_dict[key.strip()] = value.strip()
            
            name = manifest_dict.get('Implementation-Title', jar_path.stem)
            version = manifest_dict.get('Implementation-Version', 'unknown')
            
            return PluginInfo(
                name=name,
                version=version,
                file_path=str(jar_path),
            )
        except Exception as e:
            logger.warning(f"Failed to parse MANIFEST.MF in {jar_path.name}: {e}")
            return None
    
    def get_plugins(self) -> List[Dict[str, Any]]:
        """
        Get all detected plugins as dictionaries
        
        Returns:
            List of plugin dictionaries
        """
        return [plugin.to_dict() for plugin in self.plugins]
    
    def get_plugin(self, name: str) -> Optional[PluginInfo]:
        """
        Get a specific plugin by name
        
        Args:
            name: Plugin name
            
        Returns:
            PluginInfo or None if not found
        """
        for plugin in self.plugins:
            if plugin.name.lower() == name.lower():
                return plugin
        return None
