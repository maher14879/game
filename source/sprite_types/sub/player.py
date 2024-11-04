from source.sprite_types.entity import Entity

class Player(Entity):
    def __init__(self, visual, scene_layer, health):
        super().__init__(visual, scene_layer, health)