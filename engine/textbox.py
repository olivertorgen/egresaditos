# engine/textbox.py

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TextBox:
    def __init__(self, x, y, w, h, font, max_length=15, initial_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255) # Blanco para el texto
        self.box_color = (30, 30, 30) # Gris oscuro para el fondo
        self.active_color = (50, 50, 50) # Color cuando está activo
        self.font = font
        self.text = initial_text
        self.max_length = max_length
        self.active = False # Indica si está listo para recibir input
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el clic fue dentro de la caja, activarla
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.box_color = self.active_color
            else:
                self.active = False
                self.box_color = (30, 30, 30)
                
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Solo aceptar el input si no excede la longitud máxima
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def draw(self, screen):
        # Dibujar el rectángulo de fondo
        pygame.draw.rect(screen, self.box_color, self.rect)
        
        # Dibujar el borde
        pygame.draw.rect(screen, self.color, self.rect, 2) 

        # Renderizar el texto
        txt_surface = self.font.render(self.text, True, self.color)
        
        # Dibujar el texto y centrarlo verticalmente
        text_y = self.rect.centery - txt_surface.get_height() // 2
        screen.blit(txt_surface, (self.rect.x + 5, text_y))