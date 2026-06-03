"""Main entry point for Network AI Agent"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.network_agent import NetworkAgent
from src.utils.logger import Logger


def main():
    """Main function"""
    logger = Logger.setup("main", level="INFO")

    try:
        # Initialize agent
        logger.info("Initializing Network AI Agent...")
        agent = NetworkAgent(config_path="config/config.yaml")

        # Interactive mode
        logger.info("Starting interactive mode. Type 'quit' to exit.")
        print("\n" + "=" * 60)
        print("Network AI Agent - Interactive Configuration")
        print("=" * 60 + "\n")

        while True:
            try:
                # Get user input
                user_request = input("Enter your request (or 'quit' to exit): ").strip()

                if user_request.lower() in ["quit", "exit", "q"]:
                    print("Exiting...")
                    break

                if not user_request:
                    continue

                # Execute request
                print("\nProcessing request...")
                result = agent.execute(user_request)

                # Display result
                print("\n" + "-" * 60)
                print("RESULT:")
                print("-" * 60)
                print(f"Status: {result.get('status')}")

                if result.get("status") == "failed":
                    print(f"Error: {result.get('error')}")
                else:
                    commands = result.get("commands", {})
                    print(f"\nCommands Generated:")
                    for cmd in commands.get("commands", []):
                        print(f"  > {cmd}")

                    results = result.get("results", [])
                    if results:
                        print(f"\nExecution Results:")
                        for res in results:
                            status = res.get("status")
                            output = res.get("output", "")
                            print(f"  [{status}] {res.get('command')}")
                            if output and len(output) < 200:
                                print(f"       {output[:200]}")

                print("-" * 60 + "\n")

            except KeyboardInterrupt:
                print("\n\nInterrupt received. Exiting...")
                break
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"Error: {str(e)}\n")

        # Cleanup
        logger.info("Closing connections...")
        agent.device_manager.close_all_connections()
        print("Done!")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
