# scenes/customize.py

import pygame
import random
from engine.scene_manager import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, load_image
from game.particles import StarField
from game.sparks import SparkBurst 


# =====================================================================
# ✨ SparkleEmitter: Mantenido, pero su lógica de update/draw debe estar en la clase Scene.
# =====================================================================
class SparkleEmitter:
    def __init__(self, area_rect, count=10, color=(255,255,255)):
        self.particles = []
        self.area = area_rect
        self.base_count = count
        self.color = color

    def update(self, dt):
        # Reponer partículas si faltan
        while len(self.particles) < self.base_count:
            x = random.randint(self.area.left, self.area.right)
            y = random.randint(self.area.top, self.area.bottom)
            size = random.randint(3,6)
            speed = random.uniform(-10,-30)
            life = random.uniform(1.4,2.3)

            self.particles.append({
                "x":x,"y":y,"size":size,
                "alpha":255,"speed":speed,
                "time":0,"life":life
            })

        # Actualizar
        for p in self.particles:
            p["time"] += dt
            p["y"] += p["speed"]*dt
            p["alpha"] = max(0, 255*(1-(p["time"]/p["life"])))

        # Eliminar apagadas
        self.particles = [p for p in self.particles if p["alpha"]>0]

    def draw(self, screen):
        for p in self.particles:
            surf = pygame.Surface((p["size"],p["size"]),pygame.SRCALPHA)
            surf.fill((*self.color,int(p["alpha"])))
            screen.blit(surf,(p["x"],p["y"]))


