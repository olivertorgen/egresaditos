import pygame
import os
from settings import *
from engine.scene_manager import Scene
from engine.ui import Button
from engine.narrator import Narrator


def load_image(filename):
    """Carga una imagen desde /assets usando rutas reales."""
    if not filename:
        return None
    path = os.path.join("assets", filename)
    return pygame.image.load(path).convert_alpha()


class RoomScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Estado global
        self.state = self.game.state

        # Fondo
        self.background = load_image("images/rooms/day room.png")

        #===========================
        # ASSETS DEL PERSONAJE
        #===========================
        outfit = self.state.get_outfit_assets()

        self.body_img = load_image(f"bodies/{outfit['body']}") if outfit["body"] else None
        self.head_img = load_image(f"heads/{outfit['head']}") if outfit["head"] else None
        self.hat_img  = load_image(f"hats/{outfit['hat']}") if outfit["hat"] else None

        #===========================
        # BOTONES
        #===========================
        font = pygame.font.Font(None, 32)

        self.btn_open_closet = Button(
            rect=(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 90, 180, 50),
            text="Abrir armario",
            font=font,
            callback=self.go_closet
        )

        self.btn_go_kitchen = Button(
            rect=(40, SCREEN_HEIGHT - 90, 180, 50),
            text="Ir a cocina",
            font=font,
            callback=self.go_kitchen
        )

        #===========================
        # NARRADOR
        #===========================
        self.narrator = Narrator("narrative/script.json")
        # Si tu Narrator usa nodos:
        # self.narrator.start("room_intro")


    #===========================
    # CAMBIO DE ESCENAS
    #===========================
    def go_closet(self):
        self.next_scene = "CLOSET_OUTFIT"

    def go_kitchen(self):
        self.next_scene = "KITCHEN"

    #===========================
    # UPDATE
    #===========================
    def update(self, dt):
        self.btn_open_closet.update(None)
        self.btn_go_kitchen.update(None)
        self.narrator.update(dt)

    #===========================
    # DIBUJAR PERSONAJE
    #===========================
    def draw_player(self, screen):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + 40

        if self.body_img:
            body_rect = self.body_img.get_rect(midbottom=(x, y))
            screen.blit(self.body_img, body_rect)

        if self.head_img:
            head_rect = self.head_img.get_rect(midbottom=(x, y - 95))
            screen.blit(self.head_img, head_rect)

        if self.hat_img:
            hat_rect = self.hat_img.get_rect(midbottom=(x, y - 130))
            screen.blit(self.hat_img, hat_rect)

    #===========================
    # DRAW
    #===========================
    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        self.draw_player(screen)

        self.btn_open_closet.draw(screen)
        self.btn_go_kitchen.draw(screen)

        # --- FIX: ahora sí enviamos pos ---
        narrator_pos = (40, SCREEN_HEIGHT - 140)
        self.narrator.draw(screen, narrator_pos)
