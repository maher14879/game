import pygame as pg
import logging
import sys

from source.loader import Loader
from source.graphics import Graphics

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
        for chunk in self.loader.chunks:
            for sprite in chunk.values():
                sprite.update(dt)
            
            if self.tick.update(dt):
                for sprite in chunk.values():
                    sprite.tick_update()
        
        self.graphics.update()