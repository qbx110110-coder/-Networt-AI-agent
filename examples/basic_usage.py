"""Basic usage example for Network AI Agent"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.network_agent import NetworkAgent


def main():
    """Basic usage example"""

    # Initialize agent
    agent = NetworkAgent(config_path="config/config.yaml")

    # Example 1: Simple configuration request
    print("Example 1: Configure VLAN")
    print("-" * 40)
    result = agent.execute("Configure VLAN 100 named VLAN-100", device_name="switch1")
    print(f"Status: {result['status']}")
    print(f"Commands: {result.get('commands', {}).get('commands', [])}")
    print()

    # Example 2: Multiple commands
    print("Example 2: Port Configuration")
    print("-" * 40)
    result = agent.execute(
        "Configure interface Gi0/0/1 as access port for VLAN 100",
        device_name="switch1",
    )
    print(f"Status: {result['status']}")
    print()

    # Example 3: Get device status
    print("Example 3: Device Status")
    print("-" * 40)
    status = agent.get_device_status()
    print(f"Device statuses: {status}")
    print()

    # Cleanup
    agent.device_manager.close_all_connections()


if __name__ == "__main__":
    main()
