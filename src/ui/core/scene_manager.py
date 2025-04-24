from typing import Dict, Type, Optional
from .scene import Scene
from config import Config

class SceneManager:
    """Manages game scenes and transitions between them.
    
    This class is responsible for:
    - Registering available scenes
    - Managing scene transitions
    - Handling scene updates and rendering
    - Passing data between scenes
    
    Attributes:
        _config: Game configuration object
        _scenes: Dictionary mapping scene names to scene classes
        _current_scene: Currently active scene instance
        _current_scene_name: Name of the currently active scene
        _needs_redraw: Flag indicating if the scene needs a full redraw
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize the scene manager.
        
        Args:
            config: Game configuration object
        """
        self._config = config
        self._scenes: Dict[str, Type[Scene]] = {}
        self._current_scene: Optional[Scene] = None
        self._current_scene_name: Optional[str] = None
        self._needs_redraw: bool = True
        
    def register_scene(self, name: str, scene_class: Type[Scene]) -> None:
        """Register a new scene type.
        
        Args:
            name: Name of the scene
            scene_class: Scene class to register
            
        Raises:
            ValueError: If scene name is already registered
        """
        if name in self._scenes:
            raise ValueError(f"Scene '{name}' is already registered")
        self._scenes[name] = scene_class
        
    def set_scene(self, name: str, data: Optional[dict] = None) -> None:
        """Set the current scene.
        
        Args:
            name: Name of the scene to set
            data: Optional data to pass to the scene
            
        Raises:
            ValueError: If scene name is not registered
        """
        if name not in self._scenes:
            raise ValueError(f"Scene '{name}' not registered")
            
        # Create new scene instance
        self._current_scene = self._scenes[name](self._config)
        self._current_scene_name = name
        self._needs_redraw = True
        
        # Pass data to scene if provided
        if data:
            self._current_scene.set_scene_data(data)
            
    def handle_event(self, event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        if self._current_scene:
            self._current_scene.handle_event(event)
            
            # Check for scene transition
            next_scene = self._current_scene.get_next_scene()
            if next_scene:
                scene_data = self._current_scene.get_scene_data()
                self.set_scene(next_scene, scene_data)
                
    def update(self) -> None:
        """Update the current scene."""
        if self._current_scene:
            self._current_scene.update()
            
    def draw(self, surface) -> None:
        """Draw the current scene.
        
        Args:
            surface: Surface to draw on
        """
        if self._current_scene:
            # If we need a full redraw, clear the surface first
            if self._needs_redraw:
                surface.fill((0, 0, 0))  # Clear with black
                self._needs_redraw = False
                
            self._current_scene.draw(surface)
            
    @property
    def current_scene_name(self) -> Optional[str]:
        """Get the name of the current scene.
        
        Returns:
            Optional[str]: Name of the current scene
        """
        return self._current_scene_name 