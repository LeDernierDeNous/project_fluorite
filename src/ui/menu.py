import pygame
from typing import List
from .components import UIComponent
from config import Config

class Menu:
    def __init__(self, x: int, y: int):
        self.config = Config()
        self.x = x
        self.y = y
        self.components: List[UIComponent] = []
        self.visible = True
        self.background_color = self.config.MENU_BACKGROUND_COLOR

    def add_component(self, component: UIComponent):
        self.components.append(component)

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        # Draw menu background
        pygame.draw.rect(
            surface,
            self.background_color,
            (self.x - 150, self.y - 100, 300, 200)
        )

        for component in self.components:
            component.draw(surface)

    def handle_event(self, event: pygame.event.Event):
        if not self.visible:
            return

        for component in self.components:
            component.handle_event(event)

    def update(self):
        if not self.visible:
            return

        for component in self.components:
            component.update()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False 