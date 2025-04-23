import pygame
from typing import List
from .components import UIComponent

class Menu:
    def __init__(self):
        self.components: List[UIComponent] = []
        self.visible = True

    def add_component(self, component: UIComponent):
        self.components.append(component)

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

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