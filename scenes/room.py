# scenes/room.py

import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image

# --- Configuración de Escena y Estado ---
DIALOGUE_TEXT = "Es la última semana de clases. Vamos a prepararnos!"
NEXT_SCENE_NAME = 'CLOSET_OUTFIT' 

# --- Partes de Personaje (Definición necesaria para la lógica de carga de assets) ---
CHARACTER_PARTS = {
    'body': [
        'bow cat body.png',
        'cat body.png', 
        'dragon body.png', 
        'oshawott body.png', 
        'raichu body.png'
    ],
    'head': [
        'cat head.png', 
        'cloud head.png', 
        'pingu head.png', 
        'pitaya head.png', 
        'raichu head.png',
        'shark cat head.png'
    ],
    'hat': [
        'None', 
        'hat graduation.png',
        'hat santa claus.png',
        'hat wizard.png'
    ], 
}

# --- Configuración Visual del Personaje en la Habitación ---
CHARACTER_HEIGHT = 200 # Un poco más pequeño para que quepa bien en la habitación
CHARACTER_POSITION_X = SCREEN_WIDTH * 0.25 # Posición a la izquierda, cerca del centro vertical
CHARACTER_POSITION_Y = SCREEN_HEIGHT * 0.7 # Posición en el "suelo" de la habitación

class RoomScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Fuentes y Colores
        self.font_large = pygame.font.Font(None, 48) 
        self.font_medium = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_COLOR = (120, 80, 200) # Morado oscuro para el botón
        self.BUTTON_HOVER_COLOR = (150, 110, 230)
        
        # 1. Cargar y escalar el fondo de la habitación
        try:
            background_img_orig = load_image('images/rooms', 'night room.png') 
            self.background_img = pygame.transform.scale(background_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("ADVERTENCIA: Fondo 'night room.png' no encontrado. Usando fondo negro.")
            self.background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_img.fill(self.BLACK)

        # 2. Obtener los datos del personaje guardados en GameState
        self.player_name = self.game.state.player_name
        self.character_body_filename = self.game.state.character_body
        self.character_head_filename = self.game.state.character_head
        self.character_hat_filename = self.game.state.character_hat
        
        # 3. Cargar y almacenar las imágenes del personaje ya escaladas
        self.character_assets = self._load_character_assets()

        # --- Lógica de Estado de la Habitación ---
        self.room_state = 'DIALOGUE' # Estados: 'DIALOGUE', 'BUTTON_READY'
        self.dialogue_time = 0.0
        self.dialogue_duration = 3.0 # Duración mínima del diálogo antes de que aparezca el botón automáticamente
        
        # --- Configuración del Botón ---
        self.button_text_content = "Ir a elegir ropa"
        self.button_rect = pygame.Rect(0, 0, 400, 80)
        self.button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.9)
        self.is_hovering = False

    def _get_asset_path_key(self, part_filename):
        """
        Devuelve la ruta de la subcarpeta del asset basada en el nombre del archivo.
        """
        if part_filename in CHARACTER_PARTS['body']:
            return 'bodies'
        elif part_filename in CHARACTER_PARTS['head']: 
            return 'heads'
        elif part_filename in CHARACTER_PARTS['hat']:   
            return 'hats'
        return 'ui' 

    def _load_character_assets(self):
        """
        Carga, escala y almacena todas las partes del personaje de una vez.
        El escalado se basa en CHARACTER_HEIGHT para mantener la consistencia.
        """
        assets = {}
        
        # --- Lógica de Escalado Base (Basada en el cuerpo) ---
        body_img_orig = load_image(self._get_asset_path_key(self.character_body_filename), self.character_body_filename)
        
        # Calcula el factor de escala y el nuevo ancho
        scale_factor = CHARACTER_HEIGHT / body_img_orig.get_height()
        new_width = int(body_img_orig.get_width() * scale_factor)
        
        # 1. Cuerpo
        body_img = pygame.transform.scale(body_img_orig, (new_width, CHARACTER_HEIGHT))
        assets['body'] = body_img
        
        # 2. Cabeza
        head_img_orig = load_image(self._get_asset_path_key(self.character_head_filename), self.character_head_filename)
        head_img = pygame.transform.scale(head_img_orig, 
                                            (int(head_img_orig.get_width() * scale_factor), 
                                             int(head_img_orig.get_height() * scale_factor)))
        assets['head'] = head_img

        # 3. Sombrero (Condicional)
        if self.character_hat_filename and self.character_hat_filename != 'None':
            hat_img_orig = load_image(self._get_asset_path_key(self.character_hat_filename), self.character_hat_filename)
            hat_img = pygame.transform.scale(hat_img_orig, 
                                                (int(hat_img_orig.get_width() * scale_factor), 
                                                 int(hat_img_orig.get_height() * scale_factor)))
            assets['hat'] = hat_img
            
        return assets

    def handle_input(self, event):
        # Permite volver al menú de título con ESC (para pruebas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Volviendo a Title Scene...")
            self.change_scene('TITLE')
        
        # Lógica de transición de estado/botón
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.room_state == 'DIALOGUE':
                # Salta el diálogo inmediatamente y avanza al estado del botón
                self.room_state = 'BUTTON_READY'
            elif self.room_state == 'BUTTON_READY':
                # Verifica si se hizo clic en el botón
                if self.button_rect.collidepoint(event.pos):
                    print(f"Cambiando a escena de vestuario: {NEXT_SCENE_NAME}")
                    self.change_scene(NEXT_SCENE_NAME)

    def update(self, dt):
        if self.room_state == 'DIALOGUE':
            self.dialogue_time += dt
            # Transición automática al estado del botón si se cumple la duración
            if self.dialogue_time >= self.dialogue_duration:
                self.room_state = 'BUTTON_READY'
        
        # Actualiza el estado de hover del botón si está listo
        if self.room_state == 'BUTTON_READY':
            mouse_pos = pygame.mouse.get_pos()
            self.is_hovering = self.button_rect.collidepoint(mouse_pos)

    def _draw_composed_character(self, screen):
        """Dibuja las partes del personaje guardadas en la posición de la habitación."""
        
        x = CHARACTER_POSITION_X
        y = CHARACTER_POSITION_Y
        
        # 1. Cuerpo
        body_img = self.character_assets['body']
        # Usamos midbottom para anclarlo al suelo (Y)
        body_rect = body_img.get_rect(midbottom=(x, y)) 
        screen.blit(body_img, body_rect)
        
        # Posición base para la cabeza y sombrero (anclada a la parte superior del cuerpo)
        head_offset_x = x 
        head_offset_y = body_rect.y 
        
        # 2. Cabeza
        head_img = self.character_assets['head']
        # AJUSTE: Offset de superposición para posicionar la cabeza correctamente
        head_rect = head_img.get_rect(midbottom=(head_offset_x, head_offset_y + 50)) 
        screen.blit(head_img, head_rect)

        # 3. Sombrero (Condicional)
        if 'hat' in self.character_assets:
            hat_img = self.character_assets['hat']
            # AJUSTE: Offset de superposición para posicionar el sombrero correctamente
            hat_offset_y = head_rect.y + 90 
            hat_rect = hat_img.get_rect(midbottom=(head_offset_x, hat_offset_y))
            screen.blit(hat_img, hat_rect)

        # Dibuja el nombre del jugador encima del personaje
        name_text = self.font_large.render(self.player_name, True, self.WHITE)
        name_rect = name_text.get_rect(center=(CHARACTER_POSITION_X, CHARACTER_POSITION_Y - CHARACTER_HEIGHT - 30))
        screen.blit(name_text, name_rect)

    def _draw_dialogue(self, screen):
        """Dibuja el cuadro de diálogo en la parte inferior."""
        
        # Fondo semi-transparente para la caja de diálogo
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 0.25), pygame.SRCALPHA)  # Superficie con alfa
        s.fill((0, 0, 0, 180))  # Color negro semi-transparente
        screen.blit(s, (0, SCREEN_HEIGHT * 0.75))

        # Texto del jugador (Nombre)
        name_text_dialogue = self.font_medium.render(self.player_name, True, self.WHITE)
        screen.blit(name_text_dialogue, (50, SCREEN_HEIGHT * 0.77))
        
        # Texto del diálogo
        dialogue_surface = self.font_large.render(DIALOGUE_TEXT, True, self.WHITE)
        dialogue_rect = dialogue_surface.get_rect(midleft=(50, SCREEN_HEIGHT * 0.85))
        screen.blit(dialogue_surface, dialogue_rect)

    def _draw_button(self, screen):
        """Dibuja el botón de acción en el centro inferior."""
        
        # Dibuja el fondo del botón con esquinas redondeadas (simulado con rectángulos)
        current_color = self.BUTTON_HOVER_COLOR if self.is_hovering else self.BUTTON_COLOR
        pygame.draw.rect(screen, current_color, self.button_rect, border_radius=15)
        
        # Dibuja el texto del botón
        button_surface = self.font_large.render(self.button_text_content, True, self.WHITE)
        button_rect_center = button_surface.get_rect(center=self.button_rect.center)
        screen.blit(button_surface, button_rect_center)


    def draw(self, screen):
        # 1. Dibujar el fondo
        screen.blit(self.background_img, (0, 0))
        
        # 2. Dibujar el personaje
        self._draw_composed_character(screen)
        
        # 3. Dibujar el estado actual
        if self.room_state == 'DIALOGUE':
            self._draw_dialogue(screen)
        elif self.room_state == 'BUTTON_READY':
            self._draw_button(screen)