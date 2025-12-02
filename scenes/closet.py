import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, get_asset_path
from engine.scene_manager import Scene
from engine.ui import Button
from game.player import Player, CHARACTER_HEIGHT # Importamos la clase Player y la constante CHARACTER_HEIGHT

# La posición Y en el suelo (0.9 de la altura de la pantalla, como en Player)
GROUND_Y = SCREEN_HEIGHT * 0.9

class DraggableItem:
    """Clase simple para manejar un item de vestuario arrastrable."""
    def __init__(self, asset_name, asset_type, image, center_pos):
        self.asset_name = asset_name
        self.asset_type = asset_type  # Ejemplo: 'hat', 'body', 'head'
        self.original_center = center_pos
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.is_dragging = False

    def handle_event(self, event):
        """Maneja los eventos de drag."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.mouse_offset_x = self.rect.x - event.pos[0]
                self.mouse_offset_y = self.rect.y - event.pos[1]
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.rect.x = event.pos[0] + self.mouse_offset_x
                self.rect.y = event.pos[1] + self.mouse_offset_y
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        return False
    
    def reset_position(self):
        """Devuelve el item a su posición original."""
        self.rect.center = self.original_center

    def draw(self, screen):
        """Dibuja el item."""
        screen.blit(self.image, self.rect)


class ClosetScene(Scene): # Renombramos la clase a ClosetScene
    def __init__(self, game):
        super().__init__(game)
        self.state = self.game.state
        
        # Estado de la escena
        self.closet_open = False
        
        # =================================================================
        # 1. Fondos y Escalado
        # =================================================================
        self.background_closed_img = load_image("images/rooms", "closet.png")
        self.background_open_img = load_image("images/rooms", "open closet.png")
        
        self.background_closed = self._scale_background(self.background_closed_img)
        self.background_open = self._scale_background(self.background_open_img)
        
        # Posición X del fondo (centrado)
        self.bg_x = (SCREEN_WIDTH - self.background_closed.get_width()) // 2
        
        # =================================================================
        # 2. Player
        # =================================================================
        outfit = self.state.get_outfit_assets()
        self.player = Player(
            body=outfit.get('body'),
            head=outfit.get('head'),
            hat=outfit.get('hat')
        )
        # Personaje a 0.9 sobre el suelo y en la parte izquierda
        self.player.x = SCREEN_WIDTH // 4 
        self.player.y = GROUND_Y 
        
        # =================================================================
        # 3. Botones y Drag and Drop
        # =================================================================
        font = pygame.font.Font(None, 32)
        
        # Botón para Abrir/Cerrar el armario
        self.btn_toggle_closet = Button(
            rect=(SCREEN_WIDTH - 220, SCREEN_HEIGHT // 2 - 50, 180, 50),
            text="Abrir armario",
            font=font,
            callback=self.toggle_closet
        )
        
        # Botón para volver al cuarto
        self.btn_go_room = Button(
            rect=(40, SCREEN_HEIGHT - 70, 150, 50),
            text="Volver al cuarto",
            font=font,
            callback=self.go_room
        )

        self.buttons = [self.btn_toggle_closet, self.btn_go_room]
        
        # Items arrastrables (solo hats de ejemplo)
        self.draggable_items = self._setup_draggable_items()

        # Variables de D&D
        self.dragging_item = None
        self.player_rect_global = None # Se calcula en draw

    def _scale_background(self, img):
        """Escala la imagen para cubrir la pantalla sin estirar."""
        original_width = img.get_width()
        original_height = img.get_height()
        
        # Factor de escala basado en la altura de la pantalla
        scale_ratio = SCREEN_HEIGHT / original_height
        
        # Si la imagen escalada es más angosta que la pantalla, escalamos por ancho
        if original_width * scale_ratio < SCREEN_WIDTH:
             scale_ratio = SCREEN_WIDTH / original_width
        
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio) 
        
        return pygame.transform.scale(img, (new_width, new_height))

    def _setup_draggable_items(self):
        """Configura los items de vestuario disponibles."""
        items = []
        # Lista de assets de sombreros disponibles (ASSETS DE EJEMPLO)
        hat_assets = ["hat wizard.png", "hat santa claus.png", "hat graduation.png"]
        
        # Posición de inicio de los items (dentro del armario abierto)
        # Lo movemos ligeramente a la derecha para que no se superponga con el personaje
        x_start = SCREEN_WIDTH // 2 + 50
        y_pos = SCREEN_HEIGHT // 4
        x_spacing = 100

        for i, asset_name in enumerate(hat_assets):
            # Cargar imagen y escalar (asumiendo que los assets de hats están en 'hats')
            hat_img = load_image('hats', asset_name)
            # Escalar el item a un tamaño razonable para el inventario
            scale = 0.8 
            scaled_img = pygame.transform.scale(
                hat_img,
                (int(hat_img.get_width() * scale), int(hat_img.get_height() * scale))
            )

            item = DraggableItem(
                asset_name=asset_name, 
                asset_type='hat', 
                image=scaled_img, 
                center_pos=(x_start + i * x_spacing, y_pos)
            )
            items.append(item)
        return items

    # ===========================
    # CAMBIO DE ESTADO
    # ===========================
    def toggle_closet(self):
        """Cambia el estado del armario y el texto del botón."""
        self.closet_open = not self.closet_open
        if self.closet_open:
            self.btn_toggle_closet.text = "Cerrar armario"
            self.btn_toggle_closet.text_surface = self.btn_toggle_closet.font.render("Cerrar armario", True, (20, 20, 20))
        else:
            self.btn_toggle_closet.text = "Abrir armario"
            self.btn_toggle_closet.text_surface = self.btn_toggle_closet.font.render("Abrir armario", True, (20, 20, 20))

    def go_room(self):
        """Transición a la escena del cuarto."""
        self.game.current_scene.change_scene("ROOM")

    # ===========================
    # MANEJO DE INPUTS
    # ===========================
    def handle_input(self, event):
        # 1. Botones (Solo si no estamos arrastrando)
        if not self.dragging_item:
            for btn in self.buttons:
                if btn.handle_event(event):
                    if event.type == pygame.MOUSEBUTTONDOWN and self.game.can_click:
                        btn.callback()
                        self.game.can_click = False

        # 2. Drag and Drop (Solo si el armario está abierto)
        if self.closet_open:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Intenta iniciar arrastre
                # Recorrer en orden inverso para que el elemento dibujado encima sea el primero en ser arrastrado
                for item in reversed(self.draggable_items): 
                    if item.handle_event(event):
                        self.dragging_item = item
                        # Mover el item arrastrado al final de la lista para dibujarlo encima
                        self.draggable_items.remove(item)
                        self.draggable_items.append(item)
                        break
            
            elif event.type == pygame.MOUSEMOTION and self.dragging_item:
                # Mover el item arrastrado
                self.dragging_item.handle_event(event)
            
            elif event.type == pygame.MOUSEBUTTONUP and self.dragging_item:
                # Finalizar arrastre y comprobar colisión
                self.dragging_item.handle_event(event)
                self._check_drop()
                self.dragging_item = None
    
    def _check_drop(self):
        """Comprueba si el item arrastrado se ha soltado sobre el personaje."""
        item = self.dragging_item
        
        # Calculamos la posición real de la cabeza (aproximada para colisión)
        # Usamos CHARACTER_HEIGHT importada.
        player_head_x = self.player.x
        # La cabeza está en el 80% de la altura total del personaje desde el suelo
        player_head_y = self.player.y - CHARACTER_HEIGHT * 0.8 
        
        # Creamos un rectángulo de colisión pequeño alrededor de la cabeza
        player_head_rect = pygame.Rect(0, 0, 80, 80)
        player_head_rect.center = (int(player_head_x), int(player_head_y))


        if item.rect.colliderect(player_head_rect):
            # Si colisiona y es un sombrero, equiparlo
            if item.asset_type == 'hat':
                print(f"Equipando sombrero: {item.asset_name}")
                self.state.set_outfit_part('hat', item.asset_name)
                # Actualizar el objeto player de la escena con el nuevo asset
                self.player.hat_asset = item.asset_name
        
        # En cualquier caso, volver a su posición original
        item.reset_position()

    # ===========================
    # UPDATE
    # ===========================
    def update(self, dt):
        # Actualizar el player (solo para gravedad/salto si estuviera activo)
        self.player.update(dt) 
        pass

    # ===========================
    # DRAW
    # ===========================
    def draw(self, screen):
        # Dibujar el fondo correcto
        if self.closet_open:
            background = self.background_open
        else:
            background = self.background_closed
            
        screen.blit(background, (self.bg_x, 0))

        # Dibuja el personaje
        self.player.draw(screen)

        # Dibujar el área objetivo (círculo) para saber dónde soltar el sombrero, solo si el armario está abierto
        if self.closet_open:
            player_head_x = int(self.player.x)
            player_head_y = int(self.player.y - CHARACTER_HEIGHT * 0.8)
            # Dibujamos un círculo semitransparente para guiar al usuario
            target_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(target_surface, (255, 100, 100, 150), (40, 40), 40)
            
            screen.blit(target_surface, (player_head_x - 40, player_head_y - 40))


        # Dibuja los items arrastrables si el armario está abierto
        if self.closet_open:
            for item in self.draggable_items:
                # El item arrastrado se dibuja al final para la capa superior,
                # pero ya está al final de la lista, así que simplemente dibujamos todo
                item.draw(screen)
            
        # Dibuja los botones
        for btn in self.buttons:
            btn.draw(screen)