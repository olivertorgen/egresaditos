import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, get_asset_path

# Altura base del personaje, crucial para calcular posiciones
CHARACTER_HEIGHT = 200 

class Player(pygame.sprite.Sprite):
    def __init__(self, body, head, hat=None):
        super().__init__()
        
        # Assets actuales
        self.body_asset = body 
        self.head_asset = head 
        self.hat_asset = hat 
        
        self.x = 0
        self.y = 0 
        
        # Diccionario para guardar las imágenes cargadas
        self.parts = {}
        self._load_parts()
        
        # Imagen compuesta inicial y su rectángulo
        self.image = self._create_composite_image()
        self.rect = self.image.get_rect()

    def _load_parts(self):
        """Carga y reescala las imágenes de las partes del cuerpo y la ropa."""
        # Lógica de carga para el cuerpo (busca en 'clothes' si es una prenda, o 'bodies' si es base)
        if 'sweater' in self.body_asset or 'shirt' in self.body_asset:
            self.parts['body'] = load_image("clothes", self.body_asset, scale_height=CHARACTER_HEIGHT)
        else:
            self.parts['body'] = load_image("bodies", self.body_asset, scale_height=CHARACTER_HEIGHT)
            
        # Carga de la cabeza (escala a la mitad de la altura total)
        self.parts['head'] = load_image("heads", self.head_asset, scale_height=CHARACTER_HEIGHT // 2)

        # Carga del sombrero (si existe)
        if self.hat_asset:
            self.parts['hat'] = load_image("hats", self.hat_asset, scale_height=CHARACTER_HEIGHT // 3)
        else:
            self.parts['hat'] = None

    def _create_composite_image(self):
        """Combina las partes cargadas en una sola superficie para dibujar."""
        body_img = self.parts.get('body')
        if not body_img:
            # Fallback en caso de error de carga
            return pygame.Surface((100, CHARACTER_HEIGHT))

        width = body_img.get_width()
        height = body_img.get_height()
        
        composite = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Dibujar Body
        body_rect = body_img.get_rect(midbottom=(width // 2, height))
        composite.blit(body_img, body_rect)
        
        # Dibujar Head
        head_img = self.parts.get('head')
        if head_img:
            head_rect = head_img.get_rect(midbottom=(width // 2, body_rect.top + height * 0.1)) 
            composite.blit(head_img, head_rect)
            
            # Dibujar Hat
            hat_img = self.parts.get('hat')
            if hat_img:
                hat_rect = hat_img.get_rect(midbottom=(width // 2, head_rect.top + height * 0.05))
                composite.blit(hat_img, hat_rect)

        return composite

    def update(self, dt):
        """Actualiza el estado (y las partes si han cambiado)."""
        # Verificamos si los assets externos han cambiado y regeneramos la imagen si es necesario
        self._load_parts() 
        self.image = self._create_composite_image()
        
    def draw(self, screen):
        """Dibuja el jugador en la pantalla."""
        self.rect.midbottom = (int(self.x), int(self.y))
        screen.blit(self.image, self.rect)