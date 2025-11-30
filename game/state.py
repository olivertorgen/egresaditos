# game/state.py

class GameState:
    """Almacena el estado actual del personaje y el progreso."""
    def __init__(self):
        # Personalización
        self.body_asset = 'cat body.png'
        self.head_asset = 'cat head.png'
        self.clothes_asset = None # e.g., 'starry sweater.png'
        
        # Inventario
        self.has_backpack = False
        self.has_pan_dulce = False
        self.has_sidra = False
        
        # Decisiones de rutina
        self.breakfast_choice = None # e.g., 'latte'
        self.letter_written = False
        
        # Posición del personaje (para side scrolling)
        self.player_x = 0
        self.player_y = 0

    def get_character_assets(self):
        """Retorna las rutas completas para dibujar el personaje."""
        base_path = 'assets/'
        return {
            'body': f'{base_path}bodies/{self.body_asset}',
            'head': f'{base_path}heads/{self.head_asset}',
            'clothes': f'{base_path}clothes/{self.clothes_asset}' if self.clothes_asset else None
        }
    # game/state.py (Clase de ejemplo)

class GameState:
    """Contiene todas las variables de estado del juego."""
    def __init__(self):
        # Opciones de Personalización Inicial
        self.character_body = None  # Ejemplo: 'body_base_1'
        self.character_head = None  # Ejemplo: 'head_style_3'
        self.character_hat = None   # Ejemplo: 'hat_cap'
        
        # Ropa seleccionada en el armario (para la escena ROOM)
        self.current_outfit = {} 
        
        # ... (otras variables de juego)