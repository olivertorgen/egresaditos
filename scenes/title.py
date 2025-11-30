# scenes/title.py

import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image

class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Carga de recursos reales de tu assets/
        # Usamos el fondo del video, ajustando la ruta
        background_img_orig = load_image('Egresaditos portada.gif') 
        
        # --- AJUSTE DE TAMAÑO DEL FONDO: Escalar la imagen para que coincida con el tamaño de la pantalla ---
        self.background_img = pygame.transform.scale(background_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Cargar el asset real del botón JUGAR
        play_button_img_orig = load_image('ui', 'button play.png')
        
        # --- AJUSTE DE TAMAÑO DEL BOTÓN: Redimensionar el botón a un 33% (dividido por 3) del original ---
        new_width = play_button_img_orig.get_width() // 3 # CAMBIADO DE // 2 A // 3
        new_height = play_button_img_orig.get_height() // 3 # CAMBIADO DE // 2 A // 3
        self.play_button_img = pygame.transform.scale(play_button_img_orig, (new_width, new_height))
        # Si sigue siendo grande, prueba a dividir por 4 (// 4).

        self.font = pygame.font.Font(None, 48)

        # Posicionamiento del botón
        # Centrar el botón en la parte inferior de la pantalla
        self.button_rect = self.play_button_img.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8)
        )

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                print("Iniciando personalización...")
                # Llama al Scene Manager para iniciar la transición y cargar CUSTOMIZE
                self.change_scene('CUSTOMIZE') 

    def update(self, dt):
        # Lógica de animación o efectos en el título
        pass

    def draw(self, screen):
        # 1. Dibujar fondo de la portada (Ahora escalado a la pantalla)
        screen.blit(self.background_img, (0, 0))
        
        # 2. Dibujar botón de Play (usando el asset redimensionado)
        screen.blit(self.play_button_img, self.button_rect)