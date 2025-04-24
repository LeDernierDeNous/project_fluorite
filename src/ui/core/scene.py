from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import pygame
from config import Config

class Scene(ABC):
    """Base class for all game scenes.
    
    This class provides a common interface for all scenes in the game.
    Each scene must implement the abstract methods to handle events,
    update state, and render content.
    
    Attributes:
        _config: Game configuration object
        _next_scene: Name of the next scene to transition to
        _scene_data: Data to pass to the next scene
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize the scene.
        
        Args:
            config: Game configuration object
        """
        self._config = config
        self._next_scene: Optional[str] = None
        self._scene_data: Dict[str, Any] = {}
        
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        pass
        
    @abstractmethod
    def update(self) -> None:
        """Update scene state.
        
        This method is called once per frame to update the scene's state.
        """
        pass
        
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene.
        
        Args:
            surface: Surface to draw on
        """
        pass
        
    def on_window_resize(self, width: int, height: int) -> None:
        """Handle window resize event.
        
        This method should be overridden by scenes that need to update
        their layout when the window size changes.
        
        Args:
            width: New window width
            height: New window height
        """
        # Default implementation does nothing
        pass
        
    def get_next_scene(self) -> Optional[str]:
        """Get the next scene to transition to.
        
        Returns:
            Optional[str]: Name of the next scene or None if staying in current scene
        """
        return self._next_scene
        
    def get_scene_data(self) -> Dict[str, Any]:
        """Get data to pass to the next scene.
        
        Returns:
            Dict[str, Any]: Data to pass to the next scene
        """
        return self._scene_data.copy()
        
    def set_scene_data(self, data: Dict[str, Any]) -> None:
        """Set data received from the previous scene.
        
        Args:
            data: Data received from the previous scene
        """
        self._scene_data = data.copy()
        
    def reset(self) -> None:
        """Reset the scene state.
        
        This method is called when the scene is about to be reused.
        It resets all state variables to their initial values.
        """
        self._next_scene = None
        self._scene_data = {} 