import pygame
import threading
import time
import math
from typing import Callable, Optional, Tuple
from .ui_component import UIComponent
from ..style.style_manager import StyleManager

class LoadingScreen(UIComponent):
    """Loading screen component that displays a loading spinner and message.
    
    This component is used to indicate that a time-consuming operation
    is in progress, such as map generation.
    """
    
    def __init__(self, 
                 message: str = "Loading...",
                 spinner_size: int = 40,
                 spinner_color: Optional[Tuple[int, int, int]] = None,
                 text_color: Optional[Tuple[int, int, int]] = None) -> None:
        """Initialize the loading screen.
        
        Args:
            message: Message to display
            spinner_size: Size of the spinner in pixels
            spinner_color: Color of the spinner (defaults to primary color)
            text_color: Color of the text (defaults to text color)
        """
        super().__init__(0, 0, 0, 0)
        self._message = message
        self._spinner_size = spinner_size
        self._style = StyleManager.get_instance().get_style()
        self._spinner_color = spinner_color or self._style.get_color("primary")
        self._text_color = text_color or self._style.get_color("text")
        self._angle = 0
        self._last_update = time.time()
        self._bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self._font = pygame.font.Font(None, 36)
        self._is_visible = False
        self._task_completed = False
        self._task_thread = None
        
    def _render_text(self) -> pygame.Surface:
        """Render the loading message text.
        
        Returns:
            pygame.Surface: Rendered text surface
        """
        return self._font.render(self._message, True, self._text_color)
        
    def start_task(self, task: Callable, callback: Optional[Callable] = None) -> None:
        """Start a task in a separate thread with a loading screen.
        
        Args:
            task: Function to execute in the background
            callback: Optional callback to execute when task completes
        """
        self._is_visible = True
        self._task_completed = False
        
        def thread_wrapper():
            # Execute the task
            task()
            # Mark as completed
            self._task_completed = True
            # Execute callback if provided
            if callback:
                callback()
        
        # Start the thread
        self._task_thread = threading.Thread(target=thread_wrapper)
        self._task_thread.daemon = True
        self._task_thread.start()
        
    def update(self) -> None:
        """Update the loading screen animation."""
        if not self._is_visible:
            return
            
        # Update spinner rotation
        current_time = time.time()
        elapsed = current_time - self._last_update
        self._angle = (self._angle + 250 * elapsed) % 360
        self._last_update = current_time
        
        # Hide if task is completed
        if self._task_completed:
            self._is_visible = False
            
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the loading screen.
        
        Args:
            surface: Surface to draw on
        """
        if not self._is_visible:
            return
            
        # Get surface dimensions
        width, height = surface.get_size()
        
        # Create overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill(self._bg_color)
        surface.blit(overlay, (0, 0))
        
        # Draw spinner
        spinner_rect = pygame.Rect(0, 0, self._spinner_size, self._spinner_size)
        spinner_rect.center = (width // 2, height // 2 - 30)
        
        # Draw spinner arc
        radius = self._spinner_size // 2
        center = spinner_rect.center
        start_angle = self._angle
        end_angle = (self._angle + 270) % 360
        
        arc_points = []
        for angle in range(int(start_angle), int(end_angle), 10):
            rad = angle * math.pi / 180
            x = center[0] + int(radius * 0.8 * math.cos(rad))
            y = center[1] + int(radius * 0.8 * math.sin(rad))
            arc_points.append((x, y))
            
        if arc_points:
            pygame.draw.lines(surface, self._spinner_color, False, arc_points, 6)
        
        # Draw text message
        text_surface = self._render_text()
        text_rect = text_surface.get_rect(center=(width // 2, height // 2 + 30))
        surface.blit(text_surface, text_rect)
        
    def is_visible(self) -> bool:
        """Check if the loading screen is visible.
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self._is_visible
        
    def hide(self) -> None:
        """Hide the loading screen."""
        self._is_visible = False
        
    def set_message(self, message: str) -> None:
        """Set the loading message.
        
        Args:
            message: New message to display
        """
        self._message = message 