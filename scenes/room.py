import pygame
import os
# Importamos explícitamente load_image, SCREEN_WIDTH y SCREEN_HEIGHT, y get_asset_path (aunque no se use directamente, es bueno tenerlo si lo usas en otro lado)
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, get_asset_path
from engine.scene_manager import Scene
from engine.ui import Button
from engine.narrator import Narrator
from game.player import Player 

# La carga se realiza directamente en __init__ para garantizar
# que load_image() sea llamada con los DOS argumentos requeridos.

class RoomScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        self.state = self.game.state

        # Fondo: CARGA DIRECTA CON DOS ARGUMENTOS
        self.background_img = load_image("images/rooms", "day room.png")
        
        # =================================================================
        # CORRECCIÓN DE FONDO: Ajustar la escala manteniendo la proporción 
        # y asegurando que cubra toda la altura.
        # =================================================================
        original_width = self.background_img.get_width()
        original_height = self.background_img.get_height()
        
        # Calcular el factor de escala basado en la altura de la pantalla (mantiene el aspecto)
        scale_ratio = SCREEN_HEIGHT / original_height
        
        # Si la imagen original es más angosta que la pantalla, aumentamos el factor de escala
        # para que la imagen sea al menos el doble del ancho de la pantalla (para scrolling)
        if original_width * scale_ratio < SCREEN_WIDTH:
             # Si es más angosta que la pantalla, la escalamos para que sea 2x el ancho de la pantalla
            scale_ratio = (SCREEN_WIDTH * 2) / original_width
        
        new_width = int(original_width * scale_ratio)
        new_height = SCREEN_HEIGHT # La altura siempre será la de la pantalla

        self.background = pygame.transform.scale(
            self.background_img, 
            (new_width, new_height) 
        )
        
        # La posición inicial del fondo: se centra la parte visible del fondo
        self.bg_x = - (new_width - SCREEN_WIDTH) // 2 
        
        # ===========================
        # PERSONAJE
        # ===========================
        outfit = self.state.get_outfit_assets()
        # Inicializamos el Player usando la data del estado
        self.player = Player(
            body=outfit.get('body'),
            head=outfit.get('head'),
            hat=outfit.get('hat')
        )
        # Posición inicial del jugador (centrado en la vista de la cámara)
        self.player.x = SCREEN_WIDTH // 2
        
        # ===========================
        # BOTONES
        # ===========================
        font = pygame.font.Font(None, 32)
        
        # Botón Armario: a la derecha de la escena
        self.btn_open_closet = Button(
            rect=(SCREEN_WIDTH - 220, SCREEN_HEIGHT // 2 - 50, 180, 50),
            text="Abrir armario",
            font=font,
            callback=self.go_closet
        )

        # Botón Cocina: a la izquierda de la escena
        self.btn_go_kitchen = Button(
            rect=(40, SCREEN_HEIGHT // 2 - 50, 180, 50),
            text="Ir a cocina",
            font=font,
            callback=self.go_kitchen
        )

        self.buttons = [self.btn_open_closet, self.btn_go_kitchen]

        # ===========================
        # NARRADOR
        # ===========================
        self.narrator = Narrator("narrative/script.json")


    # ===========================
    # CAMBIO DE ESCENAS
    # ===========================
    def go_closet(self):
        # Aseguramos que la transición se hace a través de change_scene
        self.game.current_scene.change_scene("CLOSET")

    def go_kitchen(self):
        # Aseguramos que la transición se hace a través de change_scene
        self.game.current_scene.change_scene("KITCHEN")


    # ===========================
    # MANEJO DE INPUTS (Event Delegation)
    # ===========================
    def handle_input(self, event):
        """Maneja los eventos para los botones."""
        
        # 1. Botones (Debounce controlado por self.game.can_click)
        for btn in self.buttons:
            # handle_event gestiona el hover y devuelve True si hay un MOUSEBUTTONDOWN
            if btn.handle_event(event): 
                # Si el evento es un click y el debounce está habilitado
                if event.type == pygame.MOUSEBUTTONDOWN and self.game.can_click:
                    # Llama al callback de la escena (go_closet/go_kitchen)
                    btn.callback()
                    # Deshabilita el click (debounce)
                    self.game.can_click = False 
    
    # ===========================
    # UPDATE
    # ===========================
    def update(self, dt):
        
        # --- Manejo de Inputs de Teclado (Continuos: Side-Scrolling) ---
        keys = pygame.key.get_pressed()
        direction = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction = -1 # Corrección de lógica: mover el personaje a la izquierda es -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction = 1 # Corrección de lógica: mover el personaje a la derecha es +1

        # Actualiza la posición X del jugador
        self.player.x += direction * self.player.speed
        
        # Limita la posición X del jugador
        # El jugador debe moverse en el rango de todo el fondo.
        min_x = SCREEN_WIDTH // 4 
        max_x = self.background.get_width() - SCREEN_WIDTH // 4 
        self.player.x = max(min(self.player.x, max_x), min_x)

        # Calcula la posición del fondo (simulando que la cámara sigue al jugador)
        # La posición del fondo es la mitad de la pantalla menos la posición del jugador
        self.bg_x = SCREEN_WIDTH // 2 - self.player.x
        
        # Limita la posición del fondo para que no se vea el borde negro
        max_bg_x = SCREEN_WIDTH - self.background.get_width()
        self.bg_x = max(min(0, self.bg_x), max_bg_x)
        
        # --- Narrador ---
        self.narrator.update(dt)


    # ===========================
    # DRAW
    # ===========================
    def draw(self, screen):
        # Dibuja el fondo
        screen.blit(self.background, (self.bg_x, 0))

        # Dibuja el personaje
        self.player.draw(screen)

        # Dibuja los botones 
        for btn in self.buttons:
            btn.draw(screen)

        # Dibuja el narrador
        narrator_pos = (40, SCREEN_HEIGHT - 140)
        self.narrator.draw(screen, narrator_pos)