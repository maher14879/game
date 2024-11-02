import pygame as pg
import logging
import sys

from source.loader import Loader
from source.graphics import Graphics
from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sprite_types.tile import Tile

from source.functions import create_new_pos

class Tick():
    def __init__(self):
        self.tick_speed = int()
        self.current_tick = float()
    
    def update(self, dt: float) -> bool:
        self.current_tick += dt
        if self.current_tick >= self.tick_speed:
            self.current_tick -= self.tick_speed
            return True
        else: return False

class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
    
    def setup(self):
        self.clock = pg.time.Clock()
        self.loader = Loader()
        self.tick = Tick()
        self.graphics = Graphics()
        
        self.loader.setup()
        self.graphics.setup()
    
    def save_settings(self):
        self.loader.setup()
        pass
    
    def run(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_settings()
                self.loader.save()
                pg.quit()
                sys.exit()
                
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.display.iconify()
                
        dt = self.clock.tick() / 1000
        sprites: list[Sprite] = []
        for chunk in self.loader.chunks:
            for sprite in chunk.values():
                sprites.append(sprite)
                
        for sprite in sprites:
            sprite.update(dt)
            sprite.interact_update(sprite, sprites)
            if self.tick.update(dt): sprite.tick_update()
            
        entities = [sprite for sprite in sprites if isinstance(sprite, Entity)]
        tiles = [sprite for sprite in sprites if isinstance(sprite, Entity)]
        
        for entity in entities:
            for tile in tiles:
                new_position = create_new_pos(entity.new_position(dt), entity.box, tile.position, entity.box)
                if any(not new_position): tile.collision_update()
                else: entity.update_position(new_position)

        self.graphics.update(sprites)