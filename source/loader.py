import pygame as pg
import logging
import json
import os
import re

from source.sprite import Sprite
from source.functions import choose_type

class Loader():
    def __init__(self, render_distance = 5, chunk_size = 16):
        self.render_distance = render_distance
        self.chunks: dict[str, list[Sprite]] = {}
        self.chunk_size = chunk_size
        self.id_pattern = re.compile(r"\((\d+),(\d+)\)")
    
    def load_chunk(self, id: str):
        path = "save\\chunks\\" + id + ".json"
        if os.path.exists(path):
            with open(path, "r") as file: 
                json_file: dict[str, list[dict]] = json.load(file)
                sprites = []
                for sprite_dict in json_file["data"]:
                    sprite = choose_type(sprite_dict.pop("type"))
                    for name, value in sprite_dict.items():
                        setattr(sprite, name, value)
                    sprites.append(sprite)
                self.chunks[id] = sprites
        self.chunks[id] = self.create_chunk(id)

    def save_chunk(self, id: str, chunk: list[Sprite]):
        sprite_dict_lst = [{"type":type(sprite)}.update(vars(sprite)) for sprite in chunk]
        with open("save\\chunks\\" + id + ".json", "w") as file: json.dump(file, sprite_dict_lst)
    
    def setup(self):
        for i in range(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                self.load_chunk(str((i, j)))
    
    def save(self):
        for id, chunk in self.chunks.values():
            self.save_chunk(id, chunk)
    
    def chunk_update(self, center_position: tuple[float, float]):
        center_i = round(center_position[0] / self.chunk_size)
        center_j = round(center_position[1] / self.chunk_size)
        for i in range(center_i - self.render_distance, center_i + self.render_distance):
            for j in range(center_j - self.render_distance, center_j + self.render_distance):
                id = str((i, j))
                if id not in self.chunks.keys(): self.chunks[id] = self.load_chunk(id)
                
        for id in self.chunks.keys():
            match = self.id_pattern.match(id)
            if not match: 
                logging.warning(f"Loader: could not match id {id}")
                continue
            i, j = match.groups()
            if not (abs(i - center_i) < self.render_distance and abs(j - center_j) < self.render_distance):
                self.save_chunk(id, self.chunks.pop(id)) 
                
    def create_chunk(self, id: str):
        pass