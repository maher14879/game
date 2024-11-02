from source.visual import Visual

class Sprite():
    def __init__(self, visual: Visual, scene_layer: int):
        self.visual = visual
        self.updates = [self.visual.update]
        self.tick_updates = [self.visual.tick_update]
        self.scene_layer = scene_layer #low to high
    
    def draw(self):
        self.visual
    
    def update(self, dt):
        for update in self.updates:
            update(dt)
    
    def tick_update(self):
        for tick_update in self.tick_updates:
            tick_update()