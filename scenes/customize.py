# scenes/customize.py

import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image

# ==============================================================================
# CLASE AUXILIAR: TEXTBOX
# Necesaria para ingresar el nombre del personaje.
# ==============================================================================
class TextBox:
    def __init__(self, x, y, w, h, font, initial_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = initial_text
        self.font = font
        self.active = False
        self.txt_surface = self.font.render(self.text, True, pygame.Color('white'))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic sobre la caja
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Cambiar el color de la caja para indicar si está activa o no.
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Límite de caracteres
                    if len(self.text) < 15: 
                        self.text += event.unicode
                        
                # Re-renderizar el texto
                self.txt_surface = self.font.render(self.text, True, pygame.Color('white'))

    def draw(self, screen):
        # Dibujar el texto.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Dibujar el rectángulo.
        pygame.draw.rect(screen, self.color, self.rect, 2)
# ==============================================================================
# FIN CLASE TEXTBOX
# ==============================================================================


# --- Partes de Personaje (USANDO NOMBRES REALES) ---
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
    # --- CORRECCIÓN 2: Usamos los nombres reales de los archivos de sombreros ---
    'hat': [
        'None', 
        'hat graduation.png',
        'hat santa claus.png',
        'hat wizard.png'
    ], 
}

# --- Configuración Visual del Personaje ---
CHARACTER_HEIGHT = 250 # ALTURA REDUCIDA para asegurar que cabe en pantalla
CHARACTER_CENTER_X = (SCREEN_WIDTH // 2) - 200 
CHARACTER_BOTTOM_Y = SCREEN_HEIGHT * 0.9 
ARROW_SIZE = (40, 40) # Tamaño fijo para las flechas

class CustomizeScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        # Usaremos el font de Pygame por defecto si no tienes uno cargado
        self.font = pygame.font.Font(None, 36) 
        
        # --- Carga y escala de assets ---
        background_img_orig = load_image('ui', 'background customize.png') 
        self.background_img = pygame.transform.scale(background_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Cargar y escalar las flechas
        arrow_left_orig = load_image('ui', 'arrow left.png')
        arrow_right_orig = load_image('ui', 'arrow right.png')
        self.arrow_left_img = pygame.transform.scale(arrow_left_orig, ARROW_SIZE)
        self.arrow_right_img = pygame.transform.scale(arrow_right_orig, ARROW_SIZE)
        
        # Inicialización de las selecciones
        self.choices = {
            'body': 0,
            'head': 0,
            'hat': 0
        }
        
        # Inicialización de la caja de texto para el nombre
        self.textbox = TextBox(
            x=(SCREEN_WIDTH // 2) + 100, 
            y=SCREEN_HEIGHT // 2, 
            w=300, 
            h=50, 
            font=pygame.font.Font(None, 40),
            initial_text='Tu Nombre'
        )

        # Configuración de botones y selectores
        self.confirm_button_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 200, 60)
        
        # --- NUEVA LÓGICA: Cargar y escalar el asset del botón de continuar ---
        confirm_button_orig = load_image('ui', 'button continue.png')
        self.confirm_button_img = pygame.transform.scale(confirm_button_orig, (200, 60))
        
        self.selector_rects = self._setup_selectors()
        
    def _setup_selectors(self):
        """Define la posición de los botones de selección."""
        
        # Usamos el tamaño fijo ARROW_SIZE (40x40) para definir los rects
        w, h = ARROW_SIZE 
        return {
            'hat': { 
                # Las posiciones deben ser consistentes con la sección de dibujo
                'left': pygame.Rect(CHARACTER_CENTER_X - 150, 150, w, h),
                'right': pygame.Rect(CHARACTER_CENTER_X + 150, 150, w, h),
            },
            'head': {
                'left': pygame.Rect(CHARACTER_CENTER_X - 150, 300, w, h),
                'right': pygame.Rect(CHARACTER_CENTER_X + 150, 300, w, h),
            },
            'body': {
                'left': pygame.Rect(CHARACTER_CENTER_X - 150, 450, w, h),
                'right': pygame.Rect(CHARACTER_CENTER_X + 150, 450, w, h),
            },
        }

    def _get_asset_path_key(self, part_type):
        """
        Devuelve la ruta de la subcarpeta del asset.
        """
        if part_type == 'body':
            return 'bodies'
        elif part_type == 'head': 
            return 'heads'
        elif part_type == 'hat':   
            return 'hats' 

    def _cycle_part(self, part_type, direction):
        """Avanza o retrocede el índice de una parte específica."""
        current_index = self.choices[part_type]
        max_index = len(CHARACTER_PARTS[part_type]) - 1
        
        if direction == 'next':
            # Usa el módulo (%) para envolver al inicio de la lista
            new_index = (current_index + 1) % (max_index + 1) 
        elif direction == 'prev':
            # Usa el módulo (%) para envolver al final de la lista
            new_index = (current_index - 1 + max_index + 1) % (max_index + 1) 
        
        self.choices[part_type] = new_index

    def handle_input(self, event):
        self.textbox.handle_event(event) 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            # 1. Botón de Confirmar
            if self.confirm_button_rect.collidepoint(pos):
                if self.textbox.text.strip() and self.textbox.text != 'Tu Nombre':
                    self._save_character_to_state()
                    self.change_scene('ROOM') 
                else:
                    print("¡Por favor, ingresa un nombre!")
                return

            # 2. Selectores de partes del personaje
            for part_type, rects in self.selector_rects.items():
                if rects['right'].collidepoint(pos):
                    self._cycle_part(part_type, 'next')
                elif rects['left'].collidepoint(pos):
                    self._cycle_part(part_type, 'prev')

    def _save_character_to_state(self):
        """Guarda la selección final de partes Y el nombre en el estado global (GameState)."""
        self.game.state.player_name = self.textbox.text
        self.game.state.character_body = CHARACTER_PARTS['body'][self.choices['body']]
        self.game.state.character_head = CHARACTER_PARTS['head'][self.choices['head']]
        
        hat_filename = CHARACTER_PARTS['hat'][self.choices['hat']]
        # Si el usuario seleccionó 'None' (índice 0), guarda None en el estado
        self.game.state.character_hat = hat_filename if hat_filename != 'None' else None 
        
        print(f"Personaje '{self.game.state.player_name}' finalizado y guardado.")

    def update(self, dt):
        pass

    def _draw_composed_character(self, screen):
        """Carga, REDIMENSIONA y dibuja las partes del personaje compuestas."""
        
        x = CHARACTER_CENTER_X
        y = CHARACTER_BOTTOM_Y
        parts_to_draw = []
        
        # --- Redimensionamiento Base (Cuerpo) ---
        body_filename = CHARACTER_PARTS['body'][self.choices['body']]
        # Usamos el path correcto
        body_img_orig = load_image(self._get_asset_path_key('body'), body_filename)
        
        scale_factor = CHARACTER_HEIGHT / body_img_orig.get_height()
        new_width = int(body_img_orig.get_width() * scale_factor)
        
        body_img = pygame.transform.scale(body_img_orig, (new_width, CHARACTER_HEIGHT))
        body_rect = body_img.get_rect(midbottom=(x, y)) 
        parts_to_draw.append((body_img, body_rect))
        
        # Posición base para la cabeza y sombrero
        head_offset_y = body_rect.y 
        head_offset_x = x 

        # 2. Cabeza (Siempre se dibuja)
        head_filename = CHARACTER_PARTS['head'][self.choices['head']]
        head_img_orig = load_image(self._get_asset_path_key('head'), head_filename)
        
        head_img = pygame.transform.scale(head_img_orig, 
                                            (int(head_img_orig.get_width() * scale_factor), 
                                             int(head_img_orig.get_height() * scale_factor)))
                                            
        # AJUSTE: Posiciona la cabeza arriba del cuerpo (overlap +50)
        head_rect = head_img.get_rect(midbottom=(head_offset_x, head_offset_y + 50)) 
        parts_to_draw.append((head_img, head_rect))

        # 3. Sombrero (Condicional)
        hat_filename = CHARACTER_PARTS['hat'][self.choices['hat']]
        if hat_filename != 'None':
            # Usamos el path correcto: 'hats'
            hat_img_orig = load_image(self._get_asset_path_key('hat'), hat_filename)
            
            hat_img = pygame.transform.scale(hat_img_orig, 
                                                (int(hat_img_orig.get_width() * scale_factor), 
                                                 int(hat_img_orig.get_height() * scale_factor)))
            
            # AJUSTE: Posiciona el sombrero ENCIMA de la cabeza (overlap +90)
            hat_offset_y = head_rect.y + 90 
            hat_rect = hat_img.get_rect(midbottom=(head_offset_x, hat_offset_y))
            parts_to_draw.append((hat_img, hat_rect))

        # Dibujar todas las partes en orden (cuerpo -> cabeza -> sombrero)
        for img, rect in parts_to_draw:
            screen.blit(img, rect)

    def draw(self, screen):
        # 1. Dibujar el fondo escalado
        screen.blit(self.background_img, (0, 0))
        
        self._draw_composed_character(screen) 
        
        # --- ELIMINADO: Título "CREA TU PERSONAJE" ---
        # title_text = self.font.render("CREA TU PERSONAJE", True, (255, 255, 255))
        # screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # --- Dibujar Selectores y Opciones ---
        text_labels = {'hat': 'SOMBRERO:', 'head': 'CABEZA:', 'body': 'CUERPO:'}
        
        for part_type, index in self.choices.items():
            rects = self.selector_rects[part_type]
            
            # --- ELIMINADO: Etiquetas de parte (SOMBRERO, CABEZA, CUERPO) ---
            # label_text = self.font.render(text_labels[part_type], True, (255, 255, 255))
            # label_center_x = (rects['left'].centerx + rects['right'].centerx) // 2
            # screen.blit(label_text, label_text.get_rect(center=(CHARACTER_CENTER_X, rects['left'].top - 10))) 
            
            # --- USAR ASSETS DE FLECHA EN LUGAR DE RECTÁNGULOS GRISES ---
            # Dibuja flecha izquierda
            screen.blit(self.arrow_left_img, rects['left'])
            
            # Dibuja flecha derecha
            screen.blit(self.arrow_right_img, rects['right'])
            
        # --- Dibujar Caja de Texto de Nombre ---
        name_prompt = self.font.render("INGRESA TU NOMBRE:", True, (255, 255, 255))
        screen.blit(name_prompt, (self.textbox.rect.x, self.textbox.rect.y - 40))
        self.textbox.draw(screen)
            
        # --- Dibujar Botón de Confirmación con el asset 'button continue.png' ---
        # 1. Dibuja el asset del botón. El rect ya tiene el tamaño y posición correctos (200x60).
        screen.blit(self.confirm_button_img, self.confirm_button_rect) 
        
        # --- ELIMINADO: Texto "CONFIRMAR" sobre el botón ---
        # confirm_text = self.font.render("CONFIRMAR", True, (255, 255, 255))
        # screen.blit(confirm_text, confirm_text.get_rect(center=self.confirm_button_rect.center))