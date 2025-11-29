import pygame
from engine.ui import Button
from game.state import GameState

class EndingScene:
    def __init__(self, manager, state):
        self.manager = manager
        self.screen = manager.screen
        self.state = state

    def start(self):
        self.font = pygame.font.SysFont(None, 24)
        self.title = pygame.font.SysFont(None, 36)
        self.btn_restart = Button((WIDTH//2-120, HEIGHT-120, 240, 60), "Reiniciar juego", self.font, self.restart)

    def restart(self):
        # create fresh state and go to customize
        from scenes.customize import CustomizeScene
        self.manager.replace(CustomizeScene(self.manager))

    def handle_event(self, event):
        self.btn_restart.handle_event(event)

    def update(self, dt):
        pass

    def render(self, surf):
        surf.fill((250,250,250))
        t = self.title.render("Listo para la escuela!", True, (20,20,20))
        surf.blit(t, (40,40))
        sx = 40
        surf.blit(self.font.render(f"Nombre: {self.state.name}", True, (30,30,30)), (sx, 120))
        surf.blit(self.font.render(f"Snack: {self.state.snack}", True, (30,30,30)), (sx, 150))
        surf.blit(self.font.render(f"Bebida: {self.state.drink}", True, (30,30,30)), (sx, 180))
        surf.blit(self.font.render(f"Carta guardada. Stickers: {','.join(self.state.stickers)}", True, (30,30,30)), (sx, 210))
        self.btn_restart.draw(surf)