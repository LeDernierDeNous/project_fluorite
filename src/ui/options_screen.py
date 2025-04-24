import pygame
from typing import List, Optional, Tuple
from .components import Button
from .style import ColorPalette, StyleManager, FontSize

class OptionsScreen:
    """A screen for managing game options, particularly color themes."""
    
    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Initialize the options screen.
        
        Args:
            screen_width: The width of the screen
            screen_height: The height of the screen
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._style_manager = StyleManager.get_instance()
        self._style = self._style_manager.get_style()
        
        # Initialize UI components
        self._palette_buttons: List[Button] = []
        self._back_button: Optional[Button] = None
        
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Set up the UI components of the options screen."""
        button_width, button_height = self._calculate_button_dimensions()
        spacing = self._screen_height // 36
        
        # Calculate positions
        start_y = self._calculate_start_y(button_height, spacing)
        
        # Create theme selection buttons
        self._create_palette_buttons(button_width, button_height, spacing, start_y)
        
        # Create back button
        self._create_back_button(button_width, button_height, spacing, start_y)
        
    def _calculate_button_dimensions(self) -> Tuple[int, int]:
        """Calculate the dimensions for buttons.
        
        Returns:
            A tuple of (width, height) for the buttons
        """
        width = min(self._screen_width // 4, 200)
        height = min(self._screen_height // 12, 50)
        return width, height
        
    def _calculate_start_y(self, button_height: int, spacing: int) -> int:
        """Calculate the starting Y position for buttons.
        
        Args:
            button_height: Height of each button
            spacing: Space between buttons
            
        Returns:
            The Y coordinate to start placing buttons
        """
        total_height = (len(ColorPalette) + 1) * (button_height + spacing)
        return (self._screen_height - total_height) // 2
        
    def _create_palette_buttons(self, width: int, height: int, spacing: int, start_y: int) -> None:
        """Create buttons for each color palette.
        
        Args:
            width: Width of each button
            height: Height of each button
            spacing: Space between buttons
            start_y: Starting Y position
        """
        for i, palette in enumerate(ColorPalette):
            y = start_y + i * (height + spacing)
            button = Button(
                x=(self._screen_width - width) // 2,
                y=y,
                width=width,
                height=height,
                text=palette.name,
                action=lambda p=palette: self._on_palette_selected(p),
                color_type="primary",
                hover_color_type="hover",
                text_color_type="text"
            )
            self._palette_buttons.append(button)
            
    def _create_back_button(self, width: int, height: int, spacing: int, start_y: int) -> None:
        """Create the back button.
        
        Args:
            width: Width of the button
            height: Height of the button
            spacing: Space between buttons
            start_y: Starting Y position
        """
        back_y = start_y + len(ColorPalette) * (height + spacing)
        self._back_button = Button(
            x=(self._screen_width - width) // 2,
            y=back_y,
            width=width,
            height=height,
            text="Back",
            action=self._on_back,
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
    def _on_palette_selected(self, palette: ColorPalette) -> None:
        """Handle palette selection.
        
        Args:
            palette: The selected color palette
        """
        self._style_manager.set_style(palette)
        self._style = self._style_manager.get_style()
        self._update_button_styles()
        
    def _update_button_styles(self) -> None:
        """Update the styles of all buttons."""
        for button in self._palette_buttons:
            button.update_style(
                color_type="primary",
                hover_color_type="hover",
                text_color_type="text"
            )
        if self._back_button:
            self._back_button.update_style(
                color_type="secondary",
                hover_color_type="hover",
                text_color_type="text"
            )
        
    def _on_back(self) -> str:
        """Handle back button click.
        
        Returns:
            The state to transition to ("title")
        """
        return "title"
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the options screen.
        
        Args:
            surface: The surface to draw on
        """
        self._draw_title(surface)
        self._draw_subtitle(surface)
        self._draw_buttons(surface)
        
    def _draw_title(self, surface: pygame.Surface) -> None:
        """Draw the title text.
        
        Args:
            surface: The surface to draw on
        """
        title_font = self._style.get_font(FontSize.TITLE)
        title_text = title_font.render("Options", True, self._style.get_color("text"))
        title_rect = title_text.get_rect(center=(self._screen_width // 2, self._screen_height // 6))
        surface.blit(title_text, title_rect)
        
    def _draw_subtitle(self, surface: pygame.Surface) -> None:
        """Draw the subtitle text.
        
        Args:
            surface: The surface to draw on
        """
        subtitle_font = self._style.get_font(FontSize.HEADING)
        subtitle_text = subtitle_font.render("Select Color Theme", True, self._style.get_color("text_secondary"))
        subtitle_rect = subtitle_text.get_rect(center=(self._screen_width // 2, self._screen_height // 6 + 50))
        surface.blit(subtitle_text, subtitle_rect)
        
    def _draw_buttons(self, surface: pygame.Surface) -> None:
        """Draw all buttons.
        
        Args:
            surface: The surface to draw on
        """
        for button in self._palette_buttons:
            button.draw(surface)
        if self._back_button:
            self._back_button.draw(surface)
        
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events and return new state if needed.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            The new state to transition to, or None if no transition
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self._palette_buttons:
                if button.is_clicked(event.pos):
                    button.on_click()
            if self._back_button and self._back_button.is_clicked(event.pos):
                return self._back_button.on_click()
        return None

    def update(self) -> None:
        """Update the options screen state."""
        pass 