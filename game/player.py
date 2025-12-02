import pygame
from settings import load_image, SCREEN_WIDTH, SCREEN_HEIGHT # ¡CORRECCIÓN: Se agrega SCREEN_HEIGHT!
import os 

class Player:
    """
    Player: dibuja al alumno con cuerpo, cabeza y sombrero.
    Maneja la posición (self.x) para el side-scrolling.
    """

    def __init__(self, body, head, hat):
        
        # Factor de escala AJUSTADO (Reducido a 0.25 para un personaje más pequeño)
        self.scale_factor = 0.25 
        
        # Carga y Escalado de imágenes
        # Los argumentos aquí son SÓLO los nombres de archivo (ej: "cat body.png")
        self.body_img = self._load_and_scale_asset("bodies", body)
        self.head_img = self._load_and_scale_asset("heads", head)
        self.hat_img = self._load_and_scale_asset("hats", hat)
        
        # Offsets consistentes (ajustados a la nueva escala)
        
        # CORRECCIÓN CABEZA: Aumentamos el valor base a -180 para forzar más solapamiento.
        # Offset de la cabeza: -180 (base) * 0.25 = -45
        self.head_offset_from_body = -180 * self.scale_factor
        
        # Offset del sombrero: -180 (más profundo) * 0.25 = -45
        self.hat_offset_from_head = -180 * self.scale_factor

        # Posición inicial del jugador 
        self.x = SCREEN_WIDTH // 2
        # CORRECCIÓN SUELO: Ajustamos Y para que esté a 100 píxeles del borde inferior. 
        # Esto suele ser más preciso para que el personaje se vea "en el suelo" del fondo.
        self.y = SCREEN_HEIGHT - 100 

        self.speed = 4 

    def _load_and_scale_asset(self, folder, filename):
        """
        Loads and scales an image using the two-argument load_image function.
        """
        if not filename:
            return None
            
        # Llamada CORREGIDA a load_image con los dos argumentos.
        image = load_image(folder, filename)
        
        # Safety check to ensure it's a surface before scaling
        if image and isinstance(image, pygame.Surface): 
            width = int(image.get_width() * self.scale_factor)
            height = int(image.get_height() * self.scale_factor)
            return pygame.transform.scale(image, (width, height))
            
        return None # Returns None if loading failed


    def move(self, direction):
        """Mueve al jugador (y al fondo) izquierda o derecha."""
        self.x += direction * self.speed

    def draw(self, screen):
        # Si no hay cuerpo, no dibujamos
        if not self.body_img:
            return

        # ---- CUERPO ----
        # Position the body using midbottom to align with the ground (self.y)
        body_rect = self.body_img.get_rect(midbottom=(self.x, self.y))
        screen.blit(self.body_img, body_rect)

        # ---- CABEZA ----
        if self.head_img:
            head_x = body_rect.midtop[0]
            # Mueve la cabeza hacia arriba desde la base del cuello del cuerpo.
            # Al usar midbottom en la cabeza, el offset negativo la mueve más arriba.
            head_y = body_rect.midtop[1] + self.head_offset_from_body
            # Usamos midbottom para la cabeza para que el punto de unión (cuello) sea estable.
            head_rect = self.head_img.get_rect(midbottom=(head_x, head_y))
            screen.blit(self.head_img, head_rect)

            # ---- SOMBRERO ----
            if self.hat_img:
                hat_x = head_rect.midtop[0]
                # Mueve el sombrero hacia abajo desde el punto superior de la cabeza (midtop de head_rect)
                hat_y = head_rect.midtop[1] + self.hat_offset_from_head
                hat_rect = self.hat_img.get_rect(midbottom=(hat_x, hat_y))
                screen.blit(self.hat_img, hat_rect)