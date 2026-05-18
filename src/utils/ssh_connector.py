"""
SSH connection handler for remote servers
"""

import logging
from typing import Optional
import paramiko
from pathlib import Path

logger = logging.getLogger(__name__)

class SSHConnector:
    """
    Handles SSH connections to remote servers
    """
    
    def __init__(
        self,
        host: str,
        username: str,
        password: Optional[str] = None,
        key_path: Optional[str] = None,
        port: int = 22
    ):
        """
        Initialize SSH connector
        
        Args:
            host: Server host/IP
            username: SSH username
            password: SSH password (optional if using key)
            key_path: Path to private key (optional)
            port: SSH port (default: 22)
        """
        self.host = host
        self.username = username
        self.password = password
        self.key_path = key_path
        self.port = port
        self.client: Optional[paramiko.SSHClient] = None
    
    def connect(self) -> bool:
        """
        Connect to remote server via SSH
        
        Returns:
            True if connection successful
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_path:
                # Connect with private key
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                self.client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    pkey=key
                )
            else:
                # Connect with password
                self.client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password
                )
            
            logger.info(f"Connected to SSH: {self.username}@{self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SSH: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from remote server
        
        Returns:
            True if disconnection successful
        """
        try:
            if self.client:
                self.client.close()
                logger.info("Disconnected from SSH")
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect from SSH: {e}")
            return False
    
    def execute_command(self, command: str) -> Optional[str]:
        """
        Execute command on remote server
        
        Args:
            command: Command to execute
            
        Returns:
            Command output or None if error
        """
        try:
            if not self.client:
                if not self.connect():
                    return None
            
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if error:
                logger.error(f"Command error: {error}")
            
            return output
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return None
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        Upload file to remote server
        
        Args:
            local_path: Local file path
            remote_path: Remote file path
            
        Returns:
            True if successful
        """
        try:
            if not self.client:
                if not self.connect():
                    return False
            
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            logger.info(f"Uploaded {local_path} to {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """
        Download file from remote server
        
        Args:
            remote_path: Remote file path
            local_path: Local file path
            
        Returns:
            True if successful
        """
        try:
            if not self.client:
                if not self.connect():
                    return False
            
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            
            logger.info(f"Downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            return False
