import pygame as pg
import logging

from source.sprite import Sprite

class Graphics():
    def __init__(self):
        pass
        
    def setup(self):
        self.screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0])
        pg.display.set_caption("Cluster")
        pg.display.set_icon(pg.image.load("assets\\images\\icon.png"))
        
    def update(self, sprites: list[Sprite]):
        self.screen.fill(color="black")
        try: sorted_sprites: list[Sprite] = list(sprites.sort(key=lambda sprite: (sprite.scene_layer, sprite.position[1] if len(sprite.position) > 1 else 0)))
        except: 
            logging.warning("Graphics: unable to order sprites")
            return None
        
        for sprite in sorted_sprites:
            sprite.draw()