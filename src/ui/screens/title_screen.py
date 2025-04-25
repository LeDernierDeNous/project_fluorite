import pygame
from typing import Optional, Callable
from ..core.scene import Scene
from ..components import Button
from ..style.style_manager import StyleManager, FontSize
import sys

class TitleScreen(Scene):
    """Title screen scene.
    
    This scene displays the game title and main menu options.
    """
    
    def __init__(self, config) -> None:
        """Initialize the title screen.
        
        Args:
            config: Game configuration
        """
        super().__init__(config)
        self._style = StyleManager.get_instance().get_style()
        self._setup_menu()
        
    def _setup_menu(self) -> None:
        """Setup or update the menu layout."""
        # Calculate button dimensions
        width, height = self._config.get_window_dimensions()
        button_width = min(width // 4, 200)
        button_height = min(height // 12, 50)
        spacing = height // 36
        
        # Calculate total height needed for all buttons
        total_height = 3 * (button_height + spacing)
        start_y = (height - total_height) // 2
        
        # Create start button
        self._start_button = Button(
            x=(width - button_width) // 2,
            y=start_y,
            width=button_width,
            height=button_height,
            text="Start Game",
            action=self._on_start_clicked,
            color_type="primary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
        # Create options button
        self._options_button = Button(
            x=(width - button_width) // 2,
            y=start_y + button_height + spacing,
            width=button_width,
            height=button_height,
            text="Options",
            action=self._on_options_clicked,
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
        # Create quit button
        self._quit_button = Button(
            x=(width - button_width) // 2,
            y=start_y + 2 * (button_height + spacing),
            width=button_width,
            height=button_height,
            text="Quit",
            action=self._on_quit_clicked,
            color_type="accent",
            hover_color_type="hover",
            text_color_type="text"
        )
        
    def _on_start_clicked(self) -> None:
        """Handle start button click."""
        self._next_scene = "game"
        
    def _on_options_clicked(self) -> None:
        """Handle options button click."""
        self._next_scene = "options"
        
    def _on_quit_clicked(self) -> None:
        """Handle quit button click."""
        pygame.quit()
        sys.exit()
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.VIDEORESIZE:
            # Update UI for new window size
            self._setup_menu()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._start_button.is_clicked(event.pos):
                self._start_button.on_click()
            elif self._options_button.is_clicked(event.pos):
                self._options_button.on_click()
            elif self._quit_button.is_clicked(event.pos):
                self._quit_button.on_click()
                
    def update(self) -> None:
        """Update the title screen state."""
        pass
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the title screen.
        
        Args:
            surface: Surface to draw on
        """
        width, height = self._config.get_window_dimensions()
        
        # Draw title
        title_font = self._style.get_font(FontSize.TITLE)
        title_text = title_font.render("Project Fluorite", True, self._style.get_color("text"))
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_font = self._style.get_font(FontSize.HEADING)
        subtitle_text = subtitle_font.render("Explore and Discover", True, 
                                           self._style.get_color("text_secondary"))
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, 
                                                     title_rect.bottom + 20))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw all buttons
        self._start_button.draw(surface)
        self._options_button.draw(surface)
        self._quit_button.draw(surface)

    def on_window_resize(self, width: int, height: int) -> None:
        """Handle window resize event.
        
        Args:
            width: New window width
            height: New window height
        """
        # Update UI layout for new window size
        self._setup_menu() 