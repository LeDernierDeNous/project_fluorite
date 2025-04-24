import pygame
from typing import List, Optional
from .components import Button
from .style import ColorPalette, StyleManager, FontSize

class OptionsScreen:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.style_manager = StyleManager.get_instance()
        self.style = self.style_manager.get_style()
        
        # Calculate button dimensions
        button_width = min(screen_width // 4, 200)
        button_height = min(screen_height // 12, 50)
        spacing = screen_height // 36
        
        # Calculate total height needed for all buttons
        total_height = (len(ColorPalette) + 1) * (button_height + spacing)
        start_y = (screen_height - total_height) // 2
        
        # Create buttons for each color palette
        self.palette_buttons: List[Button] = []
        for i, palette in enumerate(ColorPalette):
            y = start_y + i * (button_height + spacing)
            button = Button(
                x=(screen_width - button_width) // 2,
                y=y,
                width=button_width,
                height=button_height,
                text=palette.name,
                action=lambda p=palette: self._on_palette_selected(p),
                color_type="primary",
                hover_color_type="hover",
                text_color_type="text"
            )
            self.palette_buttons.append(button)
            
        # Create back button
        back_y = start_y + len(ColorPalette) * (button_height + spacing)
        self.back_button = Button(
            x=(screen_width - button_width) // 2,
            y=back_y,
            width=button_width,
            height=button_height,
            text="Back",
            action=self._on_back,
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
    def _on_palette_selected(self, palette: ColorPalette):
        """Handle palette selection"""
        self.style_manager.set_style(palette)
        self.style = self.style_manager.get_style()
        # Update all button styles
        for button in self.palette_buttons:
            button.update_style(
                color_type="primary",
                hover_color_type="hover",
                text_color_type="text"
            )
        self.back_button.update_style(
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
    def _on_back(self):
        """Handle back button click"""
        return "title"
        
    def draw(self, surface: pygame.Surface):
        # Draw title
        title_font = self.style.get_font(FontSize.TITLE)
        title_text = title_font.render("Options", True, self.style.get_color("text"))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 6))
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_font = self.style.get_font(FontSize.HEADING)
        subtitle_text = subtitle_font.render("Select Color Theme", True, self.style.get_color("text_secondary"))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, title_rect.bottom + 20))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw all buttons
        for button in self.palette_buttons:
            button.draw(surface)
        self.back_button.draw(surface)
        
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events and return new state if needed"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.palette_buttons:
                if button.is_clicked(event.pos):
                    button.on_click()
            if self.back_button.is_clicked(event.pos):
                return self.back_button.on_click()
        return None

    def update(self):
        """Update the options screen state"""
        pass 