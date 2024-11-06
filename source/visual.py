import pygame as pg
import logging

from source.functions import read_folder, Vec

pg.display.init()
pg.font.init()

font_size = 15
font = pg.font.Font(pg.font.get_default_font(), font_size)

fonts_dict: dict[str, pg.font.Font] = {}
for path in read_folder("assets\\fonts", ".ttf"):
    fonts_dict[path] = pg.font.Font(path, font_size)

def get_font(path: str):
    if not path in fonts_dict.keys():
        if path: logging.warning(f"Visuals: get_font not found for path {path}")
        return font
    return fonts_dict[path]

image_dict: dict[str, pg.surface.Surface] = {}
for path in read_folder("assets\\images", ".png"):
    image_dict[path] = pg.image.load(path)
    
def get_image(path: str):
    if not path in image_dict.keys():
        logging.warning(f"Visuals: get_image not found for path {path}")
        surface = pg.Surface(1,1)
        surface.fill("red")
        return surface
    return image_dict[path]

class Visual():
    def __init__(self, box: Vec = Vec((1, 1)), text: str = None, color: str = "white", font_path: str = None):
        self.is_visible = True
        self.show_figure = False
        self.border_width = 1
        self.updates = [self.figure_update]
        
        self.box = box if type(box) == Vec else Vec(box)
        self.text = text
        self.color = color
        self.font_path = font_path
        self.setup()
        
    def setup(self):
        self.figure = self.create_figure()
        self.surface: pg.surface.Surface = get_font(self.font_path).render(self.text, True, self.color) if self.text else self.figure
        
    def figure_update(self, dt):
        if self.show_figure:
            surface_size = Vec(self.surface.get_size())
            figure_size = Vec(self.figure.get_size())
            if surface_size == (new_size := self.box.max(surface_size)): return None
            if not self.box == figure_size: self.figure = self.create_figure()
            center = new_size.mul(0.5)
            new_surface = pg.Surface(new_size.to_tuple(), pg.SRCALPHA)
            new_surface.blit(self.surface, center.to_tuple())
            new_surface.blit(self.figure, center.to_tuple())
            self.surface = new_surface
    
    def create_figure(self) -> pg.surface.Surface:
        figure = pg.Surface(self.box.to_tuple(), pg.SRCALPHA)
        rect_value = (0, 0, self.box.x - self.border_width, self.box.y - self.border_width)
        pg.draw.rect(figure, self.color, rect_value, self.border_width)
        return figure
    
class Image(Visual):
    def __init__(self, image_path, figure = None):
        super().__init__(figure)
        self.image_path = image_path
        self.surface = image_dict[image_path]
        
class Animation(Visual):
    def __init__(self, animation_path_list: list[str], frame_rate = 24, repeat: bool = True, figure = None,):
        super().__init__(figure)
        if not animation_path_list: logging.warning("Animation: given empty animation_path_list")
        self.animation_path_list = animation_path_list
        self.frame_rate = frame_rate
        self.frame_dt = 0
        self.repeat = repeat
        
        head, *tail = animation_path_list
        self.animation_queue = tail
        self.surface = image_dict[head]
        
        self.updates.append(self.frame_update)
    
    def frame_update(self, dt):
        self.frame_dt += dt
        if self.frame_dt >= self.frame_rate: 
            if not self.animation_queue:
                if self.repeat: self.animation_queue = self.animation_path_list
                else: 
                    self.is_visible = False
                    self.updates.remove(self.update)
                    return None
                
            self.frame_dt -= self.frame_rate
            head, *tail = self.animation_queue
            self.surface = image_dict[head]
            self.animation_queue = tail