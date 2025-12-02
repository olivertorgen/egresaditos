import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, WHITE

class EndingScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Usaremos la misma fuente que TitleScene
        self.font = pygame.font.Font(None, 48)
        self.footer_text = "¡Gracias por jugar!"
        self.footer_surface = self.font.render(self.footer_text, True, WHITE)
        self.footer_rect = self.footer_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.95))

        # Cargar fondo: Se usa el mismo que en TitleScene
        self.bg = load_image("", "Egresaditos portada.gif")
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Botón Rewind (Reinicio)
        self.btn_rewind_original = load_image("ui","button rewind.png")
        
        # Tamaño del botón de reinicio (un poco más pequeño que el de Play)
        BUTTON_WIDTH = 280
        BUTTON_HEIGHT = 100
        
        self.btn_rewind = pygame.transform.scale(self.btn_rewind_original, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.btn_rewind_hover = pygame.transform.scale(self.btn_rewind_original, (BUTTON_WIDTH + 20, BUTTON_HEIGHT + 10)) # Ligeramente más grande para hover
        self.btn_rewind_rect = self.btn_rewind.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.78))
        self.is_hovering = False
        
        # NOTA DE MÚSICA: El Game Manager (main.py) ya intenta reproducir 
        # 'music/ending.ogg' (o .wav) automáticamente al cargar esta escena.

    def handle_input(self, event):
        # 1. Manejo de Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.btn_rewind_rect.collidepoint(event.pos):
                # Reiniciar el juego volviendo a la escena de título
                self.change_scene("TITLE")
        
        # 2. Manejo de Hover (para detectar si el mouse está sobre el botón)
        if event.type == pygame.MOUSEMOTION:
            self.is_hovering = self.btn_rewind_rect.collidepoint(event.pos)

    def update(self, dt):
        # No se necesita actualización compleja en la escena de final (por ahora)
        pass

    def draw(self, screen):
        # Dibujar fondo
        screen.blit(self.bg, (0, 0))
        
        # Dibujar el mensaje de agradecimiento
        screen.blit(self.footer_surface, self.footer_rect)

        # Dibujar botón de Rewind (con efecto hover)
        if self.is_hovering:
            # Dibujar la versión más grande (hover) centrada
            hover_rect = self.btn_rewind_hover.get_rect(center=self.btn_rewind_rect.center)
            screen.blit(self.btn_rewind_hover, hover_rect)
        else:
            # Dibujar la versión normal
            screen.blit(self.btn_rewind, self.btn_rewind_rect)