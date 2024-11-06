import logging
import pickle
import os
import re

from source.functions import Random, Vec

from source.visual import Visual #testing
from source.sprite_types.sub.player import Player #testing
from assets.data.misc import start_settings #testing
from source.get_input import Input #testing

from source.sprite import Sprite

class Loader():
    def __init__(self, random: Random, render_distance = 5, chunk_size = 100):
        self.random = random
        self.render_distance = render_distance
        self.chunks: dict[str, list[Sprite]] = {}
        self.chunk_size = chunk_size
        self.id_pattern = re.compile(r"\((-?\d+),\s*(-?\d+)\)")
    
    def load_chunk(self, id: str):
        path = "save\\chunks\\" + id + ".pkl"
        if not os.path.exists(path):
            self.chunks[id] = self.create_chunk(id)
            return None
        
        with open(path, "rb") as file: 
            file.seek(0, 2)
            if file.tell() == 0:
                logging.warning(f"Loader: chunk with path {path} is empty")
                self.chunks[id] = self.create_chunk(id)
                return None
            file.seek(0)
            try: sprites: list[Sprite] = pickle.load(file)
            except:
                logging.warning(f"Loader: unable to load sprites in chunk {file}")
                return None
            for sprite in sprites: sprite.visual.setup()
            self.chunks[id] = sprites

    def save_chunk(self, id: str, chunk: list[Sprite]):
        if not chunk: 
            logging.warning(f"Loader: unable to save chunk with id {id} since it is empty")
            return None
        backup = [(sprite.visual.surface, sprite.visual.figure) for sprite in chunk]
        for sprite in chunk: 
            sprite.visual.surface = None
            sprite.visual.figure = None
            
        try: 
            with open(f"save\\chunks\\{id}.pkl", "wb") as file: pickle.dump(chunk, file)
        except: logging.warning(f"Loader: unable to save chunk with id {id}")
        
        for i, sprite in enumerate(chunk):
            surface, figure = backup[i]
            sprite.visual.surface = surface
            sprite.visual.figure = figure
    
    def setup(self):
        for i in range(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                self.load_chunk(str((i, j)))
    
    def save(self):
        for id, chunk in self.chunks.items():
            self.save_chunk(id, chunk)
    
    def chunk_update(self, center_position: Vec):
        center_i, center_j = center_position.mul(1 / self.chunk_size).to_tuple(True)
        for i in range(center_i - self.render_distance, center_i + self.render_distance):
            for j in range(center_j - self.render_distance, center_j + self.render_distance):
                id = str((i, j))
                if id not in self.chunks.keys(): self.chunks[id] = self.load_chunk(id)
                
        to_remove = []
        for id in self.chunks.keys():
            i, j = self.id_to_int(id)
            if not (abs(i - center_i) < self.render_distance and abs(j - center_j) < self.render_distance):
                self.save_chunk(id, self.chunks[id])
                to_remove.append(id)
                
        for id in to_remove:
            self.chunks.pop(id)
        
    def id_to_int(self, id: str):
        match = self.id_pattern.match(id)
        if not match: 
            logging.warning(f"Loader: could not match id {id}")
            return (0, 0)
        i, j = match.groups()
        return int(i), int(j)
                
    def create_chunk(self, id: str):
        return self.test(id)
        
    def test(self, id): #all test
        i, j =  self.id_to_int(id)
        if i==0 and j==0: 
            visual = Visual((100, 100), "player", "red")
            visual.show_figure = True
            return [Player(position=(0,0), visual=visual, name="player1", health=100, player_input=Input(start_settings["player_input"]))]
        visual = Visual((100, 100), id)
        return [Sprite((i * self.chunk_size / 2, j * self.chunk_size / 2), visual)]