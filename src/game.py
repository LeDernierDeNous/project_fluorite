import pygame
import sys
from enum import Enum, auto
from typing import Optional, Tuple
from ui.title_screen import TitleScreen
from ui.options_screen import OptionsScreen
from biome.biome_loader import BiomeLoader
from biome.biome_map import BiomeMap
from config import Config

class GameState(Enum):
    """Enumeration of possible game states."""
    TITLE = auto()
    GAME = auto()
    OPTIONS = auto()

class Game:
    """Main game class that manages the game loop and state transitions."""
    
    def __init__(self) -> None:
        """Initialize the game with default settings and components."""
        pygame.init()
        self._config = Config()
        self._screen_width, self._screen_height = self._config.get_window_dimensions()
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Biome Explorer")
        self._clock = pygame.time.Clock()
        self._running = True

        # Initialize game states
        self._current_state = GameState.TITLE
        self._initialize_screens()
        
        # Initialize game components
        self._biome_loader = BiomeLoader()
        self._biome_map: Optional[BiomeMap] = None

    def _initialize_screens(self) -> None:
        """Initialize all game screens with proper callbacks."""
        self._title_screen = TitleScreen(self._screen_width, self._screen_height)
        self._title_screen.set_start_game_callback(self.start_game)
        self._title_screen.set_options_callback(self.show_options)
        self._options_screen = OptionsScreen(self._screen_width, self._screen_height)

    def handle_resize(self, new_width: int, new_height: int) -> None:
        """Handle window resize event.
        
        Args:
            new_width: New window width
            new_height: New window height
        """
        self._screen_width = new_width
        self._screen_height = new_height
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)
        
        # Update screen dimensions
        self._update_screen_dimensions(new_width, new_height)

    def _update_screen_dimensions(self, width: int, height: int) -> None:
        """Update dimensions for all screens and components.
        
        Args:
            width: New width
            height: New height
        """
        self._title_screen.screen_width = width
        self._title_screen.screen_height = height
        self._title_screen.setup_menu()
        
        self._options_screen.screen_width = width
        self._options_screen.screen_height = height
        
        if self._biome_map:
            self._biome_map.update_screen_size(width, height)

    def start_game(self) -> None:
        """Start the game by loading biomes and initializing the biome map."""
        self._current_state = GameState.GAME
        self._biome_loader.load()
        self._biome_map = BiomeMap(self._biome_loader.biomes)
        self._biome_map.update_screen_size(self._screen_width, self._screen_height)

    def show_options(self) -> None:
        """Show the options screen."""
        self._current_state = GameState.OPTIONS

    def handle_events(self) -> None:
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            else:
                self._handle_state_specific_events(event)

    def _handle_state_specific_events(self, event: pygame.event.Event) -> None:
        """Handle events specific to the current game state.
        
        Args:
            event: The pygame event to handle
        """
        if self._current_state == GameState.TITLE:
            self._title_screen.handle_event(event)
        elif self._current_state == GameState.OPTIONS:
            result = self._options_screen.handle_event(event)
            if result == "title":
                self._current_state = GameState.TITLE
        elif self._current_state == GameState.GAME and self._biome_map:
            result = self._biome_map.handle_event(event)
            if result == "menu":
                self._reset_to_title()

    def _reset_to_title(self) -> None:
        """Reset the game state to the title screen."""
        self._current_state = GameState.TITLE
        self._title_screen.setup_menu()
        self._biome_map = None

    def update(self) -> None:
        """Update the current game state."""
        if self._current_state == GameState.TITLE:
            self._title_screen.update()
        elif self._current_state == GameState.OPTIONS:
            self._options_screen.update()
        elif self._current_state == GameState.GAME:
            # Update game state here
            pass

    def draw(self) -> None:
        """Draw the current game state."""
        if self._current_state == GameState.TITLE:
            self._title_screen.draw(self._screen)
        elif self._current_state == GameState.OPTIONS:
            self._options_screen.draw(self._screen)
        elif self._current_state == GameState.GAME:
            self._draw_game_state()

        pygame.display.flip()

    def _draw_game_state(self) -> None:
        """Draw the game state components."""
        self._screen.fill((0, 0, 0))
        if self._biome_map:
            self._biome_map.draw(self._screen)

    def run(self) -> None:
        """Run the main game loop."""
        while self._running:
            self.handle_events()
            self.update()
            self.draw()
            self._clock.tick(60)

        pygame.quit()
        sys.exit()