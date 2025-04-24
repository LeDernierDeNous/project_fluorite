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

        # Calculate background dimensions based on components
        if self.components:
            # Find the min and max positions of all components
            min_x = min(comp.rect.left for comp in self.components)
            max_x = max(comp.rect.right for comp in self.components)
            min_y = min(comp.rect.top for comp in self.components)
            max_y = max(comp.rect.bottom for comp in self.components)
            
            # Add padding
            padding = 20
            bg_rect = pygame.Rect(
                min_x - padding,
                min_y - padding,
                max_x - min_x + padding * 2,
                max_y - min_y + padding * 2
            )
            
            # Draw menu background
            pygame.draw.rect(surface, self.background_color, bg_rect)
            pygame.draw.rect(surface, (100, 100, 100), bg_rect, 2)  # Add a border

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