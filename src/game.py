import pygame
import sys
from typing import Tuple
from ui import SceneManager, TitleScreen, OptionsScreen, GameScreen
from config import Config

class Game:
    """Main game class that manages the game loop and state transitions.
    
    This class is responsible for:
    - Initializing the game window and systems
    - Managing the game loop
    - Handling window events
    - Coordinating scene transitions
    
    Attributes:
        _config: Game configuration object
        _screen_width: Current window width
        _screen_height: Current window height
        _screen: Pygame display surface
        _clock: Pygame clock for frame rate control
        _running: Flag indicating if the game is running
        _scene_manager: Manager for game scenes
    """
    
    def __init__(self) -> None:
        """Initialize the game with default settings and components."""
        pygame.init()
        self._config = Config()
        self._screen_width, self._screen_height = self._config.get_window_dimensions()
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Biome Explorer")
        self._clock = pygame.time.Clock()
        self._running = True

        # Initialize scene manager
        self._scene_manager = SceneManager(self._config)
        self._register_scenes()
        self._scene_manager.set_scene("title")

    def _register_scenes(self) -> None:
        """Register all available scenes with the scene manager."""
        self._scene_manager.register_scene("title", TitleScreen)
        self._scene_manager.register_scene("options", OptionsScreen)
        self._scene_manager.register_scene("game", GameScreen)

    def handle_resize(self, new_width: int, new_height: int) -> None:
        """Handle window resize event.
        
        Args:
            new_width: New window width
            new_height: New window height
        """
        self._screen_width = new_width
        self._screen_height = new_height
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)
        # Update window config
        self._config.window_config.width = new_width
        self._config.window_config.height = new_height

    def handle_events(self) -> None:
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            else:
                self._scene_manager.handle_event(event)

    def update(self) -> None:
        """Update the current scene."""
        self._scene_manager.update()

    def draw(self) -> None:
        """Draw the current scene."""
        self._scene_manager.draw(self._screen)
        pygame.display.flip()

    def run(self) -> None:
        """Run the main game loop."""
        while self._running:
            self.handle_events()
            self.update()
            self.draw()
            self._clock.tick(60)

        pygame.quit()
        sys.exit()