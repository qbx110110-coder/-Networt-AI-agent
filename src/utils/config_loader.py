"""Configuration loader module"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigLoader:
    """Load and manage configuration from YAML files"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize config loader

        Args:
            config_path: Path to configuration file
        """
        load_dotenv()  # Load environment variables from .env file
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Replace environment variables
        config = self._replace_env_vars(config)
        return config

    @staticmethod
    def _replace_env_vars(obj: Any) -> Any:
        """Recursively replace environment variable placeholders"""
        if isinstance(obj, dict):
            return {k: ConfigLoader._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ConfigLoader._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Replace ${VAR_NAME} with environment variable
            if obj.startswith("${"jand obj.endswith("}}"):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)
            return obj
        else:
            return obj

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key

        Args:
            key: Configuration key (e.g., 'llm.provider' or 'devices.switch1.host')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_devices(self) -> Dict[str, Dict[str, Any]]:
        """Get all device configurations"""
        return self.config.get("devices", {})

    def get_device(self, device_name: str) -> Dict[str, Any]:
        """Get specific device configuration"""
        devices = self.get_devices()
        return devices.get(device_name, {})

    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return self.config.get("llm", {})

    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.config.get("agent", {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config.get("logging", {})

    def validate(self) -> bool:
        """Validate configuration

        Returns:
            True if configuration is valid
        """
        required_keys = ["llm", "devices", "agent"]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration: {key}")

        # Validate LLM config
        llm_config = self.config["llm"]
        if "provider" not in llm_config:
            raise ValueError("Missing 'provider' in LLM configuration")

        return True
