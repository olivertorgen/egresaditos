import pygame

class Narrator:
    def __init__(self, font):
        self.font = font
        self.queue = []
        self.timer = 0
        self.current = None

    def say(self, text, secs=3.0):
        self.queue.append((text, secs))
        if not self.current:
            self._next()

    def _next(self):
        if self.queue:
            self.current = self.queue.pop(0)
            self.timer = self.current[1]
        else:
            self.current = None

    def update(self, dt):
        if self.current:
            self.timer -= dt
            if self.timer <= 0:
                self._next()

    def draw(self, surf, pos):
        if self.current:
            text = self.current[0]
            lines = text.split("\n")
            y = pos[1]
            for l in lines:
                s = self.font.render(l, True, (30,30,30))
                surf.blit(s, (pos[0], y))
                y += s.get_height() + 2