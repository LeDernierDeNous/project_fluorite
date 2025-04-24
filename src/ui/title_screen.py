import pygame
from typing import Optional, Callable
from .components import Button
from .style import StyleManager, FontSize

class TitleScreen:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.style = StyleManager.get_instance().get_style()
        self.start_game_callback = None
        self.setup_menu()
        
    def setup_menu(self):
        """Setup or update the menu layout"""
        # Calculate button dimensions
        button_width = min(self.screen_width // 4, 200)
        button_height = min(self.screen_height // 12, 50)
        spacing = self.screen_height // 36
        
        # Calculate total height needed for all buttons
        total_height = 3 * (button_height + spacing)
        start_y = (self.screen_height - total_height) // 2
        
        # Create start button
        self.start_button = Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y,
            width=button_width,
            height=button_height,
            text="Start Game",
            # font=self.style.get_font(FontSize.BODY),
            color=self.style.get_color("primary"),
            hover_color=self.style.get_color("hover"),
            text_color=self.style.get_color("text"),
            action=self._on_start
        )
        
        # Create options button
        self.options_button = Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y + button_height + spacing,
            width=button_width,
            height=button_height,
            text="Options",
            # font=self.style.get_font(FontSize.BODY),
            color=self.style.get_color("secondary"),
            hover_color=self.style.get_color("hover"),
            text_color=self.style.get_color("text"),
            action=self._on_options
        )
        
        # Create quit button
        self.quit_button = Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y + 2 * (button_height + spacing),
            width=button_width,
            height=button_height,
            text="Quit",
            # font=self.style.get_font(FontSize.BODY),
            color=self.style.get_color("secondary"),
            hover_color=self.style.get_color("hover"),
            text_color=self.style.get_color("text"),
            action=self._on_quit
        )
        
    def set_start_game_callback(self, callback: Callable[[], None]):
        """Set the callback function to be called when the start button is clicked"""
        self.start_game_callback = callback
        
    def _on_start(self):
        """Handle start button click"""
        if self.start_game_callback:
            self.start_game_callback()
        return "game"
        
    def _on_options(self):
        """Handle options button click"""
        return "options"
        
    def _on_quit(self):
        """Handle quit button click"""
        return "quit"
        
    def draw(self, surface: pygame.Surface):
        # Draw title
        title_font = self.style.get_font(FontSize.TITLE)
        title_text = title_font.render("Fun Test", True, self.style.get_color("text"))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        surface.blit(title_text, title_rect)
        
        # Draw all buttons
        self.start_button.draw(surface)
        self.options_button.draw(surface)
        self.quit_button.draw(surface)
        
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events and return new state if needed"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.rect.collidepoint(event.pos):
                return self.start_button.action()
            if self.options_button.rect.collidepoint(event.pos):
                return self.options_button.action()
            if self.quit_button.rect.collidepoint(event.pos):
                return self.quit_button.action()
        return None
        
    def update(self):
        """Update the title screen state"""
        pass 