import pygame
import importlib
# Importaciones necesarias
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS
from game.state import GameState

# ======================================================
# CLASE BASE DE ESCENA (Fundamental para el Game Manager)
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

# Mapeo de CLAVES (UPPERCASE) a la RUTA DEL MÓDULO (para importlib)
# Se asume que la función load_scene construirá el nombre de la clase (ej: TitleScene)
SCENE_MAP = {
    'TITLE': 'scenes.title',
    'CUSTOMIZE': 'scenes.customize',
    'ROOM': 'scenes.room',
    'CLOSET_OUTFIT': 'scenes.closet', 
    'KITCHEN': 'scenes.kitchen',
    'WRITE_LETTER': 'scenes.write_letter',
    # Agrega más escenas aquí
}

# ======================================================
# CLASE PRINCIPAL DEL JUEGO (Con Transición Restaurada)
# ======================================================

class Game:
    def __init__(self):
        # Inicialización de Pygame
        pygame.init()
        # Usamos SCREEN_WIDTH/HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = GameState()
        
        # --- PROPIEDADES DE TRANSICIÓN Y CLICK RESTAURADAS ---
        self.can_click = True           # Evita interacciones mientras la transición está activa
        self.transition_alpha = 0       # Opacidad del fundido (0=transparente, 255=negro total)
        self.transition_speed = 350     # Velocidad de la transición (píxeles de alpha / segundo)
        self.is_transitioning = False   
        self.transition_target_scene = None 
        
        # Inicialización de la primera escena
        self.current_scene = self.load_scene('TITLE')


    def load_scene(self, scene_key):
        """
        Carga dinámicamente el módulo y la clase de una escena.
        """
        module_path = SCENE_MAP.get(scene_key) 
        if not module_path:
            raise ValueError(f"Escena desconocida: {scene_key}")
        
        # 1. Importar módulo
        module = importlib.import_module(module_path)
        
        # 2. Determinar el nombre de la clase esperado (CamelCase + 'Scene')
        parts = scene_key.lower().split('_')
        class_name = "".join(p.capitalize() for p in parts) + 'Scene'
        
        # 3. AJUSTE CRÍTICO: Sobrescribir si el nombre de la clase es 'ClosetScene'
        if scene_key == 'CLOSET_OUTFIT':
            class_name = 'ClosetScene'
        
        # 4. Intentar obtener la clase del módulo
        try:
            SceneClass = getattr(module, class_name)
        except AttributeError as e:
            print(f"ERROR: No se encontró la clase '{class_name}' en el módulo '{module_path}'.")
            raise e
            
        print(f"Cargando escena: {class_name} desde {module_path}")
        return SceneClass(self)

    def _handle_transition(self, dt):
        """Maneja el efecto de transición (Fade-to-Black/Fade-In)."""
        if self.is_transitioning:
            
            # Fase 1: FADE-OUT (Oscureciendo la pantalla)
            if self.transition_target_scene:
                self.transition_alpha += self.transition_speed * dt
                if self.transition_alpha >= 255:
                    self.transition_alpha = 255
                    
                    # Carga la nueva escena A MITAD de la transición (pantalla negra total)
                    try:
                        self.current_scene = self.load_scene(self.transition_target_scene)
                    except Exception as e:
                        print(f"Error CRÍTICO al cargar la escena {self.transition_target_scene}: {e}. Volviendo a TITLE.")
                        self.current_scene = self.load_scene('TITLE') 
                        
                    self.transition_target_scene = None # Prepara para Fade-In
            
            # Fase 2: FADE-IN (Aclarando la pantalla)
            else:
                self.transition_alpha -= self.transition_speed * dt
                if self.transition_alpha <= 0:
                    self.transition_alpha = 0
                    self.is_transitioning = False
                    # Re-habilitamos el click una vez finalizada la transición
                    self.can_click = True


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Tiempo en segundos
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Solo procesar input si NO hay transición activa y se permite el click
                if not self.is_transitioning and self.can_click:
                    if self.current_scene:
                        self.current_scene.handle_input(event)
            
            # 1. Actualizar (Solo si NO estamos en la fase de Fade-Out)
            if not (self.is_transitioning and self.transition_target_scene):
                if self.current_scene:
                    self.current_scene.update(dt)

            # 2. Comprobar si hay cambio de escena (INICIA la transición)
            if self.current_scene and self.current_scene.next_scene and not self.is_transitioning:
                self.is_transitioning = True
                self.transition_target_scene = self.current_scene.next_scene
                self.current_scene.next_scene = None
                self.can_click = False # Desactiva el click inmediatamente al inicio

            # 3. Dibujar self.current_scene
            self.screen.fill((0, 0, 0)) # Limpiar pantalla
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            # 4. Manejo de Transición
            self._handle_transition(dt)
            
            # 5. Dibujar Overlay de Transición (el fundido a negro)
            if self.transition_alpha > 0:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(int(self.transition_alpha))
                self.screen.blit(overlay, (0, 0))

            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()