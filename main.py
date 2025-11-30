import pygame
import importlib
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS
from game.state import GameState

# NOTA: Se ha eliminado 'from scenes.closet import ClosetOutfitScene'
# ya que la función load_scene gestiona la importación dinámica usando las rutas de cadena.

# El diccionario SCENE_MAP debe usar rutas de cadena para que el cargador dinámico funcione correctamente.
SCENE_MAP = {
    'TITLE': 'scenes.title.TitleScene',
    'CUSTOMIZE': 'scenes.customize.CustomizeScene',
    'ROOM': 'scenes.room.RoomScene',
    'CLOSET_OUTFIT': 'scenes.closet.ClosetOutfitScene', # <--- CORREGIDO: Usamos la ruta de cadena.
 
    # Incluye aquí las otras escenas a medida que las crees:
    # 'LIVING_ROOM': 'scenes.living_room.LivingRoomScene',
    # 'KITCHEN': 'scenes.kitchen.KitchenScene',
    # 'WRITE_LETTER': 'scenes.write_letter.WriteLetterScene',
    # 'ENDING': 'scenes.ending.EndingScene',
}

class Game:
    def __init__(self):
        # Inicialización de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado del juego
        self.state = GameState()
        
        # Inicialización de la primera escena
        self.current_scene = self.load_scene('TITLE')
        
        # Diccionario para almacenar instancias de escenas ya cargadas si se desea reutilizarlas
        # Por ahora, las cargamos bajo demanda.

    def load_scene(self, scene_key):
        """
        Importa y retorna una nueva instancia de la clase de escena
        basada en la clave proporcionada (ej: 'TITLE').
        """
        if scene_key not in SCENE_MAP:
            raise ValueError(f"Escena no encontrada: {scene_key}")
        
        module_path_str = SCENE_MAP[scene_key] # Ej: 'scenes.title.TitleScene'
        
        # Dividir la ruta para obtener el nombre del módulo y el nombre de la clase
        try:
            # Añadimos una verificación de tipo para ser más robustos
            if not isinstance(module_path_str, str):
                raise TypeError(f"La ruta de la escena debe ser una cadena: {scene_key}")

            module_name, class_name = module_path_str.rsplit('.', 1)
            
            # 1. Importar dinámicamente el módulo (ej: scenes.title)
            module = importlib.import_module(module_name)
            
            # 2. Obtener la clase del módulo (ej: TitleScene)
            SceneClass = getattr(module, class_name)
            
            # 3. Crear y retornar la instancia de la escena
            new_scene = SceneClass(self)
            return new_scene
            
        except (ValueError, ImportError, AttributeError, TypeError) as e:
            print(f"Error al cargar la escena {scene_key}: {e}")
            # Si hay un error, salir de Pygame de forma segura
            pygame.quit()
            exit()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Tiempo en segundos desde el último frame
            
            # 1. Manejar entradas (eventos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Pasar el evento a la escena actual
                if self.current_scene:
                    self.current_scene.handle_input(event)
            
            # 2. Actualizar self.current_scene
            if self.current_scene:
                self.current_scene.update(dt)
            
            # 3. Comprobar si hay cambio de escena
            if self.current_scene and self.current_scene.next_scene:
                next_scene_key = self.current_scene.next_scene
                self.current_scene.next_scene = None # Resetear la solicitud de cambio
                self.current_scene = self.load_scene(next_scene_key)

            # 4. Dibujar self.current_scene
            self.screen.fill((0, 0, 0)) # Limpiar pantalla (fondo negro)
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()