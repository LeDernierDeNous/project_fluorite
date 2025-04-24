import pygame
from typing import Callable, Tuple
from .ui_component import UIComponent
from ..style import StyleManager, FontSize

class Button(UIComponent):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, action: Callable[[], None],
                 color_type: str = "primary",
                 hover_color_type: str = "hover",
                 text_color_type: str = "text"):
        super().__init__(x, y, width, height)
        self.text = text
        self.action = action
        self.color_type = color_type
        self.hover_color_type = hover_color_type
        self.text_color_type = text_color_type
        self.is_hovered = False
        self.style = StyleManager.get_instance().get_style()
        self.font = self.style.get_font(FontSize.BODY)

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        color = self.style.get_color(self.hover_color_type) if self.is_hovered else self.style.get_color(self.color_type)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.style.get_color("border"), self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, self.style.get_color(self.text_color_type))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.action()

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """Check if the button is clicked at the given position"""
        return self.rect.collidepoint(pos)

    def on_click(self):
        """Execute the button's action"""
        self.action()

    def update_style(self, color_type: str = None, hover_color_type: str = None, text_color_type: str = None):
        """Update the button's color types"""
        if color_type:
            self.color_type = color_type
        if hover_color_type:
            self.hover_color_type = hover_color_type
        if text_color_type:
            self.text_color_type = text_color_type 