# =====================================================================
# 📦 TEXTBOX — Se mantiene intacto
# =====================================================================
class TextBox:
    def __init__(self, x, y, w, h, font, initial_text=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = initial_text
        self.font = font
        self.active = False
        self.txt_surface = self.font.render(self.text,True,pygame.Color('white'))

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        if event.type==pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                self.active=False; self.color=self.color_inactive
            elif event.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
            else:
                if len(self.text)<15: self.text+=event.unicode
            self.txt_surface=self.font.render(self.text,True,pygame.Color('white'))

    def draw(self,screen):
        screen.blit(self.txt_surface,(self.rect.x+5,self.rect.y+5))
        pygame.draw.rect(screen,self.color,self.rect,2)


# =====================================================================
# OPCIONES DEL PERSONAJE (Se mantienen intactas)
# =====================================================================
CHARACTER_PARTS = {
    "body": ['bow cat body.png','cat body.png','dragon body.png','oshawott body.png','raichu body.png'],
    "head": ['cat head.png','cloud head.png','pingu head.png','pitaya head.png','raichu head.png','shark cat head.png'],
    "hat": 	['None','hat graduation.png','hat santa claus.png','hat wizard.png'],
}

CHARACTER_HEIGHT 	= 250
CHARACTER_CENTER_X = (SCREEN_WIDTH//2)-200
CHARACTER_BOTTOM_Y = SCREEN_HEIGHT*0.9
ARROW_SIZE = (40,40)


# =====================================================================
# 🎨 CUSTOMIZE SCENE FINAL (Correcciones de persistencia aplicadas)
# =====================================================================
class CustomizeScene(Scene):
    def __init__(self,game):
        super().__init__(game)
        self.font = pygame.font.Font(None,36)

        # Fondo
        self.background_img = pygame.transform.scale(
            load_image('ui','background customize.png'),
            (SCREEN_WIDTH,SCREEN_HEIGHT)
        )

        # 🌌 Estrellas GIF — fondo dinámico
        self.stars = StarField("images/ui/stars.gif",count=18,scale=1.1)

        # ✨ Partículas suaves constantes
        sparkle_area = pygame.Rect(CHARACTER_CENTER_X-60,450,300,200)
        self.sparkles = SparkleEmitter(sparkle_area,count=10)

        # 🌟 Spark burst (ONLY when user changes part)
        self.spark_burst = SparkBurst()

        # UI
        self.arrow_left_img 	= pygame.transform.scale(load_image('ui','arrow left.png'),ARROW_SIZE)
        self.arrow_right_img = pygame.transform.scale(load_image('ui','arrow right.png'),ARROW_SIZE)
        self.confirm_button_rect = pygame.Rect(SCREEN_WIDTH-250,SCREEN_HEIGHT-100,200,60)
        self.confirm_button_img = pygame.transform.scale(load_image('ui','button continue.png'),(200,60))

        # Selección inicial
        self.choices={'body':0,'head':0,'hat':0}

        # Nombre
        self.textbox = TextBox((SCREEN_WIDTH//2)+100,SCREEN_HEIGHT//2,300,50,
                                font=pygame.font.Font(None,40),initial_text="Tu Nombre")

        self.selector_rects=self._setup_selectors()


    # ---------------------------------------------------
    def _setup_selectors(self):
        w,h = ARROW_SIZE
        return{
            'hat': {'left':pygame.Rect(CHARACTER_CENTER_X-150,150,w,h),
                    'right':pygame.Rect(CHARACTER_CENTER_X+150,150,w,h)},
            'head':{'left':pygame.Rect(CHARACTER_CENTER_X-150,300,w,h),
                    'right':pygame.Rect(CHARACTER_CENTER_X+150,300,w,h)},
            'body':{'left':pygame.Rect(CHARACTER_CENTER_X-150,450,w,h),
                    'right':pygame.Rect(CHARACTER_CENTER_X+150,450,w,h)},
        }

    def _get_asset_path_key(self,t):
        return {"body":"bodies","head":"heads","hat":"hats"}[t]


    # 🔥 Aquí entra el SPARK BURST al cambiar selección
    def _cycle_part(self,part,direction):
        m=len(CHARACTER_PARTS[part])-1
        c=self.choices[part]
        self.choices[part]=(c+1)%(m+1) if direction=='next' else (c-1)%(m+1)

        # ► Spark explosion at avatar center
        self.spark_burst.trigger(CHARACTER_CENTER_X, CHARACTER_BOTTOM_Y-CHARACTER_HEIGHT//2)


    # ----------------------------------------------------
    def handle_input(self,event):
        self.textbox.handle_event(event)

        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.confirm_button_rect.collidepoint(event.pos):
                if self.textbox.text.strip() and self.textbox.text!="Tu Nombre":
                    self._save_character_to_state()
                    self.change_scene("ROOM")
                else: print("⚠ Ingresa un nombre para continuar")
                return

            for p,r in self.selector_rects.items():
                if r['right'].collidepoint(event.pos): self._cycle_part(p,'next')
                elif r['left'].collidepoint(event.pos): self._cycle_part(p,'prev')


    # ----------------------------------------------------
    def _save_character_to_state(self):
        """
        CORRECCIÓN CRÍTICA: Se usan los nombres de variables 'outfit_...' 
        que el GameState (y Player) espera para la persistencia.
        """
        g=self.game.state
        g.player_name=self.textbox.text
        
        # 🟢 CORRECCIÓN DE PERSISTENCIA (cambiado de g.character_head a g.outfit_head)
        g.outfit_body=CHARACTER_PARTS['body'][self.choices['body']]
        g.outfit_head=CHARACTER_PARTS['head'][self.choices['head']]
        
        hat=CHARACTER_PARTS['hat'][self.choices['hat']]
        g.outfit_hat = hat if hat!="None" else None 
        
        # Aseguramos que el jugador inicie en la posición por defecto de la siguiente escena
        g.player_x = 0.0 

        print(f"✔ Personaje '{g.player_name}' guardado. Head: {g.outfit_head}, Hat: {g.outfit_hat}")


    # ----------------------------------------------------
    def update(self,dt):
        self.stars.update(dt)
        self.sparkles.update(dt) # ⬅️ Lógica de update de SparkleEmitter
        self.spark_burst.update(dt)


    # ----------------------------------------------------
    def draw(self,screen):
        screen.blit(self.background_img,(0,0))
        self.stars.draw(screen)

        self._draw_composed_character(screen)

        # ✨ flotando suave + burst reactivo
        self.sparkles.draw(screen) # ⬅️ Lógica de draw de SparkleEmitter
        self.spark_burst.draw(screen)

        # UI ARROWS
        for p,rc in self.selector_rects.items():
            screen.blit(self.arrow_left_img,rc['left'])
            screen.blit(self.arrow_right_img,rc['right'])

        # Name box
        screen.blit(self.confirm_button_img,self.confirm_button_rect)
        screen.blit(self.font.render("INGRESA TU NOMBRE:",True,(255,255,255)),
                    (self.textbox.rect.x,self.textbox.rect.y-40))
        self.textbox.draw(screen)


    # =================================================================
    def _draw_composed_character(self, screen):
        x=CHARACTER_CENTER_X; y=CHARACTER_BOTTOM_Y
        parts=[]

        # cuerpo
        body=CHARACTER_PARTS['body'][self.choices['body']]
        body_img=load_image(self._get_asset_path_key('body'),body)
        sc=CHARACTER_HEIGHT/body_img.get_height()
        body_img=pygame.transform.scale(body_img,(int(body_img.get_width()*sc),CHARACTER_HEIGHT))
        body_rect=body_img.get_rect(midbottom=(x,y))
        parts.append((body_img,body_rect))

        # cabeza
        head=CHARACTER_PARTS['head'][self.choices['head']]
        head_img=load_image('heads',head)
        head_img=pygame.transform.scale(head_img,(int(head_img.get_width()*sc),int(head_img.get_height()*sc)))
        head_rect=head_img.get_rect(midbottom=(x,body_rect.top+50))
        parts.append((head_img,head_rect))

        # sombrero
        hat=CHARACTER_PARTS['hat'][self.choices['hat']]
        if hat!="None":
            hat_img=load_image('hats',hat)
            hat_img=pygame.transform.scale(hat_img,(int(hat_img.get_width()*sc),int(hat_img.get_height()*sc)))
            # Ajuste de posición para el sombrero
            hat_rect=hat_img.get_rect(midbottom=(x,head_rect.top)) 
            parts.append((hat_img,hat_rect))

        for img,rect in parts: screen.blit(img,rect)