import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image
from engine.scene_manager import Scene
from engine.ui import Button
from game.player import Player, CHARACTER_HEIGHT

GROUND_Y = SCREEN_HEIGHT * 0.9

class DraggableItem:
    """Clase simple para manejar un item de vestuario arrastrable."""
    def __init__(self, asset_name, asset_type, image, center_pos):
        self.asset_name = asset_name
        self.asset_type = asset_type  # Ejemplo: 'hat', 'body', 'head'
        self.original_center = center_pos
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.is_dragging = False

    def handle_event(self, event):
        """Maneja los eventos de drag."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.mouse_offset_x = self.rect.x - event.pos[0]
                self.mouse_offset_y = self.rect.y - event.pos[1]
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.rect.x = event.pos[0] + self.mouse_offset_x
                self.rect.y = event.pos[1] + self.mouse_offset_y
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        return False

    def reset_position(self):
        """Devuelve el item a su posición original."""
        self.rect.center = self.original_center

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ClosetScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.state = self.game.state
        self.closet_open = False

        # Fondos
        try:
            self.background_closed_img = load_image("images/rooms", "closet.png")
            self.background_open_img = load_image("images/rooms", "open closet.png")
        except Exception as e:
            print(f"Error al cargar fondos: {e}")
            self.background_closed_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_closed_img.fill((50, 50, 50))
            self.background_open_img = self.background_closed_img

        self.background_closed = self._scale_background(self.background_closed_img)
        self.background_open = self._scale_background(self.background_open_img)
        self.bg_x = (SCREEN_WIDTH - self.background_closed.get_width()) // 2

        # Player
        outfit = self.state.get_outfit_assets()
        default_body = 'cat body.png'
        default_head = 'cat head.png'
        self.player = Player(
            body=outfit.get('body', default_body),
            head=outfit.get('head', default_head),
            hat=outfit.get('hat')
        )
        self.player.x = SCREEN_WIDTH // 4
        self.player.y = GROUND_Y

        # Botones
        font = pygame.font.Font(None, 32)
        self.btn_toggle_closet = Button(
            rect=(SCREEN_WIDTH - 220, SCREEN_HEIGHT // 2 - 50, 180, 50),
            text="Abrir armario",
            font=font,
            callback=self.toggle_closet
        )
        self.btn_go_room = Button(
            rect=(40, SCREEN_HEIGHT - 70, 150, 50),
            text="Volver al cuarto",
            font=font,
            callback=self.go_room
        )
        self.buttons = [self.btn_toggle_closet, self.btn_go_room]

        # Items arrastrables
        self.draggable_items = self._setup_draggable_items()
        self.dragging_item = None

    def _scale_background(self, img):
        original_width = img.get_width()
        original_height = img.get_height()
        scale_ratio = SCREEN_HEIGHT / original_height
        if original_width * scale_ratio < SCREEN_WIDTH:
            scale_ratio = SCREEN_WIDTH / original_width
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        return pygame.transform.scale(img, (new_width, new_height))

    def _setup_draggable_items(self):
        items = []
        clothes_assets = [
            "black and white sweater.png",
            "shirt charly garcia.png",
            "shirt soda estereo.png",
            "shirt spider punk.png",
            "starry sweater.png",
            "stripped sweater.png"
        ]
        center_x = SCREEN_WIDTH * 0.75
        center_y = SCREEN_HEIGHT * 0.55
        stack_offset = 20
        item_scale = 0.35

        for i, asset_name in enumerate(clothes_assets):
            body_img = load_image('clothes', asset_name)
            scaled_img = pygame.transform.scale(
                body_img,
                (int(body_img.get_width() * item_scale), int(body_img.get_height() * item_scale))
            )
            pos_x = center_x + (i % 3) * stack_offset - stack_offset
            pos_y = center_y + (i // 3) * stack_offset
            item = DraggableItem(asset_name, 'body', scaled_img, (pos_x, pos_y))
            items.append(item)
        return items

    def toggle_closet(self):
        self.closet_open = not self.closet_open
        new_text = "Cerrar armario" if self.closet_open else "Abrir armario"
        self.btn_toggle_closet.text = new_text
        self.btn_toggle_closet.text_surface = self.btn_toggle_closet.font.render(new_text, True, (20, 20, 20))

    def go_room(self):
        self.change_scene("ROOM")

    def handle_input(self, event):
        if not self.dragging_item:
            for btn in self.buttons:
                if btn.handle_event(event) and event.type == pygame.MOUSEBUTTONDOWN and self.game.can_click:
                    btn.callback()
                    self.game.can_click = False
                    return

        if self.closet_open:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item in reversed(self.draggable_items):
                    if item.handle_event(event):
                        self.dragging_item = item
                        self.draggable_items.remove(item)
                        self.draggable_items.append(item)
                        break
            elif event.type == pygame.MOUSEMOTION and self.dragging_item:
                self.dragging_item.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONUP and self.dragging_item:
                self.dragging_item.handle_event(event)
                self._check_drop()
                self.dragging_item = None

    def _check_drop(self):
        item = self.dragging_item
        if not item:
            return
        player_body_rect = pygame.Rect(0, 0, 100, 150)
        player_body_rect.center = (int(self.player.x), int(self.player.y - CHARACTER_HEIGHT * 0.4))

        if item.asset_type == 'body' and item.rect.colliderect(player_body_rect):
            self.state.set_outfit_part('body', item.asset_name)
            self.player.body_asset = item.asset_name
            self.player._load_parts()
            self.player.image = self.player._create_composite_image()
            self.player.rect = self.player.image.get_rect(midbottom=(self.player.x, self.player.y))

        item.reset_position()

    def update(self, dt):
        self.player.update(dt)

    def draw(self, screen):
        background = self.background_open if self.closet_open else self.background_closed
        screen.blit(background, (self.bg_x, 0))
        self.player.draw(screen)

        if self.closet_open:
            player_body_x = int(self.player.x)
            player_body_y = int(self.player.y - CHARACTER_HEIGHT * 0.4)
            target_surface = pygame.Surface((120, 180), pygame.SRCALPHA)
            target_surface.fill((255, 100, 100, 100))
            screen.blit(target_surface, (player_body_x - 60, player_body_y - 90))
            for item in self.draggable_items:
                item.draw(screen)

        for btn in self.buttons:
            btn.draw(screen)
