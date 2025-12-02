import pygame
from settings import load_image

class Player:
    """
    Player: dibuja al alumno con cuerpo, cabeza y sombrero.
    Este sistema queda como base y RoomScene ahora lo replica.
    """

    def __init__(self, body, head, hat):
        self.body_img = load_image(body)
        self.head_img = load_image(head)
        self.hat_img = load_image(hat)

        # Offsets consistentes en ambos archivos
        self.head_offset_from_body = -120
        self.hat_offset_from_head = -70

        # Posición inicial del jugador
        self.x = 300
        self.y = 500

    def draw(self, screen):
        # ---- CUERPO ----
        body_rect = self.body_img.get_rect(midbottom=(self.x, self.y))
        screen.blit(self.body_img, body_rect)

        # ---- CABEZA ----
        head_x = body_rect.midtop[0]
        head_y = body_rect.midtop[1] + self.head_offset_from_body
        head_rect = self.head_img.get_rect(midbottom=(head_x, head_y))
        screen.blit(self.head_img, head_rect)

        # ---- SOMBRERO ----
        hat_x = head_rect.midtop[0]
        hat_y = head_rect.midtop[1] + self.hat_offset_from_head
        hat_rect = self.hat_img.get_rect(midbottom=(hat_x, hat_y))
        screen.blit(self.hat_img, hat_rect)
