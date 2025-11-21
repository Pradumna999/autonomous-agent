import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.agents.supervisor_agent import SupervisorAgent
from src.utils.logger import get_logger

def main():
    logger = get_logger("main")
    logger.info("Initializing Windows AI Agent...")

    try:
        agent = SupervisorAgent()
        logger.info("Agent initialized successfully.")
        
        print("\n--- Windows AI Agent ---")
        print("Enter your objective below. Type 'exit' to quit.")
        
        while True:
            user_query = input("\nObjective: ")
            if user_query.lower() == 'exit':
                print("Exiting agent.")
                break
            
            if not user_query:
                print("Please enter a valid objective.")
                continue

            result = agent.run(user_query)
            print(f"\n--- Task Finished ---")
            print(f"Final Result: {result}")
            print("\nEnter a new objective or type 'exit'.")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nERROR: {e}")
        print("Please ensure your .env file is set up correctly.")
    except Exception as e:
        logger.critical(f"An unhandled exception occurred: {e}", exc_info=True)
        print(f"\nA critical error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
