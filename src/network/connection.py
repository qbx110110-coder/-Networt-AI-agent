"""Network connection base module"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class NetworkConnection(ABC):
    """Abstract base class for network connections"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize network connection

        Args:
            config: Device configuration dictionary
        """
        self.config = config
        self.host = config.get("host")
        self.port = config.get("port", 22)
        self.username = config.get("username")
        self.password = config.get("password")
        self.timeout = config.get("timeout", 30)
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to device

        Returns:
            True if connection successful
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Close connection to device

        Returns:
            True if disconnection successful
        """
        pass

    @abstractmethod
    def send_command(self, command: str) -> str:
        """Send command to device and get response

        Args:
            command: Command to execute

        Returns:
            Command output
        """
        pass

    @abstractmethod
    def send_commands(self, commands: List[str]) -> Dict[str, str]:
        """Send multiple commands to device

        Args:
            commands: List of commands to execute

        Returns:
            Dictionary mapping commands to their outputs
        """
        pass

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
        return False

    def is_connected(self) -> bool:
        """Check if connected to device

        Returns:
            True if connected
        """
        return self.connected
