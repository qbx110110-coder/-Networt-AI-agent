"""Network AI Agent for intelligent network device management"""

from typing import Any, Dict, List, Optional
import json
import re

from src.utils.logger import Logger
from src.utils.config_loader import ConfigLoader
from src.llm.openai_client import OpenAIClient
from src.network.device_manager import DeviceManager
from src.agent.command_executor import CommandExecutor
from src.prompts.system_prompts import NETWORK_AGENT_SYSTEM_PROMPT


class NetworkAgent:
    """Intelligent Network AI Agent for device configuration and management"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize Network Agent

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config_loader = ConfigLoader(config_path)
        self.config_loader.validate()

        # Initialize logging
        logging_config = self.config_loader.get_logging_config()
        self.logger = Logger.setup(
            "NetworkAgent",
            level=logging_config.get("level", "INFO"),
            log_file=logging_config.get("file", "logs/network_agent.log"),
        )

        # Initialize LLM
        llm_config = self.config_loader.get_llm_config()
        provider = llm_config.get("provider", "openai")

        if provider == "openai":
            self.llm = OpenAIClient(llm_config.get("openai", llm_config))
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        # Initialize device manager
        devices_config = self.config_loader.get_devices()
        self.device_manager = DeviceManager(devices_config)

        # Initialize command executor
        agent_config = self.config_loader.get_agent_config()
        self.executor = CommandExecutor(self.device_manager, agent_config)

        # Message history for multi-turn conversation
        self.conversation_history: List[Dict[str, str]] = []

        self.logger.info("Network AI Agent initialized successfully")

    def execute(
        self,
        user_request: str,
        device_name: Optional[str] = None,
        dry_run: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Execute user request

        Args:
            user_request: Natural language request
            device_name: Specific device to target (optional)
            dry_run: Override dry run setting (optional)

        Returns:
            Execution result dictionary
        """
        self.logger.info(f"Processing request: {user_request}")

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_request})

        try:
            # Parse user request with LLM
            parsed = self._parse_request(user_request, device_name)
            self.logger.info(f"Parsed request: {parsed}")

            # Generate commands
            commands = self._generate_commands(parsed, user_request)
            self.logger.info(f"Generated commands: {commands}")

            # Validate commands
            validated = self._validate_commands(commands)
            self.logger.info(f"Validation result: {validated}")

            if not validated["valid"]:
                return {
                    "status": "failed",
                    "error": "Command validation failed",
                    "details": validated["errors"],
                }

            # Execute commands
            target_device = parsed.get("device") or device_name
            if not target_device:
                return {
                    "status": "failed",
                    "error": "No target device specified",
                }

            # Set dry run mode if specified
            if dry_run is not None:
                if dry_run:
                    self.executor.enable_dry_run_mode()
                else:
                    self.executor.disable_dry_run_mode()

            results = self.executor.execute_commands(target_device, commands["commands"])

            # Prepare response
            response = {
                "status": "success" if all(r["status"] != "failed" for r in results) else "partial",
                "request": user_request,
                "device": target_device,
                "commands": commands,
                "validation": validated,
                "results": results,
            }

            # Add to conversation history
            self.conversation_history.append(
                {
                    "role": "assistant",
                    "content": json.dumps(response),
                }
            )

            return response

        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "request": user_request,
            }

    def execute_batch(self, requests: List[str]) -> List[Dict[str, Any]]:
        """Execute multiple requests

        Args:
            requests: List of natural language requests

        Returns:
            List of execution results
        """
        results = []
        for request in requests:
            result = self.execute(request)
            results.append(result)

        return results

    def get_device_status(self, device_name: Optional[str] = None) -> Dict[str, Any]:
        """Get device status

        Args:
            device_name: Specific device (None = all)

        Returns:
            Device status information
        """
        if device_name:
            return self.device_manager.get_device_status(device_name)
        else:
            return self.device_manager.get_all_statuses()

    def _parse_request(self, user_request: str, device_name: Optional[str] = None) -> Dict[str, Any]:
        """Parse user request to extract intent and parameters

        Args:
            user_request: Natural language request
            device_name: Optional device name override

        Returns:
            Parsed request dictionary
        """
        prompt = f"""Analyze this network configuration request and extract:
1. The intent/action (configure, modify, query, etc.)
2. Target device (if mentioned)
3. Configuration parameters
4. Device type needed

Request: {user_request}

Respond in JSON format:
{{
    "intent": "string",
    "action": "string",
    "device": "string or null",
    "parameters": {{}},
    "device_type": "string"
}}"""

        try:
            response = self.llm.generate(prompt)
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                if device_name:
                    parsed["device"] = device_name
                return parsed
        except Exception as e:
            self.logger.warning(f"Failed to parse request with LLM: {str(e)}")

        # Fallback parsing
        return {
            "intent": "unknown",
            "action": "unknown",
            "device": device_name,
            "parameters": {},
            "device_type": "cisco_ios",
        }

    def _generate_commands(self, parsed_request: Dict[str, Any], user_request: str) -> Dict[str, Any]:
        """Generate network commands from parsed request

        Args:
            parsed_request: Parsed request dictionary
            user_request: Original user request

        Returns:
            Generated commands dictionary
        """
        prompt = f"""{NETWORK_AGENT_SYSTEM_PROMPT}

User Request: {user_request}

Intent: {parsed_request.get('intent')}
Device Type: {parsed_request.get('device_type')}
Parameters: {json.dumps(parsed_request.get('parameters', {}))}

Generate the appropriate network commands. Format your response as JSON:
{{
    "commands": ["command1", "command2", ...],
    "explanation": "string",
    "warnings": ["warning1", ...]
}}"""

        try:
            response = self.llm.generate(prompt)
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            self.logger.warning(f"Failed to generate commands: {str(e)}")

        return {
            "commands": [],
            "explanation": "Failed to generate commands",
            "warnings": ["Could not parse LLM response"],
        }

    def _validate_commands(self, commands_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated commands

        Args:
            commands_dict: Commands dictionary

        Returns:
            Validation result
        """
        commands = commands_dict.get("commands", [])

        if not commands:
            return {
                "valid": False,
                "errors": ["No commands to validate"],
            }

        errors = []
        for command in commands:
            is_valid, error = self.executor.validate_command(command)
            if not is_valid:
                errors.append(f"{command}: {error}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "commands_checked": len(commands),
        }

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history

        Returns:
            Conversation history
        """
        return self.conversation_history

    def __del__(self):
        """Cleanup on agent destruction"""
        try:
            self.device_manager.close_all_connections()
        except:
            pass
