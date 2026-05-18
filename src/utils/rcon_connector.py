"""
RCON connection handler
"""

import logging
from typing import Optional
from mcrcon import MCRcon

logger = logging.getLogger(__name__)

class RCONConnector:
    """
    Handles RCON communication with Minecraft servers
    """
    
    def __init__(self, host: str, port: int, password: str):
        """
        Initialize RCON connector
        
        Args:
            host: Server host/IP
            port: RCON port
            password: RCON password
        """
        self.host = host
        self.port = port
        self.password = password
        self.rcon: Optional[MCRcon] = None
    
    def connect(self) -> bool:
        """
        Connect to RCON
        
        Returns:
            True if connection successful
        """
        try:
            self.rcon = MCRcon(self.host, self.password, self.port)
            self.rcon.connect()
            logger.info(f"Connected to RCON: {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to RCON: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from RCON
        
        Returns:
            True if disconnection successful
        """
        try:
            if self.rcon:
                self.rcon.disconnect()
                logger.info("Disconnected from RCON")
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect from RCON: {e}")
            return False
    
    def send_command(self, command: str) -> Optional[str]:
        """
        Send command to server
        
        Args:
            command: Command to send (without leading /)
            
        Returns:
            Server response or None if error
        """
        try:
            if not self.rcon:
                if not self.connect():
                    return None
            
            response = self.rcon.command(command)
            logger.debug(f"RCON command '{command}' response: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send RCON command: {e}")
            return None
    
    def broadcast(self, message: str) -> bool:
        """
        Send broadcast message to all players
        
        Args:
            message: Message to broadcast
            
        Returns:
            True if successful
        """
        try:
            self.send_command(f"say {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
            return False
    
    def stop_server(self) -> bool:
        """
        Stop the server
        
        Returns:
            True if command sent successfully
        """
        try:
            self.send_command("stop")
            logger.info("Server stop command sent")
            return True
        except Exception as e:
            logger.error(f"Failed to stop server: {e}")
            return False
    
    def restart_server(self, warning_minutes: int = 5) -> bool:
        """
        Restart the server with warning message
        
        Args:
            warning_minutes: Minutes before restart
            
        Returns:
            True if command sent successfully
        """
        try:
            self.broadcast(f"⚠️ Server will restart in {warning_minutes} minutes for plugin updates.")
            self.send_command("stop")
            logger.info("Server restart sequence initiated")
            return True
        except Exception as e:
            logger.error(f"Failed to restart server: {e}")
            return False
