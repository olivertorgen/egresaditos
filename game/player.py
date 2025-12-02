import pygame
from settings import load_image, SCREEN_HEIGHT

# Altura estándar del personaje para escala
CHARACTER_HEIGHT = 200
# La posición Y en el suelo
GROUND_Y = SCREEN_HEIGHT * 0.9

# =================================================================
# 🏃‍♂️ PLAYER CLASS
# =================================================================
class Player:
    def __init__(self, body, head, hat=None):
        self.body_asset = body
        self.head_asset = head
        self.hat_asset = hat
        
        # Posición inicial del jugador (actualizada por RoomScene)
        self.x = 0
        self.y = GROUND_Y
        
        # Velocidad de movimiento (píxeles por segundo)
        # Nota: La velocidad se ajusta a 400 en RoomScene para un movimiento más rápido.
        self.speed = 150 
        
        # Estado de salto
        self.is_jumping = False
        self.jump_velocity = 0
        # CORRECCIÓN DE FLUIDEZ: AUMENTAMOS drásticamente la gravedad para un salto instantáneo y reactivo
        self.gravity = 2500 # Aceleración de la gravedad, valor muy alto para un efecto arcade/plataforma ultrarrápido
        

    def start_jump(self):
        """Inicia el salto si el personaje está en el suelo."""
        if not self.is_jumping:
            self.is_jumping = True
            # CORRECCIÓN DE FLUIDEZ: Mayor impulso inicial para un salto más enérgico
            self.jump_velocity = -1000 

    def update(self, dt=1/60.0):
        """
        Aplica gravedad y actualiza la posición vertical (salto).
        Usa dt para garantizar que el salto es fluido y consistente.
        """
        if self.is_jumping:
            # Aplicar la velocidad vertical
            self.y += self.jump_velocity * dt
            # Aplicar la gravedad para reducir la velocidad
            self.jump_velocity += self.gravity * dt
            
            # Comprobar si aterriza
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
                self.jump_velocity = 0
                
    # =================================================================
    # DRAWING LOGIC (Lógica de Dibujado)
    # =================================================================
    def draw(self, screen):
        parts = []
        
        # 1. Cuerpo
        body_img = load_image('bodies', self.body_asset)
        # Factor de escala
        scale_ratio = CHARACTER_HEIGHT / body_img.get_height()
        
        body_img = pygame.transform.scale(
            body_img,
            (int(body_img.get_width() * scale_ratio), CHARACTER_HEIGHT)
        )
        
        # Usamos self.x y self.y (que incluye el ajuste de salto)
        body_rect = body_img.get_rect(midbottom=(self.x, self.y))
        parts.append((body_img, body_rect))
        
        # 2. Cabeza
        head_img = load_image('heads', self.head_asset)
        head_img = pygame.transform.scale(
            head_img,
            (int(head_img.get_width() * scale_ratio), int(head_img.get_height() * scale_ratio))
        )
        
        # 50 es la compensación de la cabeza respecto al cuello (body_rect.top)
        head_rect = head_img.get_rect(midbottom=(self.x, body_rect.top + 50))
        parts.append((head_img, head_rect))
        
        # 3. Sombrero (¡Corrección de offsets!)
        if self.hat_asset:
            hat_img = load_image('hats', self.hat_asset)
            hat_img = pygame.transform.scale(
                hat_img,
                (int(hat_img.get_width() * scale_ratio), int(hat_img.get_height() * scale_ratio))
            )

            # OFFSETS AJUSTADOS para que el sombrero se siente correctamente
            HAT_OFFSETS = {
                "hat graduation.png": 60, # Offset pequeño para la parte superior de la cabeza
                "hat santa claus.png": 40,  # Offset más pequeño
                "hat wizard.png": 80, # Offset medio
            }

            offset = HAT_OFFSETS.get(self.hat_asset, 60) 

            # Posicionar el sombrero usando el top de la cabeza (head_rect.top) más el offset
            # Este offset empuja el sombrero hacia abajo, sobre la cabeza.
            hat_rect = hat_img.get_rect(
                midbottom=(self.x, head_rect.top + offset) 
            )

            parts.append((hat_img, hat_rect))
            
        # Dibujar todas las partes
        for img, rect in parts:
            screen.blit(img, rect)