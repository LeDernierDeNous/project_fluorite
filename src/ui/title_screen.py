import pygame
from typing import Callable
from .menu import Menu
from .components import Button

class TitleScreen:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu = Menu()
        self.setup_menu()

    def setup_menu(self):
        # Calculate button dimensions and positions
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_height = (button_height * 3) + (button_spacing * 2)
        start_y = (self.screen_height - total_height) // 2

        # Create buttons
        self.menu.add_component(Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y,
            width=button_width,
            height=button_height,
            text="Start Game",
            action=self.on_start_game
        ))

        self.menu.add_component(Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y + button_height + button_spacing,
            width=button_width,
            height=button_height,
            text="Options",
            action=self.on_options
        ))

        self.menu.add_component(Button(
            x=(self.screen_width - button_width) // 2,
            y=start_y + (button_height + button_spacing) * 2,
            width=button_width,
            height=button_height,
            text="Quit",
            action=self.on_quit
        ))

    def on_start_game(self):
        self.menu.hide()
        if hasattr(self, 'on_start_game_callback'):
            self.on_start_game_callback()

    def on_options(self):
        # TODO: Implement options menu
        pass

    def on_quit(self):
        pygame.quit()
        exit()

    def set_start_game_callback(self, callback: Callable[[], None]):
        self.on_start_game_callback = callback

    def draw(self, surface: pygame.Surface):
        # Draw background
        surface.fill((0, 0, 0))
        
        # Draw title
        font = pygame.font.Font(None, 74)
        title_text = font.render("Biome Explorer", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        surface.blit(title_text, title_rect)

        # Draw menu
        self.menu.draw(surface)

    def handle_event(self, event: pygame.event.Event):
        self.menu.handle_event(event)

    def update(self):
        self.menu.update() 