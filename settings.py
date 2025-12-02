import pygame, os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

ASSETS_PATH = "assets" # Root assets folder

def get_asset_path(*parts):
    return os.path.join(ASSETS_PATH, *parts)

def load_image(folder, filename):
    """
    Real load example: load_image("ui", "button.png")
    If loading fails, returns a Surface, NOT a string.
    """
    path = get_asset_path(folder, filename)

    if not os.path.exists(path):
        print(f"⚠ Image not found → {path}")
        surf = pygame.Surface((120, 120))
        surf.fill((255, 50, 50))
        return surf # never return string

    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"⚠ Error loading {path}: {e}")
        surf = pygame.Surface((120, 120))
        surf.fill((255, 0, 0))
        return surf

# --- Optional Style
WHITE = (255, 255, 255)

# ==============================
# GLOBAL VARIABLES
# ==============================
CAPTION = "Egresaditos – La Última Semana"
FPS = 60 # Frames per second