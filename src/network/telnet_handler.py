"""Telnet connection handler"""

import socket
import time
import re
from typing import Any, Dict, List, Optional

from .connection import NetworkConnection


class TelnetHandler(NetworkConnection):
    """Telnet connection handler"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize Telnet handler

        Args:
            config: Device configuration dictionary
        """
        super().__init__(config)
        self.socket = None
        self.secret = config.get("secret", "")

    def connect(self) -> bool:
        """Establish Telnet connection to device

        Returns:
            True if connection successful
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))

            # Wait for login prompt
            time.sleep(0.5)
            output = self._recv()

            # Send username
            self.socket.send(f"{self.username}\n".encode())
            time.sleep(0.2)
            output = self._recv()

            # Send password
            self.socket.send(f"{self.password}\n".encode())
            time.sleep(0.5)
            output = self._recv()

            self.connected = True
            return True

        except Exception as e:
            raise ConnectionError(f"Telnet connection failed to {self.host}: {str(e)}")

    def disconnect(self) -> bool:
        """Close Telnet connection

        Returns:
            True if disconnection successful
        """
        try:
            if self.socket:
                self.socket.close()
            self.connected = False
            return True
        except Exception as e:
            raise RuntimeError(f"Telnet disconnection failed: {str(e)}")

    def send_command(self, command: str) -> str:
        """Send command to device via Telnet

        Args:
            command: Command to execute

        Returns:
            Command output
        """
        if not self.connected:
            raise RuntimeError("Not connected to device")

        try:
            # Send command
            self.socket.send(f"{command}\n".encode())
            time.sleep(0.2)

            # Receive response
            output = self._recv()
            return output

        except Exception as e:
            raise RuntimeError(f"Command execution failed: {str(e)}")

    def send_commands(self, commands: List[str]) -> Dict[str, str]:
        """Send multiple commands to device

        Args:
            commands: List of commands to execute

        Returns:
            Dictionary mapping commands to their outputs
        """
        results = {}
        for command in commands:
            try:
                results[command] = self.send_command(command)
            except Exception as e:
                results[command] = f"Error: {str(e)}"

        return results

    def _recv(self, buffer_size: int = 4096) -> str:
        """Receive data from socket

        Args:
            buffer_size: Size of receive buffer

        Returns:
            Received data as string
        """
        try:
            data = self.socket.recv(buffer_size).decode("utf-8", errors="ignore")
            return data
        except socket.timeout:
            return ""
        except Exception as e:
            raise RuntimeError(f"Failed to receive data: {str(e)}")

    def enable_mode(self, enable_password: Optional[str] = None) -> bool:
        """Enter enable mode

        Args:
            enable_password: Enable password (optional)

        Returns:
            True if successful
        """
        try:
            output = self.send_command("enable")

            if enable_password:
                output = self.send_command(enable_password)

            return True
        except Exception as e:
            raise RuntimeError(f"Failed to enter enable mode: {str(e)}")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        if self.connected:
            try:
                self.disconnect()
            except:
                pass
