import pygame
from typing import List, Optional
from ..core.scene import Scene
from ..components import UIComponent
from ..style.style_manager import StyleManager, FontSize
from config import Config

class Menu(Scene):
    """A menu scene that can contain multiple UI components.
    
    This class provides a flexible menu system that can be used for various
    in-game menus like pause menu, settings menu, etc.
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize the menu.
        
        Args:
            config: Game configuration object
        """
        super().__init__(config)
        self._style = StyleManager.get_instance().get_style()
        self._components: List[UIComponent] = []
        self._visible = True
        self._padding = 20
        
    def add_component(self, component: UIComponent) -> None:
        """Add a UI component to the menu.
        
        Args:
            component: The UI component to add
        """
        self._components.append(component)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        if not self._visible:
            return
            
        if event.type == pygame.VIDEORESIZE:
            # Update components for new window size
            self._update_component_positions(event.w, event.h)
            
        for component in self._components:
            component.handle_event(event)
            
    def update(self) -> None:
        """Update the menu state."""
        if not self._visible:
            return
            
        for component in self._components:
            component.update()
            
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the menu.
        
        Args:
            surface: Surface to draw on
        """
        if not self._visible:
            return
            
        # Draw background if there are components
        if self._components:
            # Calculate background dimensions
            min_x = min(comp.rect.left for comp in self._components)
            max_x = max(comp.rect.right for comp in self._components)
            min_y = min(comp.rect.top for comp in self._components)
            max_y = max(comp.rect.bottom for comp in self._components)
            
            # Add padding
            bg_rect = pygame.Rect(
                min_x - self._padding,
                min_y - self._padding,
                max_x - min_x + self._padding * 2,
                max_y - min_y + self._padding * 2
            )
            
            # Draw menu background
            pygame.draw.rect(surface, self._style.get_color("surface"), bg_rect)
            pygame.draw.rect(surface, self._style.get_color("border"), bg_rect, 2)
            
        # Draw components
        for component in self._components:
            component.draw(surface)
            
    def _update_component_positions(self, width: int, height: int) -> None:
        """Update component positions based on new window size.
        
        Args:
            width: New window width
            height: New window height
        """
        # Center the menu in the window
        if self._components:
            # Calculate total menu dimensions
            min_x = min(comp.rect.left for comp in self._components)
            max_x = max(comp.rect.right for comp in self._components)
            min_y = min(comp.rect.top for comp in self._components)
            max_y = max(comp.rect.bottom for comp in self._components)
            
            menu_width = max_x - min_x + self._padding * 2
            menu_height = max_y - min_y + self._padding * 2
            
            # Calculate offset to center the menu
            offset_x = (width - menu_width) // 2
            offset_y = (height - menu_height) // 2
            
            # Update component positions
            for component in self._components:
                component.rect.x += offset_x - min_x + self._padding
                component.rect.y += offset_y - min_y + self._padding
                
    def show(self) -> None:
        """Show the menu."""
        self._visible = True
        
    def hide(self) -> None:
        """Hide the menu."""
        self._visible = False
        
    def reset(self) -> None:
        """Reset the menu state."""
        super().reset()
        self._components.clear()
        self._visible = True 