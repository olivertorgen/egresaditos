# scenes/kitchen.py

import pygame
from engine.scene_manager import Scene
from game.player import Player
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image

# --- CONSTANTES DE LA ESCENA ---
CHARACTER_HEIGHT = 200
CHARACTER_DEFAULT_X = int(SCREEN_WIDTH * 0.25)
CHARACTER_GROUND_Y = int(SCREEN_HEIGHT * 0.98)
FRIDGE_HOTSPOT_X = int(SCREEN_WIDTH * 0.8)
BACKPACK_HOTSPOT_X = int(SCREEN_WIDTH * 0.6)

class KitchenScene(Scene):

    def __init__(self, game):
        super().__init__(game)
        
        # ... (Fondo: kitchen.png, UI, Hotspots se mantienen) ...
        img = load_image("images/rooms", "kitchen.png")
        self.background_img = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # --- Inicialización del personaje (carga outfit y posición) ---
        initial_x = self.game.state.player_x if self.game.state.player_x != 0.0 else CHARACTER_DEFAULT_X
        
        self.player = Player(
            state = game.state,
            x = initial_x,
            ground_y = CHARACTER_GROUND_Y,
            character_height= CHARACTER_HEIGHT
        )
        self.game.state.player_y = CHARACTER_GROUND_Y

        # ... (Hotspots, _load_ui_elements se mantienen) ...


    # ================================================================
    def handle_input(self, event):
        # ... (Lógica de Volver a ROOM, Abrir menús se mantiene. AHORA GUARDA POSICIÓN al salir) ...
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if self.back_rect.collidepoint(mouse_pos):
                self.game.state.player_x = self.player.x # GUARDAR POSICIÓN
                self.change_scene("ROOM")
            # ... (Lógica de menús se mantiene) ...
            
    # ================================================================
    def update(self, dt):
        
        if self.current_menu: return

        # --- Movimiento Local del Jugador ---
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt, world_min_x=50, world_max_x=SCREEN_WIDTH - 50) 
        
        # ... (Detección de Hotspots se mantiene) ...

    # ================================================================
    def draw(self, screen):
        # ... (Dibujo de fondo, jugador (camera_x=0), UI y Menús se mantiene) ...
        pass