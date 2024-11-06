from source.sprite import Sprite
from source.visual import Visual

class Area(Sprite):
    def __init__(self, visual: Visual, scene_layer: int, health: int):
        super().__init__(visual, scene_layer)