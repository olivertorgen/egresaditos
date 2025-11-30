# settings.py

import pygame
import os

# Configuración de la Ventana (Mantener)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CAPTION = "Egresaditos: La Última Semana"

# Base de Rutas
ASSETS_PATH = 'assets/'

def get_asset_path(*parts):
    """
    Construye una ruta de archivo completa para un recurso,
    uniendo la base con las subcarpetas especificadas.
    """
    return os.path.join(ASSETS_PATH, *parts)

def load_image(*parts):
    """Carga una imagen de Pygame desde la ruta calculada."""
    try:
        path = get_asset_path(*parts)
        # Usamos .convert_alpha() para manejar la transparencia
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Error al cargar la imagen {os.path.join(*parts)}: {e}")
        # Retorna una superficie vacía para evitar que el juego falle
        return pygame.Surface((50, 50))
    
    # settings.py

# --- Configuración de Pantalla ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CAPTION = "Egresaditos Game"

# --- Configuración del Juego ---
# ¡AÑADE ESTO!
FPS = 60 

# ... (El resto de tus funciones y configuraciones en settings.py) ...
# Por ejemplo, tu función load_image
# def load_image(folder, filename):
#    ...