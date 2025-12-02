# scenes/closet.py (Versión final simplificada)

import pygame
from engine.scene_manager import Scene
from game.player import Player
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image
import os 

# (DraggableItem class se mantiene igual)
# (CONSTANTES se mantienen igual)

class ClosetScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.is_open = False
        
        # --- Fondos ---
        self.background_closed = pygame.transform.smoothscale(
            load_image("images/rooms", "closet.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) # Fondo inicial
        self.background_open = pygame.transform.smoothscale(
            load_image("images/rooms", "open closet.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) # Fondo al abrir
        
        # --- Personaje de Referencia (Outfit de customize.py) ---
        self.player = Player(
            state = game.state,
            x = OUTFIT_X_POS,
            ground_y = OUTFIT_Y_POS,
            character_height= OUTFIT_HEIGHT 
        )

        # ... (_load_ui_elements se mantiene) ...
        self.clothes_items = pygame.sprite.Group()


    def _load_clothes_items(self):
        """Carga la ropa amontonada en el centro de la pantalla."""
        self.clothes_items.empty()
        
        folder = 'clothes'; asset_type = 'clothes'
        
        # Posición central para amontonar la ropa
        center_x = SCREEN_WIDTH // 2 
        center_y = SCREEN_HEIGHT // 2
        
        asset_dir = os.path.join('assets', folder) 
        
        try:
            filenames = [f for f in os.listdir(asset_dir) if f.endswith('.png')]
            
            for i, filename in enumerate(filenames):
                # Offset para el efecto "amontonado"
                offset_x = (i % 3 - 1) * 30 
                offset_y = (i // 3 - 1) * 30
                
                item = DraggableItem(filename, folder, asset_type, 
                                     center_x + offset_x, center_y + offset_y,
                                     scale_factor=0.8)
                self.clothes_items.add(item)
                
        except FileNotFoundError:
            print(f"Error: No se encuentra el directorio de assets: {asset_dir}")


    # ================================================================
    def handle_input(self, event):
        # ... (Manejo de arrastre si abierto) ...
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if self.back_rect.collidepoint(mouse_pos):
                self.game.state.save()
                self.change_scene(NEXT_SCENE_NAME)

            # Transición de cerrado a abierto
            if not self.is_open and self.open_button_rect.collidepoint(mouse_pos):
                self.is_open = True
                self._load_clothes_items() # Carga la ropa


    # ================================================================
    def update(self, dt):
        if self.is_open:
            # (Lógica de soltar la ropa en el personaje y actualizar state.outfit_clothes)
            pass

    # ================================================================
    def draw(self, screen):

        if self.is_open:
            screen.blit(self.background_open, (0, 0)) # Muestra fondo abierto
            self.player.draw(screen, camera_x=0)
            self.clothes_items.draw(screen) # Muestra ropa amontonada
        else:
            screen.blit(self.background_closed, (0, 0)) # Muestra fondo cerrado
            screen.blit(self.open_button_img, self.open_button_rect)

        screen.blit(self.back_img, self.back_rect)