# scenes/closet.py

import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image

# --- Configuración de Escena ---
DIALOGUE_TEXT = "¡Elige tu mejor atuendo para la última semana!"
NEXT_SCENE_NAME = 'LIVING_ROOM' 

# --- Configuración Visual del Personaje (Mantenemos la consistencia) ---
CHARACTER_HEIGHT = 200
CHARACTER_POSITION_X = SCREEN_WIDTH * 0.40  # Posición central del personaje
CHARACTER_POSITION_Y = SCREEN_HEIGHT * 0.7  # Posición en el "suelo"

# --- Partes Fijas del Personaje (Necesario para la carga de assets) ---
CHARACTER_PARTS = {
    'body': [
        'bow cat body.png', 'cat body.png', 'dragon body.png', 'oshawott body.png', 'raichu body.png'
    ],
    'head': [
        'cat head.png', 'cloud head.png', 'pingu head.png', 'pitaya head.png', 'raichu head.png', 'shark cat head.png'
    ],
    'hat': [
        'None', 'hat graduation.png', 'hat santa claus.png', 'hat wizard.png'
    ], 
}

# --- Ropa Disponible (Assets de 'assets/clothes') ---
CLOTHING_ASSETS = [
    'black and white sweater.png',
    'shirt charly garcia.png',
    'shirt soda estereo.png',
    'shirt spider punk.png',
    'starry sweater.png',
    'stripped sweater.png',
]

class DraggableItem(pygame.sprite.Sprite):
    """Clase para la ropa arrastrable."""
    def __init__(self, filename, initial_pos, scale_factor):
        super().__init__()
        # La ropa se encuentra en la subcarpeta 'clothes'
        original_image = load_image('clothes', filename)
        
        # Redimensionar la imagen (ej: 100x100)
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(topleft=initial_pos)
        self.original_pos = initial_pos
        self.dragging = False
        self.filename = filename

    def update(self, mouse_pos):
        if self.dragging:
            # Centrar el ítem bajo el cursor mientras se arrastra
            self.rect.center = mouse_pos

    def start_drag(self):
        self.dragging = True

    def end_drag(self):
        self.dragging = False
        # Aquí puedes añadir lógica para verificar si se soltó sobre el personaje
        
    def reset_position(self):
        self.rect.topleft = self.original_pos


class ClosetOutfitScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        self.font_large = pygame.font.Font(None, 48) 
        self.font_medium = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_COLOR = (0, 150, 0) # Verde para avanzar
        self.BUTTON_HOVER_COLOR = (0, 180, 0)
        
        # 1. Cargar fondo del armario
        try:
            # Usar 'images/rooms/closet.png' según el árbol de archivos
            background_img_orig = load_image('images/rooms', 'closet.png') 
            self.background_img = pygame.transform.scale(background_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("ADVERTENCIA: Fondo 'closet.png' no encontrado. Usando fondo negro.")
            self.background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_img.fill(self.BLACK)

        # 2. Cargar assets del personaje (para mostrar el maniquí)
        self.player_name = self.game.state.player_name
        self.character_body_filename = self.game.state.character_body
        self.character_head_filename = self.game.state.character_head
        self.character_hat_filename = self.game.state.character_hat
        self.character_assets = self._load_character_assets()
        
        # 3. Inicializar los ítems de ropa arrastrables
        self.clothing_items = pygame.sprite.Group()
        self.drag_scale_factor = 0.5 # Factor de escala para la ropa que se arrastra
        self._setup_clothing_items()
        
        # 4. Estado de arrastre
        self.current_drag_item = None
        self.selected_outfit = None # Almacena la imagen del outfit seleccionado

        # 5. Botón de Confirmación
        self.button_text_content = "Listo para salir"
        self.button_rect = pygame.Rect(0, 0, 300, 60)
        self.button_rect.center = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9)
        self.is_hovering = False


    # --- Métodos de Carga de Assets ---
    def _get_asset_path_key(self, part_filename):
        if part_filename in CHARACTER_PARTS['body']: return 'bodies'
        if part_filename in CHARACTER_PARTS['head']: return 'heads'
        if part_filename in CHARACTER_PARTS['hat']: return 'hats'
        return 'ui' 

    def _load_character_assets(self):
        """Carga y escala las partes base del personaje."""
        assets = {}
        body_img_orig = load_image(self._get_asset_path_key(self.character_body_filename), self.character_body_filename)
        scale_factor = CHARACTER_HEIGHT / body_img_orig.get_height()
        new_width = int(body_img_orig.get_width() * scale_factor)
        
        body_img = pygame.transform.scale(body_img_orig, (new_width, CHARACTER_HEIGHT))
        assets['body'] = body_img
        
        head_img_orig = load_image(self._get_asset_path_key(self.character_head_filename), self.character_head_filename)
        head_img = pygame.transform.scale(head_img_orig, 
                                            (int(head_img_orig.get_width() * scale_factor), 
                                             int(head_img_orig.get_height() * scale_factor)))
        assets['head'] = head_img

        if self.character_hat_filename and self.character_hat_filename != 'None':
            hat_img_orig = load_image(self._get_asset_path_key(self.character_hat_filename), self.character_hat_filename)
            hat_img = pygame.transform.scale(hat_img_orig, 
                                                (int(hat_img_orig.get_width() * scale_factor), 
                                                 int(hat_img_orig.get_height() * scale_factor)))
            assets['hat'] = hat_img
            
        return assets
    
    def _setup_clothing_items(self):
        """Coloca los ítems de ropa a la izquierda de la pantalla, como si estuvieran en el closet."""
        x_start = SCREEN_WIDTH * 0.60
        y_start = SCREEN_HEIGHT * 0.20
        y_spacing = 70  # Espacio vertical entre ítems
        item_scale = 0.6  # Escala visual de los ítems en el "inventario"
        
        for i, filename in enumerate(CLOTHING_ASSETS):
            pos = (x_start, y_start + i * y_spacing)
            item = DraggableItem(filename, pos, item_scale)
            self.clothing_items.add(item)


    # --- Métodos de Interacción ---
    def handle_input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Iniciar el arrastre
            if self.current_drag_item is None:
                for item in self.clothing_items:
                    if item.rect.collidepoint(mouse_pos):
                        self.current_drag_item = item
                        self.current_drag_item.start_drag()
                        
            # Clic en el botón
            if self.button_rect.collidepoint(event.pos) and self.selected_outfit:
                # Guardar el outfit seleccionado y avanzar
                self.game.state.selected_outfit = self.current_drag_item.filename # Guarda el nombre del archivo
                print(f"Outfit seleccionado: {self.game.state.selected_outfit}. Cambiando a {NEXT_SCENE_NAME}.")
                self.change_scene(NEXT_SCENE_NAME)


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Finalizar el arrastre
            if self.current_drag_item:
                target_rect = self.get_character_target_rect()
                
                if target_rect.colliderect(self.current_drag_item.rect):
                    # Ropa aplicada exitosamente: seleccionar el outfit
                    self.selected_outfit = self.current_drag_item.image
                    self.game.state.selected_outfit_filename = self.current_drag_item.filename
                    self.current_drag_item.reset_position() # Opcional: desaparecer el ítem arrastrado
                else:
                    # Soltado fuera del área, regresa a la posición original
                    self.current_drag_item.reset_position()
                    
                self.current_drag_item.end_drag()
                self.current_drag_item = None
                
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar la posición del ítem arrastrado
        if self.current_drag_item:
            self.current_drag_item.update(mouse_pos)
        
        # Actualizar el estado de hover del botón
        self.is_hovering = self.button_rect.collidepoint(mouse_pos)

    # --- Métodos de Dibujo ---
    def get_character_target_rect(self):
        """Calcula el área del cuerpo donde se debe soltar la ropa."""
        x = CHARACTER_POSITION_X
        y = CHARACTER_POSITION_Y
        
        # El área de "drop" es alrededor del cuerpo, un poco más arriba
        target_rect = pygame.Rect(0, 0, CHARACTER_HEIGHT * 0.8, CHARACTER_HEIGHT * 0.8)
        target_rect.center = (x, y - CHARACTER_HEIGHT * 0.4)
        return target_rect

    def _draw_composed_character(self, screen):
        """Dibuja las partes base del personaje (maniquí)."""
        x = CHARACTER_POSITION_X
        y = CHARACTER_POSITION_Y
        
        # Dibuja el cuerpo base
        body_img = self.character_assets['body']
        body_rect = body_img.get_rect(midbottom=(x, y)) 
        screen.blit(body_img, body_rect)
        
        head_offset_x = x 
        head_offset_y = body_rect.y 
        
        # Dibuja la cabeza
        head_img = self.character_assets['head']
        head_rect = head_img.get_rect(midbottom=(head_offset_x, head_offset_y + 50)) 
        screen.blit(head_img, head_rect)

        # Dibuja el sombrero (si existe)
        if 'hat' in self.character_assets:
            hat_img = self.character_assets['hat']
            hat_offset_y = head_rect.y + 90 
            hat_rect = hat_img.get_rect(midbottom=(head_offset_x, hat_offset_y))
            screen.blit(hat_img, hat_rect)
            
        # Dibuja el outfit seleccionado encima del cuerpo
        if self.selected_outfit:
            # Aquí necesitamos escalar la imagen del outfit al tamaño del cuerpo (CHARACTER_HEIGHT)
            # Para simplificar, asumiremos que el outfit ya se ajusta al cuerpo y usamos el rect del cuerpo como base.
            outfit_rect = self.selected_outfit.get_rect(center=(body_rect.centerx, body_rect.centery + 40))
            screen.blit(self.selected_outfit, outfit_rect)

    def _draw_dialogue(self, screen):
        """Dibuja el cuadro de diálogo superior."""
        # Fondo semi-transparente para la caja de diálogo
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 0.15), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        dialogue_surface = self.font_large.render(DIALOGUE_TEXT, True, self.WHITE)
        dialogue_rect = dialogue_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.075))
        screen.blit(dialogue_surface, dialogue_rect)

    def _draw_button(self, screen):
        """Dibuja el botón de acción."""
        
        current_color = self.BUTTON_HOVER_COLOR if self.is_hovering else self.BUTTON_COLOR
        # El botón solo se habilita si hay un outfit seleccionado
        if not self.selected_outfit:
            current_color = (100, 100, 100) # Gris deshabilitado
            
        pygame.draw.rect(screen, current_color, self.button_rect, border_radius=15)
        
        button_surface = self.font_large.render(self.button_text_content, True, self.WHITE)
        button_rect_center = button_surface.get_rect(center=self.button_rect.center)
        screen.blit(button_surface, button_rect_center)

    def draw(self, screen):
        # 1. Dibujar el fondo
        screen.blit(self.background_img, (0, 0))
        
        # 2. Dibujar el personaje (maniquí)
        self._draw_composed_character(screen)
        
        # 3. Dibujar la ropa disponible (excepto el que se está arrastrando)
        for item in self.clothing_items:
            if item != self.current_drag_item:
                screen.blit(item.image, item.rect)
                
        # 4. Dibujar el diálogo
        self._draw_dialogue(screen)
        
        # 5. Dibujar el botón
        self._draw_button(screen)
        
        # 6. Dibujar el ítem arrastrado al final (para que esté siempre encima)
        if self.current_drag_item:
            screen.blit(self.current_drag_item.image, self.current_drag_item.rect)
            
        # Dibujar una guía para el área de drop (Solo para debugging, puedes eliminarlo después)
        # target_rect = self.get_character_target_rect()
        # pygame.draw.rect(screen, (255, 0, 0), target_rect, 2)