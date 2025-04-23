import pygame
from typing import List, Dict, Callable
from config import Config

class ResourceFilter:
    def __init__(self, x: int, y: int, resource_types: List[str], on_filter_change: Callable[[Dict[str, bool]], None]):
        self.config = Config()
        self.x = x
        self.y = y
        self.resource_types = resource_types
        self.on_filter_change = on_filter_change
        self.font = pygame.font.Font(None, 24)
        self.checkbox_size = 20
        self.spacing = 30
        self.filters = {resource: True for resource in resource_types}
        self.hovered_checkbox = None

    def draw(self, surface: pygame.Surface):
        # Draw background
        padding = 10
        width = 200
        height = len(self.resource_types) * self.spacing + padding * 2
        bg_rect = pygame.Rect(self.x, self.y, width, height)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect)
        pygame.draw.rect(surface, (100, 100, 100), bg_rect, 2)

        # Draw title
        title = self.font.render("Resource Filter", True, (255, 255, 255))
        surface.blit(title, (self.x + padding, self.y + padding))

        # Draw checkboxes and labels
        for i, resource in enumerate(self.resource_types):
            y = self.y + padding + 30 + i * self.spacing
            checkbox_rect = pygame.Rect(self.x + padding, y, self.checkbox_size, self.checkbox_size)
            
            # Draw checkbox
            pygame.draw.rect(surface, (100, 100, 100), checkbox_rect)
            if self.filters[resource]:
                pygame.draw.rect(surface, (200, 200, 200), checkbox_rect.inflate(-4, -4))
            
            # Draw label
            label = self.font.render(resource, True, (255, 255, 255))
            surface.blit(label, (self.x + padding + self.checkbox_size + 10, y))

            # Highlight hovered checkbox
            if self.hovered_checkbox == i:
                pygame.draw.rect(surface, (150, 150, 150), checkbox_rect, 2)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over any checkbox
            self.hovered_checkbox = None
            for i, resource in enumerate(self.resource_types):
                y = self.y + 40 + i * self.spacing
                checkbox_rect = pygame.Rect(self.x + 10, y, self.checkbox_size, self.checkbox_size)
                if checkbox_rect.collidepoint(event.pos):
                    self.hovered_checkbox = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Toggle checkbox if clicked
            if self.hovered_checkbox is not None:
                resource = self.resource_types[self.hovered_checkbox]
                self.filters[resource] = not self.filters[resource]
                self.on_filter_change(self.filters)

    def update(self):
        pass 