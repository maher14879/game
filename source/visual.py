import pygame as pg
import logging
from source.functions import Vec

pg.display.init()
pg.font.init()

class Visual():
    def __init__(self, box: Vec = Vec((16, 8)), text: str = None, color: str = "white", font_path: str = None):
        self.is_visible = True
        self.show_figure = False
        self.border_width = 1
        self.updates = []
        self.box = box if type(box) == Vec else Vec(box)
        self.text = text
        self.color = color
        self.font_path = font_path
        self.image = None
        self.images = []
        
    def update(self, dt):
        self.images = [self.image] if self.image else []
        
        for update in self.updates:
            update(self, dt)

class Image(Visual):
    def __init__(self, image_path, box: Vec = Vec((16, 8))):
        super().__init__(box)
        self.image = image_path
        
def frame_update(self: "Animation", dt):
    self.frame_dt += dt
    
    if not self.frame_dt >= self.frame_rate: return None
    self.frame_dt -= self.frame_rate
    
    if not self.animation_queue:
        if not self.repeat:
            self.is_visible = False
            self.updates.remove(frame_update)
            return None
        
        head, *tail = self.animation_path_list
        self.image = head
        self.animation_queue = tail
        
    head, *tail = self.animation_queue
    self.image = head
    self.animation_queue = tail

        
class Animation(Visual):
    def __init__(self, animation_path_list: list[str], frame_rate = 12, repeat: bool = True, box: Vec = Vec((16, 8))):
        super().__init__(box)
        
        if not animation_path_list: raise ValueError("Animation: path list is empty.")
        if len(animation_path_list) < 2: raise ValueError(f"Animation: given animation_path_list that is too short {animation_path_list}")
            
        self.animation_path_list = animation_path_list
        self.frame_rate = 1/frame_rate
        self.frame_dt = 0
        self.repeat = repeat
        
        head, *tail = animation_path_list
        self.animation_queue = tail
        self.image = head
        
        self.updates.insert(0, frame_update)