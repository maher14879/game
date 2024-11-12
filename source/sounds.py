import pygame as pg
import logging

from source.functions import read_folder

class Sounds():
    def __init__(self):
        self.sounds: dict[str, pg.mixer.Sound] = {}
    
    def setup(self):
        for path in read_folder("assets\\sound", ".ogg"):
            try: self.sounds[path] = pg.mixer.Sound(path)
            except: 
                logging.warning(f"Sounds: Unable to convert {path} to Sound")
                continue

    def play(self, sound_name: str, volume: float = 1, channel_num: int = None, must_play: bool = False):
        """Play a sound on a specified or free channel.

        Args:
            class_name (str): Name of the sound to play.
            volume (float): Volume level (0.0 to 100.0).
            channel_num (int, optional): Specific channel to play on. If None, uses a free channel.
        """
        if not sound_name in self.sounds.keys(): raise ValueError(f"Sounds: {sound_name} does not exist")
            
        sound = self.sounds[sound_name]
        sound.set_volume(volume)

        if channel_num: channel = pg.mixer.Channel(channel_num)
        else: channel = pg.mixer.find_channel()

        if channel: channel.play(sound)
        elif must_play: pg.mixer.Channel(1).play(sound)
        else: logging.warning(f"Sounds: No available channel to play sound {sound_name}")
            
    def len(self, sound_name: str):
        if not sound_name in self.sounds.keys(): raise ValueError(f"Sounds: {sound_name} does not exist")
        
        sound = self.sounds[sound_name]
        return sound.get_length()
    
sounds = Sounds()