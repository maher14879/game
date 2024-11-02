from source.visual import Visual

class Sprite():
    def __init__(self, position: tuple[float], visual: Visual, scene_layer: int, box = None):
        self.visual = visual
        self.updates = [self.visual.update]
        self.interact_updates = []
        self.tick_updates = [self.visual.tick_update]
        self.scene_layer = scene_layer #low to high
        self.position = position
        self.box = box if box else visual.box
    
    def draw(self):
        self.visual
    
    def update(self, dt):
        for update in self.updates:
            update(dt)
            
    def interact_update(self, sprite, sprites):
        for interact_update in self.interact_updates:
            interact_update(sprite, sprites)
    
    def tick_update(self):
        for tick_update in self.tick_updates:
            tick_update()