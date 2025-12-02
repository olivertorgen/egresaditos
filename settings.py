import pygame
import os

# ==============================
# CONFIGURACIÓN DE LA PANTALLA
# ==============================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) # Añadido
CAPTION = "Egresaditos – La Última Semana" # Actualizado
FPS = 60 # Frames per second (Añadido)

# ==============================
# RUTAS Y CARGA DE ASSETS
# ==============================
ASSETS_PATH = "assets" # Root assets folder (debe estar en el directorio de ejecución)

def get_asset_path(*paths):
    """Construye una ruta relativa a la carpeta de assets."""
    return os.path.join(ASSETS_PATH, *paths)

def load_image(subfolder, filename, scale_height=None):
    """
    Carga una imagen, verifica su existencia y opcionalmente la reescala por altura.
    La subcarpeta es la carpeta dentro de 'assets/' (ej: 'bodies', 'clothes').
    """
    path = get_asset_path(subfolder, filename)
    
    # 1. Verificar si existe (de tu código)
    if not os.path.exists(path):
        print(f"⚠ Image not found → {path}")
        surf = pygame.Surface((120, 120))
        surf.fill((255, 50, 50))
        return surf # Fallback surface

    # 2. Carga y manejo de errores
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"ERROR: No se pudo cargar la imagen: {path} - {e}")
        # Retorna un surface rojo de placeholder
        placeholder = pygame.Surface((100, 100))
        placeholder.fill((255, 0, 0))
        return placeholder

    # 3. Escalado (Mantenido - crucial para el personaje)
    if scale_height is not None:
        aspect_ratio = image.get_width() / image.get_height()
        new_width = int(scale_height * aspect_ratio)
        image = pygame.transform.scale(image, (new_width, scale_height))
        
    return image

# ==============================
# COLORES Y ESTILO
# ==============================
WHITE = (255, 255, 255) # Añadido