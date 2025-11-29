import pygame

class Button:
    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surf):
        pygame.draw.rect(surf, (240,240,240) if self.hover else (220,220,220), self.rect, border_radius=8)
        txt = self.font.render(self.text, True, (20,20,20))
        txt_r = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_r)