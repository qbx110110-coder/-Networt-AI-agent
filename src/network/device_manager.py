"""Device manager for handling multiple network devices"""

from typing import Any, Dict, List, Optional
from .ssh_handler import SSHHandler
from .telnet_handler import TelnetHandler
from .connection import NetworkConnection
from src.utils.logger import Logger


class DeviceManager:
    """Manages connections to multiple network devices"""

    def __init__(self, devices_config: Dict[str, Dict[str, Any]]):
        """Initialize device manager

        Args:
            devices_config: Dictionary of device configurations
        """
        self.logger = Logger.get_logger("DeviceManager")
        self.devices_config = devices_config
        self.connections: Dict[str, NetworkConnection] = {}

    def get_connection(self, device_name: str) -> NetworkConnection:
        """Get or create connection to device

        Args:
            device_name: Name of the device

        Returns:
            NetworkConnection instance
        """
        # Return existing connection if available
        if device_name in self.connections:
            conn = self.connections[device_name]
            if conn.is_connected():
                return conn

        # Get device configuration
        if device_name not in self.devices_config:
            raise ValueError(f"Device not found: {device_name}")

        device_config = self.devices_config[device_name]

        # Check if device is enabled
        if not device_config.get("enabled", True):
            raise RuntimeError(f"Device is disabled: {device_name}")

        # Create appropriate connection handler
        protocol = device_config.get("protocol", "ssh").lower()

        if protocol == "ssh":
            conn = SSHHandler(device_config)
        elif protocol == "telnet":
            conn = TelnetHandler(device_config)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")

        # Connect to device
        try:
            conn.connect()
            self.connections[device_name] = conn
            self.logger.info(f"Connected to {device_name} via {protocol.upper()}")
            return conn
        except Exception as e:
            self.logger.error(f"Failed to connect to {device_name}: {str(e)}")
            raise

    def send_command(self, device_name: str, command: str) -> str:
        """Send command to device

        Args:
            device_name: Name of the device
            command: Command to execute

        Returns:
            Command output
        """
        conn = self.get_connection(device_name)
        return conn.send_command(command)

    def send_commands(self, device_name: str, commands: List[str]) -> Dict[str, str]:
        """Send multiple commands to device

        Args:
            device_name: Name of the device
            commands: List of commands

        Returns:
            Dictionary mapping commands to outputs
        """
        conn = self.get_connection(device_name)
        return conn.send_commands(commands)

    def broadcast_command(self, command: str, devices: Optional[List[str]] = None) -> Dict[str, str]:
        """Send same command to multiple devices

        Args:
            command: Command to execute
            devices: List of device names (None = all)

        Returns:
            Dictionary mapping device names to outputs
        """
        target_devices = devices or list(self.devices_config.keys())
        results = {}

        for device_name in target_devices:
            try:
                output = self.send_command(device_name, command)
                results[device_name] = output
                self.logger.info(f"Command sent to {device_name}")
            except Exception as e:
                results[device_name] = f"Error: {str(e)}"
                self.logger.error(f"Failed to send command to {device_name}: {str(e)}")

        return results

    def close_connection(self, device_name: str) -> bool:
        """Close connection to device

        Args:
            device_name: Name of the device

        Returns:
            True if successful
        """
        if device_name in self.connections:
            try:
                self.connections[device_name].disconnect()
                del self.connections[device_name]
                self.logger.info(f"Disconnected from {device_name}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to disconnect from {device_name}: {str(e)}")
                return False
        return False

    def close_all_connections(self) -> bool:
        """Close all device connections

        Returns:
            True if all closed successfully
        """
        success = True
        for device_name in list(self.connections.keys()):
            if not self.close_connection(device_name):
                success = False
        return success

    def get_device_status(self, device_name: str) -> Dict[str, Any]:
        """Get device connection status

        Args:
            device_name: Name of the device

        Returns:
            Device status dictionary
        """
        if device_name not in self.devices_config:
            return {"status": "not_found"}

        config = self.devices_config[device_name]
        is_connected = (
            device_name in self.connections and self.connections[device_name].is_connected()
        )

        return {
            "name": device_name,
            "host": config.get("host"),
            "protocol": config.get("protocol", "ssh"),
            "enabled": config.get("enabled", True),
            "connected": is_connected,
        }

    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all devices

        Returns:
            Dictionary mapping device names to their statuses
        """
        return {
            device_name: self.get_device_status(device_name)
            for device_name in self.devices_config.keys()
        }

    def __del__(self):
        """Destructor to ensure all connections are closed"""
        try:
            self.close_all_connections()
        except:
            pass
