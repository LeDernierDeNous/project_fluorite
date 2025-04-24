import pygame
from typing import Dict, Tuple, List, Optional
from enum import Enum

class ColorPalette(Enum):
    DARK = {
        "background": (20, 20, 20),
        "surface": (30, 30, 30),
        "primary": (41, 128, 185),  # Blue
        "secondary": (39, 174, 96),  # Green
        "accent": (231, 76, 60),    # Red
        "text": (236, 240, 241),    # Light gray
        "text_secondary": (189, 195, 199),  # Gray
        "border": (44, 62, 80),     # Dark blue
        "hover": (52, 152, 219),    # Light blue
        "disabled": (127, 140, 141) # Gray
    }
    
    LIGHT = {
        "background": (236, 240, 241),
        "surface": (189, 195, 199),
        "primary": (52, 152, 219),  # Blue
        "secondary": (46, 204, 113), # Green
        "accent": (231, 76, 60),    # Red
        "text": (44, 62, 80),       # Dark blue
        "text_secondary": (52, 73, 94),  # Dark gray
        "border": (149, 165, 166),  # Gray
        "hover": (41, 128, 185),    # Dark blue
        "disabled": (189, 195, 199) # Light gray
    }
    
    MYSTICAL = {
        "background": (44, 62, 80),
        "surface": (52, 73, 94),
        "primary": (155, 89, 182),  # Purple
        "secondary": (26, 188, 156), # Turquoise
        "accent": (230, 126, 34),   # Orange
        "text": (236, 240, 241),    # Light gray
        "text_secondary": (189, 195, 199),  # Gray
        "border": (41, 128, 185),   # Blue
        "hover": (142, 68, 173),    # Dark purple
        "disabled": (127, 140, 141) # Gray
    }

class FontSize(Enum):
    TITLE = 48
    HEADING = 36
    BODY = 24
    SMALL = 18
    TINY = 14

class UIStyle:
    def __init__(self, palette: ColorPalette = ColorPalette.DARK):
        self.palette = palette
        self.colors = palette.value
        self.fonts: Dict[FontSize, pygame.font.Font] = {}
        self._load_fonts()
        
    def _load_fonts(self):
        """Load all required fonts with different sizes"""
        for size in FontSize:
            self.fonts[size] = pygame.font.Font(None, size.value)
            
    def get_font(self, size: FontSize) -> pygame.font.Font:
        """Get a font of the specified size"""
        return self.fonts[size]
        
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get a color from the current palette"""
        return self.colors[color_name]
        
    def set_palette(self, palette: ColorPalette):
        """Change the current color palette"""
        self.palette = palette
        self.colors = palette.value

class StyleManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StyleManager, cls).__new__(cls)
            cls._instance.current_style = UIStyle()
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'StyleManager':
        return cls()
    
    def get_style(self) -> UIStyle:
        return self.current_style
    
    def set_style(self, palette: ColorPalette):
        self.current_style.set_palette(palette) 