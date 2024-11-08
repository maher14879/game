from source.sprite import Sprite

class Area(Sprite):
    def __init__(self, position, visual, scene_layer = 1, box=None):
        super().__init__(position, visual, scene_layer, box)
        