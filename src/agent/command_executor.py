"""Command executor module for executing network commands"""

from typing import Any, Dict, List, Optional
from src.utils.logger import Logger
from src.network.device_manager import DeviceManager


class CommandExecutor:
    """Executes network commands with validation and safety checks"""

    def __init__(self, device_manager: DeviceManager, config: Dict[str, Any]):
        """Initialize command executor

        Args:
            device_manager: DeviceManager instance
            config: Agent configuration
        """
        self.logger = Logger.get_logger("CommandExecutor")
        self.device_manager = device_manager
        self.config = config

        # Safety configuration
        self.dry_run = config.get("dry_run", True)
        self.allow_config_changes = config.get("allow_config_changes", True)
        self.allow_reboot = config.get("allow_reboot", False)
        self.validate_commands = config.get("validate_commands", True)
        self.forbidden_keywords = config.get("forbidden_keywords", [])

    def validate_command(self, command: str) -> tuple:
        """Validate command for safety and syntax

        Args:
            command: Command to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        command_lower = command.lower()

        # Check for forbidden keywords
        for keyword in self.forbidden_keywords:
            if keyword.lower() in command_lower:
                return False, f"Command contains forbidden keyword: {keyword}"

        # Check for potentially dangerous commands
        dangerous_patterns = ["erase", "delete", "reload", "shutdown", "reset"]
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                if not self.allow_reboot:
                    return False, f"Dangerous command not allowed: {pattern}"

        return True, None

    def execute_command(
        self,
        device_name: str,
        command: str,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Execute a single command on a device

        Args:
            device_name: Target device name
            command: Command to execute
            validate: Whether to validate command first

        Returns:
            Dictionary with execution results
        """
        # Validate command if enabled
        if validate and self.validate_commands:
            is_valid, error = self.validate_command(command)
            if not is_valid:
                return {
                    "status": "failed",
                    "device": device_name,
                    "command": command,
                    "error": error,
                    "output": None,
                }

        # Dry run mode
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would execute on {device_name}: {command}")
            return {
                "status": "dry_run",
                "device": device_name,
                "command": command,
                "output": "[DRY RUN] Command not executed",
            }

        # Execute command
        try:
            output = self.device_manager.send_command(device_name, command)
            self.logger.info(f"Command executed on {device_name}")

            return {
                "status": "success",
                "device": device_name,
                "command": command,
                "output": output,
            }

        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return {
                "status": "failed",
                "device": device_name,
                "command": command,
                "error": str(e),
                "output": None,
            }

    def execute_commands(
        self,
        device_name: str,
        commands: List[str],
        validate: bool = True,
    ) -> List[Dict[str, Any]]:
        """Execute multiple commands on a device

        Args:
            device_name: Target device name
            commands: List of commands to execute
            validate: Whether to validate commands first

        Returns:
            List of execution results
        """
        results = []
        for command in commands:
            result = self.execute_command(device_name, command, validate)
            results.append(result)

            # Stop on first failure in strict mode
            if result["status"] == "failed":
                self.logger.warning(f"Stopping execution due to command failure")
                break

        return results

    def execute_batch(
        self,
        batch_config: Dict[str, List[str]],
        validate: bool = True,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Execute commands on multiple devices

        Args:
            batch_config: Dictionary mapping device names to command lists
            validate: Whether to validate commands first

        Returns:
            Dictionary mapping device names to execution results
        """
        results = {}

        for device_name, commands in batch_config.items():
            try:
                device_results = self.execute_commands(device_name, commands, validate)
                results[device_name] = device_results
            except Exception as e:
                self.logger.error(f"Batch execution failed for {device_name}: {str(e)}")
                results[device_name] = [
                    {
                        "status": "failed",
                        "device": device_name,
                        "command": None,
                        "error": str(e),
                        "output": None,
                    }
                ]

        return results

    def parse_response(self, command_output: str) -> Dict[str, Any]:
        """Parse command output

        Args:
            command_output: Raw command output

        Returns:
            Parsed output dictionary
        """
        return {
            "raw": command_output,
            "lines": command_output.split("\n"),
            "error": any(
                keyword in command_output.lower()
                for keyword in ["error", "invalid", "unknown command"]
            ),
        }

    def enable_dry_run_mode(self):
        """Enable dry run mode (no actual commands executed)"""
        self.dry_run = True
        self.logger.info("Dry run mode enabled")

    def disable_dry_run_mode(self):
        """Disable dry run mode (execute actual commands)"""
        self.dry_run = False
        self.logger.warning("Dry run mode disabled - actual commands will be executed")
