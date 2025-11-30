import pygame
from engine.ui import Button

class WriteLetterScene:
    def __init__(self, manager, state):
        self.manager = manager
        self.screen = manager.screen
        self.state = state

    def start(self):
        self.font = pygame.font.SysFont(None, 24)
        self.title = pygame.font.SysFont(None, 36)
        self.input_text = self.state.letter or "Querido profesor..."
        self.cursor = 0
        self.btn_save = Button((WIDTH-220, HEIGHT-80, 200, 50), "Guardar sobre", self.font, self.save_letter)
        # sticker options (just names, el usuario puede poner imágenes en assets)
        self.stickers = ['estrella','corazon','nota']
        self.chosen_stickers = []

    def save_letter(self):
        self.state.letter = self.input_text
        self.state.stickers = self.chosen_stickers
        self.state.save()
        from scenes.ending import EndingScene
        self.manager.push(EndingScene(self.manager, self.state))

    def handle_event(self, event):
        self.btn_save.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.input_text += "\n"
            else:
                self.input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = event.pos
            # sticker pick areas
            if 60 < mx < 260 and 420 < my < 460:
                idx = (mx-60)//60
                if 0 <= idx < len(self.stickers):
                    self.chosen_stickers.append(self.stickers[idx])

    def update(self, dt):
        pass

    def render(self, surf):
        surf.fill((255,250,245))
        t = self.title.render("Escribí tu carta", True, (20,20,20))
        surf.blit(t, (40,40))
        # input box
        box = pygame.Rect(40, 100, WIDTH-120, 260)
        pygame.draw.rect(surf, (245,245,245), box)
        lines = self.input_text.split('\n')
        y = 110
        for l in lines:
            surf.blit(self.font.render(l, True, (20,20,20)), (50, y))
            y += 24
        # sticker palette
        x = 60
        for s in self.stickers:
            pygame.draw.rect(surf, (220,220,220), (x, 420, 48, 32))
            surf.blit(self.font.render(s[0].upper(), True, (30,30,30)), (x+14, 426))
            x += 60
        # chosen stickers preview
        surf.blit(self.font.render("Stickers: " + ",".join(self.chosen_stickers), True, (30,30,30)), (40, 360))
        self.btn_save.draw(surf)