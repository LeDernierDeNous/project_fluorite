from typing import Callable, Optional
import pygame
from .ui_component import UIComponent
from ..style.style_manager import StyleManager, FontSize

class Slider(UIComponent):
    """A slider component for selecting values within a range."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float,
        max_value: float,
        initial_value: float,
        on_value_change: Optional[Callable[[float], None]] = None,
        label: Optional[str] = None
    ) -> None:
        """Initialize the slider.
        
        Args:
            x: X position of the slider
            y: Y position of the slider
            width: Width of the slider
            height: Height of the slider
            min_value: Minimum value of the slider
            max_value: Maximum value of the slider
            initial_value: Initial value of the slider
            on_value_change: Callback function when the value changes
            label: Optional label text for the slider
        """
        super().__init__(x, y, width, height)
        self._style = StyleManager.get_instance().get_style()
        self._min_value = min_value
        self._max_value = max_value
        self._value = initial_value
        self._on_value_change = on_value_change
        self._is_dragging = False
        self._label = label
        
    @property
    def value(self) -> float:
        """Get the current value of the slider."""
        return self._value
        
    @value.setter
    def value(self, new_value: float) -> None:
        """Set the value of the slider.
        
        Args:
            new_value: The new value to set
        """
        self._value = max(self._min_value, min(self._max_value, new_value))
        if self._on_value_change:
            self._on_value_change(self._value)
            
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self._is_dragging = True
                self._update_value_from_mouse(event.pos[0])
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._is_dragging:
                self._is_dragging = False
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            if self._is_dragging:
                self._update_value_from_mouse(event.pos[0])
                return True
                
        return False
        
    def _update_value_from_mouse(self, mouse_x: int) -> None:
        """Update the slider value based on mouse position.
        
        Args:
            mouse_x: The x position of the mouse
        """
        relative_x = mouse_x - self.rect.x
        percentage = max(0.0, min(1.0, relative_x / self.rect.width))
        self.value = self._min_value + (self._max_value - self._min_value) * percentage
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the slider on the surface.
        
        Args:
            surface: The surface to draw on
        """
        # Draw label if present
        if self._label:
            font = self._style.get_font(FontSize.SMALL)
            label_text = font.render(self._label, True, self._style.get_color("text"))
            label_rect = label_text.get_rect(
                x=self.rect.x,
                y=self.rect.y - label_text.get_height() - 5
            )
            surface.blit(label_text, label_rect)
            
            # Draw value
            value_text = font.render(f"{self._value:.0f}", True, self._style.get_color("text"))
            value_rect = value_text.get_rect(
                x=self.rect.right + 10,
                y=self.rect.y + (self.rect.height - value_text.get_height()) // 2
            )
            surface.blit(value_text, value_rect)
        
        # Draw the track
        pygame.draw.rect(surface, self._style.get_color("surface"), self.rect)
        pygame.draw.rect(surface, self._style.get_color("border"), self.rect, 1)
        
        # Calculate the position of the handle
        percentage = (self._value - self._min_value) / (self._max_value - self._min_value)
        handle_x = self.rect.x + int(self.rect.width * percentage)
        handle_rect = pygame.Rect(
            handle_x - 5,
            self.rect.y - 5,
            10,
            self.rect.height + 10
        )
        
        # Draw the handle
        pygame.draw.rect(surface, self._style.get_color("primary"), handle_rect) 