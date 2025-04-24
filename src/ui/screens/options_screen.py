import pygame
from typing import Dict, Optional
from ..core.scene import Scene
from ..components import Button
from ..style.style_manager import StyleManager, FontSize, ColorPalette
from config import Config

class OptionsScreen(Scene):
    """Options screen scene for selecting game styles/themes.
    
    This scene allows the user to switch between different visual styles
    and color themes for the game.
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize the options screen.
        
        Args:
            config: Game configuration
        """
        super().__init__(config)
        self._style = StyleManager.get_instance().get_style()
        self._theme_buttons: Dict[str, Button] = {}
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Setup the options screen UI."""
        # Calculate dimensions
        width, height = self._config.get_window_dimensions()
        button_width = min(width // 4, 200)
        button_height = min(height // 12, 50)
        spacing = height // 36
        
        # Create back button
        self._back_button = Button(
            x=20,
            y=20,
            width=button_width,
            height=button_height,
            text="Back",
            action=self._on_back_clicked,
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
        # Create theme selection buttons
        start_y = height // 3
        current_y = start_y
        
        for theme in ColorPalette:
            button = Button(
                x=(width - button_width) // 2,
                y=current_y,
                width=button_width,
                height=button_height,
                text=theme.name.capitalize(),
                action=lambda t=theme: self._on_theme_selected(t),
                color_type="primary" if theme == self._config.theme else "secondary",
                hover_color_type="hover",
                text_color_type="text"
            )
            self._theme_buttons[theme.name] = button
            current_y += button_height + spacing
            
    def _on_back_clicked(self) -> None:
        """Handle back button click."""
        self._next_scene = "title"
        
    def _on_theme_selected(self, theme: ColorPalette) -> None:
        """Handle theme selection.
        
        Args:
            theme: Selected color theme
        """
        # Update theme in config
        self._config.theme = theme
        
        # Update style manager
        StyleManager.get_instance().set_style(theme)
        
        # Update button states
        for name, button in self._theme_buttons.items():
            button.color_type = "primary" if ColorPalette[name] == theme else "secondary"
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.VIDEORESIZE:
            # Update UI for new window size
            self._setup_ui()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._back_button.is_clicked(event.pos):
                self._back_button.on_click()
                
            for button in self._theme_buttons.values():
                if button.is_clicked(event.pos):
                    button.on_click()
                    
    def update(self) -> None:
        """Update the options screen state."""
        pass
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the options screen.
        
        Args:
            surface: Surface to draw on
        """
        width, height = self._config.get_window_dimensions()
        
        # Draw background
        surface.fill(self._style.get_color("background"))
        
        # Draw title
        title_font = self._style.get_font(FontSize.TITLE)
        title_text = title_font.render("Style Selector", True, self._style.get_color("text"))
        title_rect = title_text.get_rect(center=(width // 2, height // 6))
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_font = self._style.get_font(FontSize.BODY)
        subtitle_text = subtitle_font.render("Select a theme:", True, self._style.get_color("text_secondary"))
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 4))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw back button
        self._back_button.draw(surface)
        
        # Draw theme buttons
        for button in self._theme_buttons.values():
            button.draw(surface)
            
    def reset(self) -> None:
        """Reset the options screen state."""
        super().reset()
        self._theme_buttons.clear()

    def on_window_resize(self, width: int, height: int) -> None:
        """Handle window resize event.
        
        Args:
            width: New window width
            height: New window height
        """
        # Update UI layout for new window size
        self._setup_ui() 