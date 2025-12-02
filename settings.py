# settings.py
import pygame, os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

ASSETS_PATH = "assets"  # carpeta raíz de imágenes

def get_asset_path(*parts):
    return os.path.join(ASSETS_PATH, *parts)

def load_image(folder, filename):
    """
    Carga real → load_image("ui","button.png")
    Si falla, devuelve Surface y NO string.
    """
    path = get_asset_path(folder, filename)

    if not os.path.exists(path):
        print(f"⚠ Imagen no encontrada → {path}")
        surf = pygame.Surface((120,120))
        surf.fill((255,50,50))
        return surf  # never return string

    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"⚠ Error cargando {path}: {e}")
        surf = pygame.Surface((120,120))
        surf.fill((255,0,0))
        return surf

# --- Estilo opcional
WHITE = (255,255,255)
# ==============================
# RESTAURO VARIABLES QUE MAIN.PY NECESITA
# ==============================

CAPTION = "Egresaditos – La Última Semana"
FPS = 60
