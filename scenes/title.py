import pygame
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, WHITE

class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Cargar fondo
        # Asumo que 'Egresaditos portada.gif' es un frame estático si no usamos librerías de GIF/Video.
        # Si prefieres usar la imagen estática 'Egresaditos portada.gif', asegúrate de que solo se cargue el primer frame.
        # Si no, podrías usar otra imagen si la portada.gif trae problemas.
        self.bg = load_image("", "Egresaditos portada.gif")
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Botón Play
        self.btn_play_original = load_image("ui","button play.png")
        self.btn_play = pygame.transform.scale(self.btn_play_original, (330, 120))
        self.btn_play_hover = pygame.transform.scale(self.btn_play_original, (350, 130)) # Ligeramente más grande para hover
        self.btn_play_rect = self.btn_play.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.78))
        self.is_hovering = False
        
        # Opcional: Iniciar la música del menú si tuvieras el motor de audio listo
        # if hasattr(self.game, 'audio') and self.game.audio:
        #     self.game.audio.play_music('Egresaditos portada.mp4') # O cualquier música de menú
        
    def handle_input(self, event):
        # 1. Manejo de Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_play_rect.collidepoint(event.pos):
                # Cambiar a la escena de personalización
                self.change_scene("CUSTOMIZE")
        
        # 2. Manejo de Hover (para detectar si el mouse está sobre el botón)
        if event.type == pygame.MOUSEMOTION:
            self.is_hovering = self.btn_play_rect.collidepoint(event.pos)

    def update(self, dt):
        # No se necesita actualización compleja en la escena de título (por ahora)
        pass

    def draw(self, screen):
        # Dibujar fondo
        screen.blit(self.bg, (0, 0))
        
        # Dibujar botón de Play (con efecto hover)
        if self.is_hovering:
            # Dibujar la versión más grande (hover) centrada
            hover_rect = self.btn_play_hover.get_rect(center=self.btn_play_rect.center)
            screen.blit(self.btn_play_hover, hover_rect)
        else:
            # Dibujar la versión normal
            screen.blit(self.btn_play, self.btn_play_rect)