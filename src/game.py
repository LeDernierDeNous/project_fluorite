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
        _is_fullscreen: Flag indicating if the game is in fullscreen mode
    """
    
    def __init__(self) -> None:
        """Initialize the game with default settings and components."""
        pygame.init()
        self._config = Config()
        # Use initial window dimensions for startup
        self._screen_width, self._screen_height = self._config.get_initial_window_dimensions()
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Biome Explorer")
        self._clock = pygame.time.Clock()
        self._running = True
        self._is_fullscreen = False

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
        # Update current window dimensions in config
        self._config.update_window_dimensions(new_width, new_height)
        # Notify scene manager of window resize
        self._scene_manager.handle_window_resize(new_width, new_height)

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode."""
        self._is_fullscreen = not self._is_fullscreen
        
        if self._is_fullscreen:
            # Store current window size before going fullscreen
            self._windowed_size = (self._screen_width, self._screen_height)
            # Switch to fullscreen mode
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self._screen_width, self._screen_height = self._screen.get_size()
        else:
            # Restore windowed mode with previous size
            self._screen_width, self._screen_height = self._windowed_size
            self._screen = pygame.display.set_mode(
                (self._screen_width, self._screen_height), 
                pygame.RESIZABLE
            )
        
        # Update the configuration with new dimensions
        self._config.update_window_dimensions(self._screen_width, self._screen_height)
        # Notify scene manager of window resize
        self._scene_manager.handle_window_resize(self._screen_width, self._screen_height)

    def handle_events(self) -> None:
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                else:
                    self._scene_manager.handle_event(event)
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