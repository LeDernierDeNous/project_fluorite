import pygame
from typing import List, Dict, Callable
from config import Config
from ui.style import StyleManager, FontSize

class NoiseMapSelector:
    def __init__(self, x: int, y: int, noise_types: List[str], on_map_change: Callable[[Dict[str, bool]], None]):
        self.config = Config()
        self.x = x
        self.y = y
        self.noise_types = noise_types
        self.on_map_change = on_map_change
        self.style = StyleManager.get_instance().get_style()
        self.checkbox_size = 20
        self.spacing = 30
        self.active_maps = {noise_type: False for noise_type in noise_types}
        self.hovered_checkbox = None

    def draw(self, surface: pygame.Surface):
        # Draw background
        padding = 10
        width = 200
        height = len(self.noise_types) * self.spacing + padding * 2
        bg_rect = pygame.Rect(self.x, self.y, width, height)
        pygame.draw.rect(surface, self.style.get_color("surface"), bg_rect)
        pygame.draw.rect(surface, self.style.get_color("border"), bg_rect, 2)

        # Draw title
        title = self.style.get_font(FontSize.BODY).render("Noise Maps", True, self.style.get_color("text"))
        surface.blit(title, (self.x + padding, self.y + padding))

        # Draw checkboxes and labels
        for i, noise_type in enumerate(self.noise_types):
            y = self.y + padding + 30 + i * self.spacing
            checkbox_rect = pygame.Rect(self.x + padding, y, self.checkbox_size, self.checkbox_size)
            
            # Draw checkbox
            pygame.draw.rect(surface, self.style.get_color("border"), checkbox_rect)
            if self.active_maps[noise_type]:
                pygame.draw.rect(surface, self.style.get_color("primary"), checkbox_rect.inflate(-4, -4))
            
            # Draw label
            label = self.style.get_font(FontSize.BODY).render(noise_type, True, self.style.get_color("text"))
            surface.blit(label, (self.x + padding + self.checkbox_size + 10, y))

            # Highlight hovered checkbox
            if self.hovered_checkbox == i:
                pygame.draw.rect(surface, self.style.get_color("hover"), checkbox_rect, 2)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over any checkbox
            self.hovered_checkbox = None
            for i, noise_type in enumerate(self.noise_types):
                y = self.y + 40 + i * self.spacing
                checkbox_rect = pygame.Rect(self.x + 10, y, self.checkbox_size, self.checkbox_size)
                if checkbox_rect.collidepoint(event.pos):
                    self.hovered_checkbox = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Toggle checkbox if clicked
            if self.hovered_checkbox is not None:
                noise_type = self.noise_types[self.hovered_checkbox]
                self.active_maps[noise_type] = not self.active_maps[noise_type]
                self.on_map_change(self.active_maps)

    def update(self):
        pass 