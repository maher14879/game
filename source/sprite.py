from source.visual import Visual
from source.functions import Vec

class Sprite():
    def __init__(self, position: Vec, visual: Visual, scene_layer: int = 1, box = None):
        self.kill = False
        self.visual = visual
        self.updates = self.visual.updates
        self.interact_updates = []
        self.tick_updates = []
        self.scene_layer = scene_layer #low render first
        self.position = Vec(position)
        self.box = box if box else visual.box
    
    def update(self, dt):
        for update in self.updates:
            update(dt)
            
    def interact_update(self, sprites):
        for interact_update in self.interact_updates:
            interact_update(sprites)
    
    def tick_update(self):
        for tick_update in self.tick_updates:
            tick_update()