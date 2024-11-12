import pygame as pg
import logging

pg.display.init()
pg.font.init()

scale = 1
basic_font = None
fonts_dict: dict[str, pg.font.Font] = {}
image_dict: dict[str, pg.surface.Surface] = {}

from source.functions import read_folder, Vec

def font_dict_setup(font_size):
    global basic_font
    global fonts_dict
    basic_font = pg.font.Font(pg.font.get_default_font(), font_size)
    for path in read_folder("assets\\fonts", "ttf"):
        fonts_dict[path] = pg.font.Font(path, font_size)

def image_dict_setup(image_size):
    global scale
    global image_dict
    scale = image_size
    for path in read_folder("assets\\images", "png"):
        image = pg.image.load(path)
        w, h = image.get_size()
        image_dict[path] = pg.transform.scale(image, (w * image_size, h * image_size))

def get_font(path: str):
    if not path in fonts_dict.keys():
        if path: logging.warning(f"Visuals: get_font not found for path {path}")
        return basic_font
    return fonts_dict[path]
    
def get_image(path: str):
    if not path in image_dict.keys():
        logging.warning(f"Visuals: get_image not found for path {path}")
        surface = pg.Surface(1,1)
        surface.fill("red")
        return surface
    return image_dict[path]

class Visual():
    def __init__(self, box: Vec = Vec((16, 16)), text: str = None, color: str = "white", font_path: str = None):
        self.is_visible = True
        self.show_figure = False
        self.border_width = 1
        self.updates = []
        self.box = box if type(box) == Vec else Vec(box)
        self.text = text
        self.color = color
        self.font_path = font_path
        self.surfaces = []
        self.setup()
        
    def setup(self):
        self.figure = self.create_figure()
        self.surface: pg.surface.Surface = get_font(self.font_path).render(self.text, True, self.color) if self.text else self.figure
        
    def update(self, dt):
        self.surfaces = [self.surface]
        
        if self.show_figure:
            if not self.box.mul(scale) == Vec(self.figure.get_size()): self.figure = self.create_figure()
            self.surfaces.append(self.figure)
        
        for update in self.updates:
            update(self, dt)
    
    def create_figure(self) -> pg.surface.Surface:
        figure = pg.Surface(self.box.mul(scale).to_tuple(), pg.SRCALPHA)
        rect_value = (0, 0, self.box.x - self.border_width, self.box.y - self.border_width)
        pg.draw.rect(figure, self.color, rect_value, self.border_width)
        return figure
    
def image_update(self: "Image", dt):
    self.surface = image_dict[self.image_path]

class Image(Visual):
    def __init__(self, image_path, box: Vec = Vec((0,0))):
        super().__init__(box)
        self.image_path = image_path
        self.updates.insert(0, image_update)
        
def frame_update(self: "Animation", dt):
    self.frame_dt += dt
    if self.frame_dt >= self.frame_rate: 
        if not self.animation_queue:
            if self.repeat: self.animation_queue = self.animation_path_list
            else: 
                self.is_visible = False
                self.updates.remove(frame_update)
                return None
            
        self.frame_dt -= self.frame_rate
        head, *tail = self.animation_queue
        self.surface = image_dict[head]
        self.animation_queue = tail
        
class Animation(Visual):
    def __init__(self, animation_path_list: list[str], frame_rate = 12, repeat: bool = True):
        super().__init__()
        if not animation_path_list: raise ValueError("Animation: path list is empty.")
            
        if len(animation_path_list) < 2: raise ValueError(f"Animation: given empty animation_path_list {animation_path_list}")
            
        self.animation_path_list = animation_path_list
        self.frame_rate = 1/frame_rate
        self.frame_dt = 0
        self.repeat = repeat
        
        head, *tail = animation_path_list
        self.animation_queue = tail
        self.surface = image_dict[head]
        
        self.updates.insert(0, frame_update)