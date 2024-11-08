import pygame as pg
import logging

from source.sprite import Sprite
from source.visual import Visual
from source.functions import Vec

class Graphics():
    def __init__(self):
        self.camera_speed = 2
        self.camera = Vec((0,0))
        
    def setup(self):
        self.screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0])
        pg.display.set_caption("Cluster")
        pg.display.set_icon(pg.image.load("assets\\images\\icon.png"))
        screen_size = Vec(self.screen.get_size())
        self.screen_center = screen_size.mul(1 / 2)
    
    def intro_text(self, text: str):
        visual = Visual(text=text)
        center = self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2
        self.screen.blit(visual.surface, center)
        pg.display.update()
        
    def update(self, dt, center: Vec, sprites: list[Sprite]):
        self.screen.fill(color="black")
        try: sprites.sort(key=lambda sprite: (sprite.scene_layer, sprite.position.y, sprite.position.x))
        except: 
            logging.warning(f"Graphics: unable to order sprites")
   
        difference = center.sub(self.camera)
        scalar = self.camera_speed * dt
        delta_cam = difference.mul(scalar)
        self.camera = self.camera.add(delta_cam)
        
        for sprite in sprites:
            if not sprite.visual.is_visible: continue
            try:
                position = sprite.position.sub(self.camera).add(self.screen_center)
                if not position.less(self.screen_center.mul(2)) and Vec((0,0)).less(position): continue
                for surface in sprite.visual.surfaces: self.screen.blit(surface, position.to_tuple())
            except:
                logging.warning(f"Graphics: unable to draw sprite {vars(sprite)}")
        pg.display.update()
        
    def tick_update(self, sprites: list[Sprite], show_figure: bool = False):
        if show_figure:
            for sprite in sprites: sprite.visual.show_figure = True
        