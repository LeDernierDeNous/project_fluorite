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
        self.small_font = pygame.font.Font(None, 18)
        self.checkbox_size = 20
        self.spacing = 30
        self.filters = {resource: True for resource in resource_types}
        self.hovered_checkbox = None
        self.resource_counts = {resource: 0 for resource in resource_types}
        self.total_biomes = 0

    def update_resource_stats(self, biome_grid):
        # Reset counts
        self.resource_counts = {resource: 0 for resource in self.resource_types}
        self.total_biomes = 0

        # Count biomes for each resource type
        for row in biome_grid:
            for biome in row:
                if biome:
                    self.resource_counts[biome.resource_type] += 1
                    self.total_biomes += 1

    def draw(self, surface: pygame.Surface):
        # Draw background
        padding = 10
        width = 200
        # Calculate height to fit both filter and stats
        filter_height = len(self.resource_types) * self.spacing + padding * 2
        stats_height = len(self.resource_types) * 20 + padding * 2  # 20 pixels per stat line
        total_height = filter_height + stats_height + 10  # 10 pixels gap between sections
        
        bg_rect = pygame.Rect(self.x, self.y, width, total_height)
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

        # Draw separator line
        separator_y = self.y + filter_height
        pygame.draw.line(surface, (100, 100, 100), 
                        (self.x + padding, separator_y),
                        (self.x + width - padding, separator_y))

        # Draw statistics title
        stats_title = self.font.render("Resource Distribution", True, (255, 255, 255))
        surface.blit(stats_title, (self.x + padding, separator_y + padding))

        # Draw resource statistics
        for i, resource in enumerate(self.resource_types):
            y = separator_y + padding + 30 + i * 20
            count = self.resource_counts[resource]
            percentage = (count / self.total_biomes * 100) if self.total_biomes > 0 else 0
            stat_text = f"{resource}: {count} ({percentage:.1f}%)"
            stat_label = self.small_font.render(stat_text, True, (200, 200, 200))
            surface.blit(stat_label, (self.x + padding, y))

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