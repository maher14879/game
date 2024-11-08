from source.sprite import Sprite
from source.functions import Vec

class Particle(Sprite):
    def __init__(self, position, visual, scene_layer = 1, box=None, direction: Vec = Vec((0, 0)), speed: float = 1., max_age = 1, 
                 rotation: float = None, spawn: "Particle" = None, spawn_speed: float = 1.):
        super().__init__(position, visual, scene_layer, box)
        self.updates[self.rotation_update, self.age_update, self.spawn_update]
        self.direction = direction
        self.speed = speed
        
        self.max_age = abs(max_age)
        self.age = 0
        
        self.rotation = rotation
        
        self.spawn = spawn
        self.spawn_speed = spawn_speed
        self.spawn_time = 0
        
    def new_position(self, dt) -> Vec:
        return self.position.add(self.direction.mul(self.speed).mul(dt))
    
    def rotation_update(self, dt):
        if self.rotation: self.direction = self.direction.rot(self.rotation * dt)
    
    def age_update(self, dt):
        self.age += dt
        if self.age >= self.max_age: self.kill = True
    
    def spawn_update(self, dt):
        if self.spawn:
            self.spawn_time += dt
            if self.spawn_time >= self.spawn_speed: 
                self.__dict__.update(self.spawn.__dict__)