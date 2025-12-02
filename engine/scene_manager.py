import pygame
import importlib

from settings import SCREEN_SIZE, CAPTION 
from game.state import GameState 

# ======================================================
# DEFINICIÓN DE CLASES Y MAPA 
# ======================================================

class Scene:
    """Clase base para todas las escenas del juego."""
    def __init__(self, game):
        self.game = game
        self.next_scene = None # Usado para solicitar un cambio de escena

    def handle_input(self, event): 
        """Maneja los eventos (mouse, teclado)."""
        pass
        
    def update(self, dt): 
        """Actualiza la lógica del juego (movimiento, colisiones)."""
        pass
        
    def draw(self, screen): 
        """Dibuja todos los elementos en la pantalla."""
        pass
    
    def change_scene(self, next_scene_key):
        """Método llamado por las escenas para iniciar una transición."""
        self.next_scene = next_scene_key

# Mapeo de CLAVES (UPPERCASE) a MÓDULOS (lowercase con puntos)
SCENE_MAP = {
    'TITLE': 'scenes.title',
    'CUSTOMIZE': 'scenes.customize',
    'ROOM': 'scenes.room',
    'CLOSET_OUTFIT': 'scenes.closet_outfit', # ¡ASEGÚRATE DE QUE ESTA RUTA ES CORRECTA EN TU AMBIENTE!
    'KITCHEN': 'scenes.kitchen',
    'WRITE_LETTER': 'scenes.write_letter',
    # Agrega más escenas aquí
}

# ======================================================
# CLASE PRINCIPAL DEL JUEGO
# ======================================================

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = GameState()
        
        # --- Variables de Transición ---
        self.transition_alpha = 0 
        self.transition_speed = 350
        self.is_transitioning = False
        self.transition_target_scene = None
        
        # Carga la primera escena (Requiere SCENE_MAP y Scene definidos)
        self.current_scene = self.load_scene('TITLE')

    def load_scene(self, scene_key):
        """
        Carga dinámicamente el módulo y la clase de una escena.
        Asegura que las claves con guiones bajos (e.g., CLOSET_OUTFIT) se 
        conviertan a CamelCase (e.g., ClosetOutfitScene) correctamente.
        """
        module_path = SCENE_MAP.get(scene_key) 
        if not module_path:
            raise ValueError(f"Escena desconocida: {scene_key}")
        
        # DEBUGGING ADICIONAL: Imprime la ruta del módulo que intentará importar
        print(f"DEBUG: Intentando importar módulo: {module_path}")
            
        module = importlib.import_module(module_path)
        
        # Generación de nombre de clase en CamelCase (e.g., CLOSET_OUTFIT -> ClosetOutfitScene)
        # 1. Convertir a minúsculas y dividir por guiones bajos.
        # 2. Capitalizar cada parte y unirlas.
        parts = scene_key.lower().split('_')
        class_name = "".join(p.capitalize() for p in parts) + 'Scene'
        
        # Intenta obtener la clase del módulo
        SceneClass = getattr(module, class_name)
        
        print(f"Cargando escena: {class_name} desde {module_path}")
        return SceneClass(self)

    def _handle_transition(self, dt):
        """Maneja el efecto de transición (Fade-to-Black/Fade-In)."""
        if self.is_transitioning:
            
            # Fase de FADE-OUT (Fundido a negro)
            if self.transition_target_scene:
                self.transition_alpha += self.transition_speed * dt
                if self.transition_alpha >= 255:
                    self.transition_alpha = 255
                    # Carga la nueva escena A MITAD de la transición
                    self.current_scene = self.load_scene(self.transition_target_scene)
                    self.transition_target_scene = None # Prepara para Fade-In
            
            # Fase de FADE-IN (Desvanecer el negro)
            else:
                self.transition_alpha -= self.transition_speed * dt
                if self.transition_alpha <= 0:
                    self.transition_alpha = 0
                    self.is_transitioning = False # Transición terminada

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Solo procesar input si no hay transición activa
                if not self.is_transitioning:
                    self.current_scene.handle_input(event)
            
            # 1. Actualización (Solo si NO estamos en la fase de Fade-Out)
            if not (self.is_transitioning and self.transition_target_scene):
                    self.current_scene.update(dt)

            # 2. Comprobar y ejecutar cambio de escena (INICIA la transición)
            if self.current_scene.next_scene and not self.is_transitioning:
                self.is_transitioning = True
                self.transition_target_scene = self.current_scene.next_scene
                self.current_scene.next_scene = None
            
            # 3. Dibujado de la escena
            self.current_scene.draw(self.screen)
            
            # 4. Manejo de Transición
            self._handle_transition(dt)
            
            # 5. Dibujar Overlay de Transición
            if self.transition_alpha > 0:
                overlay = pygame.Surface(SCREEN_SIZE)
                overlay.fill((0, 0, 0))
                overlay.set_alpha(int(self.transition_alpha))
                self.screen.blit(overlay, (0, 0))

            pygame.display.flip()
            
        pygame.quit()