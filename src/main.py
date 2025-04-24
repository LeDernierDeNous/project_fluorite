import logging
import sys
from typing import NoReturn
from game import Game
from config import Config

def setup_logging() -> None:
    """Configure logging for the application.
    
    Sets up a basic logging configuration with both file and console output.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('game.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_config(config: Config) -> bool:
    """Validate the game configuration.
    
    Args:
        config: The game configuration to validate
        
    Returns:
        bool: True if the configuration is valid, False otherwise
    """
    if not config.validate():
        logging.error("Invalid game configuration")
        return False
    return True

def main() -> NoReturn:
    """Main entry point for the game.
    
    This function:
    1. Sets up logging
    2. Validates configuration
    3. Creates and runs the game
    4. Handles any errors that occur
    
    Returns:
        NoReturn: This function never returns, it either runs the game or exits
    """
    try:
        # Setup logging
        setup_logging()
        logging.info("Starting game...")
        
        # Initialize configuration
        config = Config()
        if not validate_config(config):
            logging.error("Failed to validate configuration")
            sys.exit(1)
            
        # Create and run game
        game = Game()
        logging.info("Game initialized successfully")
        
        # Run the game
        game.run()
        
    except Exception as e:
        logging.exception("An error occurred while running the game")
        sys.exit(1)
    finally:
        logging.info("Game shutdown complete")
        sys.exit(0)

if __name__ == "__main__":
    main()
