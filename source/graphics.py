import pygame as pg
import logging

from source.sprite import Sprite
from source.visual import Visual
from source.functions import Vec, read_folder

scale = 1
basic_font = None
fonts_dict: dict[str, pg.font.Font] = {}
image_dict: dict[str, pg.surface.Surface] = {}

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
        image = pg.image.load(path).convert_alpha()
        w, h = image.get_size()
        image_dict[path] = pg.transform.scale(image, (w * image_size, h * image_size))

def get_font(path: str = None):
    if path not in fonts_dict.keys():
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

class SurfaceSprite(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position: Vec):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position.to_tuple())

class Graphics():
    def __init__(self, scale):
        self.scale = scale
        self.camera_speed = 2 
        self.edge_speed = 1 / 50
        self.camera = Vec((0,0))
        
    def setup(self):
        self.screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0])
        pg.display.set_caption("Cluster")
        pg.display.set_icon(pg.image.load("assets\\images\\icon.png"))
        screen_size = Vec(self.screen.get_size())
        self.screen_center = screen_size.mul(1 / 2)
        self.edge = self.screen_center.x - 70
        self.max_distance = screen_size.add(Vec((40 * self.scale, 40 * self.scale)))
        self.min_distance = Vec((-40 * self.scale, -40 * self.scale))
    
    def intro_text(self, text: str):
        center = self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2
        surface = get_font().render(text, True, "white")
        self.screen.blit(surface, center)
        pg.display.update()
        
    def update(self, dt, center: Vec, sprites: list[Sprite]):        
        center = center.mul(self.scale)
        difference = center.sub(self.camera)
        scalar = self.camera_speed * dt
        delta_cam = difference.mul(scalar)
        self.camera = self.camera.add(delta_cam)
        
        groups: dict[tuple[int, float], pg.sprite.Group] = {}
        
        for sprite in sprites:
            if not sprite.visual.is_visible: continue
            position = sprite.position.mul(self.scale).sub(self.camera).add(self.screen_center)
            position.y -= max(0, abs(self.screen_center.x - (position.x + sprite.box.x * 0.5 * self.scale)) - self.edge)**2 * self.edge_speed
            if not (position.less(self.max_distance) and self.min_distance.less(position)): continue

            key = (sprite.scene_layer, sprite.position.y)
            if key not in groups: groups[key] = pg.sprite.Group()
            
            if sprite.visual.text:
                font = get_font(sprite.visual.font_path)
                surface = font.render(sprite.visual.text, True, sprite.visual.color)
                groups[key].add(SurfaceSprite(surface, position))
            
            for image in sprite.visual.images:
                groups[key].add(SurfaceSprite(get_image(image), position))

            if sprite.visual.show_figure:
                surface = pg.Surface(sprite.visual.box.mul(scale).to_tuple(), pg.SRCALPHA)
                rect_value = (0, 0, sprite.visual.box.x * scale - sprite.visual.border_width, sprite.visual.box.y * scale - sprite.visual.border_width)
                pg.draw.rect(surface, sprite.visual.color, rect_value, sprite.visual.border_width)
                groups[key].add(SurfaceSprite(surface, position))

        self.screen.fill(color="black")
        for scene_layer, id in sorted(groups.keys()):
            try: groups[(scene_layer, id)].draw(self.screen)
            except Exception as e: raise ValueError(f"Graphics: unable to draw group {id} in scene layer {scene_layer}. Error: {e}")

        pg.display.update()