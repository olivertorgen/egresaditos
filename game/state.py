# game/state.py

import json
import os

class GameState:
    def __init__(self):
        # ==================================
        # 1. ESTADO DEL PERSONAJE Y VESTUARIO
        # ==================================
        # Posición global del jugador (0.0 significa "usar posición por defecto de la escena")
        self.player_x = 0.0
        self.player_y = 0.0  
        self.player_name = "Nacho" # Nombre por defecto

        # Vestuario (Nombres de archivo)
        # Partes elegidas en CUSTOMIZE.PY
        self.outfit_body = 'cat body.png'     # Valor por defecto inicial
        self.outfit_head = 'cat head.png'     # Valor por defecto inicial
        self.outfit_hat = None               # No tiene sombrero por defecto

        # Partes elegidas en CLOSET.PY (Ropa)
        self.outfit_clothes = None           # Ropa inicialmente Nula
        
        # ==================================
        # 2. DECISIONES NARRATIVAS / INVENTARIO
        # ==================================
        
        self.breakfast_choice = None 
        self.has_pan_dulce = False
        self.has_sidra = False
        self.has_backpack = False
        
        # ... (Resto del estado) ...

    def get_outfit_assets(self):
        """Devuelve los assets que el Player debe dibujar."""
        return {
            "body"    : self.outfit_body,
            "head"    : self.outfit_head,
            "clothes" : self.outfit_clothes,
            "hat"     : self.outfit_hat
        }
    
    # --- Funciones de guardado y carga (save/load se mantienen) ---
    def save(self, filename="savegame.json"):
        data = self.__dict__.copy()
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print("✅ Progreso guardado con éxito.")
        except Exception as e:
            print(f"❌ Error al guardar el juego: {e}")

    def load(self, filename="savegame.json"):
        if not os.path.exists(filename):
            return

        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.__dict__.update(data)
            print("✅ Progreso cargado con éxito.")
        except Exception as e:
            print(f"❌ Error al cargar el juego: {e}")
            self.__init__()