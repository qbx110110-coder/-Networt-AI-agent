"""SSH connection handler"""

import paramiko
from typing import Any, Dict, List, Optional
import time

from .connection import NetworkConnection


class SSHHandler(NetworkConnection):
    """SSH connection handler using paramiko"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize SSH handler

        Args:
            config: Device configuration dictionary
        """
        super().__init__(config)
        self.ssh_client = None
        self.shell = None
        self.secret = config.get("secret", "")

    def connect(self) -> bool:
        """Establish SSH connection to device

        Returns:
            True if connection successful
        """
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to device
            self.ssh_client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False,
            )

            # Open interactive shell
            self.shell = self.ssh_client.invoke_shell()
            self.shell.settimeout(self.timeout)

            # Clear initial banner
            time.sleep(0.5)
            _ = self.shell.recv(4096)

            self.connected = True
            return True

        except Exception as e:
            raise ConnectionError(f"SSH connection failed to {self.host}: {str(e)}")

    def disconnect(self) -> bool:
        """Close SSH connection

        Returns:
            True if disconnection successful
        """
        try:
            if self.shell:
                self.shell.close()
            if self.ssh_client:
                self.ssh_client.close()
            self.connected = False
            return True
        except Exception as e:
            raise RuntimeError(f"SSH disconnection failed: {str(e)}")

    def send_command(self, command: str) -> str:
        """Send command to device via SSH

        Args:
            command: Command to execute

        Returns:
            Command output
        """
        if not self.connected:
            raise RuntimeError("Not connected to device")

        try:
            # Send command
            self.shell.send(command + "\n")
            time.sleep(0.2)

            # Receive response
            output = ""
            while True:
                try:
                    chunk = self.shell.recv(4096).decode("utf-8", errors="ignore")
                    if not chunk:
                        break
                    output += chunk
                except:
                    break

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
