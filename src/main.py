import pygame
import sys
from ui.title_screen import TitleScreen
from biome.biome_loader import BiomeLoader
from biome.biome_map import BiomeMap

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Biome Explorer")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game states
        self.current_state = "title"  # title, game
        self.title_screen = TitleScreen(self.screen_width, self.screen_height)
        self.title_screen.set_start_game_callback(self.start_game)

        # Game components
        self.biome_loader = BiomeLoader()
        self.biome_map = None

    def handle_resize(self, new_width: int, new_height: int):
        """Handle window resize event"""
        self.screen_width = new_width
        self.screen_height = new_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        
        # Update title screen dimensions
        self.title_screen.screen_width = new_width
        self.title_screen.screen_height = new_height
        self.title_screen.setup_menu()
        
        # Update biome map if it exists
        if self.biome_map:
            self.biome_map.update_screen_size(new_width, new_height)

    def start_game(self):
        self.current_state = "game"
        self.biome_loader.load()
        self.biome_map = BiomeMap(self.biome_loader.get_biomes())
        self.biome_map.update_screen_size(self.screen_width, self.screen_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            
            if self.current_state == "title":
                self.title_screen.handle_event(event)
            elif self.current_state == "game" and self.biome_map:
                self.biome_map.handle_event(event)

    def update(self):
        if self.current_state == "title":
            self.title_screen.update()
        elif self.current_state == "game":
            # Update game state here
            pass

    def draw(self):
        if self.current_state == "title":
            self.title_screen.draw(self.screen)
        elif self.current_state == "game":
            self.screen.fill((0, 0, 0))
            if self.biome_map:
                self.biome_map.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
