import pygame as pg

from source.visual import Visual
from source.functions import Vec

class Sprite():
    def __init__(self, position: Vec, visual: Visual, scene_layer: int = 1, box = None):
        self.visual = visual
        self.spawn_list: list[Sprite] = []
        self.updates = []
        self.interact_updates = []
        self.tick_updates = []
        self.kill_on_update = False
        self.scene_layer = scene_layer
        self.position = Vec(position)
        self.box = box if box else visual.box
    
    def update(self, dt):
        for update in self.updates:
            update(self, dt)
        
        self.visual.update(dt)
            
    def interact_update(self, sprites):
        for interact_update in self.interact_updates:
            interact_update(self, sprites)
    
    def tick_update(self):
        for tick_update in self.tick_updates:
            tick_update(self)