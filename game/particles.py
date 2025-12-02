# game/particles.py
import pygame, random

class StarParticle:
    def __init__(self, frames, x, y, speed, scale=1):
        self.frames = frames         # lista de imágenes del GIF procesado
        self.index = 0
        self.x = x
        self.y = y
        self.speed = speed
        self.time = 0
        self.scale = scale

    def update(self, dt):
        self.time += dt * 12                 # velocidad de animación
        self.index = int(self.time) % len(self.frames)
        self.y += self.speed * dt            # movimiento vertical suave

        # si sale de pantalla, reaparece arriba
        if self.y > pygame.display.get_surface().get_height():
            self.y = -30
            self.x = random.randint(0, pygame.display.get_surface().get_width())

    def draw(self, screen):
        frame = self.frames[self.index]
        rect = frame.get_rect(center=(self.x, self.y))
        screen.blit(frame, rect)


class StarField:
    """Genera un cielo con estrellas/GIF animado."""
    def __init__(self, image_path, count=20, scale=1):
        # cargar GIF animado con pygame.image.load_extended
        frames = []
        try:
            gif = pygame.image.load(image_path)
            gif.convert_alpha()
            frames.append(gif)
        except:
            print("⚠ No se pudo cargar GIF. Usando círculo blanco.")
            frames = [pygame.Surface((6,6),pygame.SRCALPHA)]
            pygame.draw.circle(frames[0], (255,255,255), (3,3), 3)

        # generar partículas
        self.particles = []
        for _ in range(count):
            x = random.randint(0, pygame.display.get_surface().get_width())
            y = random.randint(-200, pygame.display.get_surface().get_height())
            speed = random.uniform(20,70)
            self.particles.append(StarParticle(frames,x,y,speed,scale))


    def update(self, dt):
        for s in self.particles: s.update(dt)

    def draw(self, screen):
        for s in self.particles: s.draw(screen)
