# game/sparks.py
import pygame, random

class Spark:
    def __init__(self, x, y):
        self.x = x + random.randint(-10,10)
        self.y = y + random.randint(-10,10)
        self.size = random.randint(2,4)
        self.speed_y = random.uniform(-30,-60)
        self.lifetime = 0.3
        self.age = 0
        self.alpha = 255
        self.color = (255,255,255)

    def update(self, dt):
        self.age += dt
        self.y += self.speed_y * dt
        self.alpha = max(0, 255 * (1 - self.age/self.lifetime))

    def draw(self, screen):
        if self.alpha>0:
            s = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
            s.fill((*self.color,int(self.alpha)))
            screen.blit(s,(self.x,self.y))

    def dead(self):
        return self.age>=self.lifetime


class SparkBurst:
    def __init__(self):
        self.sparks=[]

    def trigger(self,x,y):
        for _ in range(14):
            self.sparks.append(Spark(x,y))

    def update(self,dt):
        for s in self.sparks: s.update(dt)
        self.sparks=[s for s in self.sparks if not s.dead()]

    def draw(self,screen):
        for s in self.sparks: s.draw(screen)
