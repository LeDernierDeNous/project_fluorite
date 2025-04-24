# Biome Explorer

A Python-based exploration game that procedurally generates biomes based on environmental factors.

## Features

- Procedurally generated biome maps
- Resource exploration and discovery
- Interactive map with panning and zooming
- Multiple visual themes/styles
- Fullscreen support

## Controls

- **F11**: Toggle fullscreen mode
- **Mouse drag**: Pan the map
- **Mouse wheel**: Zoom in/out
- **Click on biomes**: View detailed information

## Command Line Options

```
python main.py [options]

Options:
  --fullscreen    Start the game in fullscreen mode
  --fps FPS       Target frames per second (default: 60)
```

## Installation

1. Clone the repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```

## Development

The game is built with Python and Pygame. The codebase is organized into modules:
- `src/`: Main source code
  - `biome/`: Biome generation and management
  - `map/`: Map rendering and navigation
  - `ui/`: User interface components
  - `config.py`: Game configuration
  - `game.py`: Game loop and main logic
  - `main.py`: Entry point
