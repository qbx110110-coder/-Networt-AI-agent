"""Advanced usage examples for Network AI Agent"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.network_agent import NetworkAgent


def main():
    """Advanced usage examples"""

    # Initialize agent
    agent = NetworkAgent(config_path="config/config.yaml")

    # Example 1: Batch configuration on multiple devices
    print("Example 1: Batch Configuration")
    print("-" * 40)
    requests = [
        "Enable spanning tree on switch1",
        "Configure VLAN 200 on switch1",
        "Add interface Gi0/0/5 to VLAN 200",
    ]

    results = agent.execute_batch(requests)
    for i, result in enumerate(results):
        print(f"Request {i+1}: {result['status']}")

    print()

    # Example 2: Complex configuration workflow
    print("Example 2: Complex Configuration Workflow")
    print("-" * 40)

    # Step 1: Create VLAN
    result1 = agent.execute(
        "Create VLAN 300 named PRODUCTION",
        device_name="switch1",
        dry_run=True,  # Use dry run for safety
    )
    print(f"Step 1 - Create VLAN: {result1['status']}")

    # Step 2: Configure ports
    result2 = agent.execute(
        "Configure ports 1-10 as access ports in VLAN 300",
        device_name="switch1",
        dry_run=True,
    )
    print(f"Step 2 - Configure ports: {result2['status']}")

    # Step 3: Save configuration
    result3 = agent.execute(
        "Save running configuration to startup config",
        device_name="switch1",
        dry_run=True,
    )
    print(f"Step 3 - Save config: {result3['status']}")

    print()

    # Example 3: Configuration with validation
    print("Example 3: Configuration with Validation")
    print("-" * 40)

    # Get device status first
    status = agent.get_device_status("switch1")
    print(f"Current device status: {status}")

    # Execute configuration with dry run
    result = agent.execute(
        "Enable port 24 and make it a trunk port",
        device_name="switch1",
        dry_run=True,  # Safety first!
    )

    print(f"Validation result: {result.get('validation')}")
    if result.get("validation", {}).get("valid"):
        print("Configuration validated successfully!")
        # In real scenario, would set dry_run=False to execute
    else:
        print("Configuration validation failed!")
        print(f"Errors: {result.get('validation', {}).get('errors')}")

    print()

    # Example 4: Conversation with history
    print("Example 4: Multi-turn Conversation")
    print("-" * 40)

    requests = [
        "What VLANs do we need to configure?",
        "Configure VLAN 100 as management",
        "Configure VLAN 200 as users",
        "Configure VLAN 300 as guests",
    ]

    for req in requests:
        result = agent.execute(req, device_name="switch1")
        print(f"Request: {req}")
        print(f"Status: {result['status']}\n")

    # View conversation history
    history = agent.get_history()
    print(f"Conversation history length: {len(history)} messages")

    # Cleanup
    agent.device_manager.close_all_connections()


if __name__ == "__main__":
    main()
