import pygame

class Button:
    def __init__(self, image=None, pos=None, callback=None,
                 rect=None, text=None, font=None):
        """
        Soporta DOS modos:
        ------------------------------------
        1) Botón con imagen:
           Button(image=img, pos=(x,y), callback=fn)

        2) Botón rectangular con texto:
           Button(rect=(x,y,w,h), text="Play", font=font, callback=fn)
        """

        self.callback = callback
        self.hover = False

        # ===== MODO 1: BOTÓN CON IMAGEN =====
        if image is not None and pos is not None:
            self.mode = "image"
            self.image = image
            self.rect = self.image.get_rect(center=pos)

        # ===== MODO 2: BOTÓN DE TEXTO (UI clásico) =====
        elif rect is not None and text is not None and font is not None:
            self.mode = "text"
            self.rect = pygame.Rect(rect)
            self.text = text
            self.font = font
            self.text_surface = self.font.render(self.text, True, (20, 20, 20))

        else:
            raise ValueError("Button mal creado. Faltan argumentos.")

    # -------------------------
    # UPDATE (vacío por seguridad)
    # -------------------------
    def update(self, dt=None):
        pass

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, surf):
        if self.mode == "image":
            surf.blit(self.image, self.rect)

        elif self.mode == "text":
            # color al pasar mouse
            color = (240, 240, 240) if self.hover else (220, 220, 220)
            pygame.draw.rect(surf, color, self.rect, border_radius=8)

            txt_rect = self.text_surface.get_rect(center=self.rect.center)
            surf.blit(self.text_surface, txt_rect)

    # -------------------------
    # EVENTOS
    # -------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
