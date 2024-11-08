import pygame as pg
import logging

from source.functions import read_folder

class Sounds():
    def __init__(self):
        self.sounds: dict[str, pg.mixer.Sound] = {}
    
    def setup(self):
        for path in read_folder("assets\\sound", ".ost"):
            try: sound_name = path.replace("\\", "_")
            except: 
                logging.warning(f"Sounds: Unable to convert {path} to sound_name")
                continue
            
            try: self.sounds[sound_name] = pg.mixer.Sound(path)
            except: 
                logging.warning(f"Sounds: Unable to convert {path} to Sound")
                continue

    def play(self, sound_name: str, must_play: bool = False, volume: float = 100.0, channel_num: int = None):
        """Play a sound on a specified or free channel.

        Args:
            class_name (str): Name of the sound to play.
            volume (float): Volume level (0.0 to 100.0).
            channel_num (int, optional): Specific channel to play on. If None, uses a free channel.
        """
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume / 100)

            if channel_num: channel = pg.mixer.Channel(channel_num)
            else: channel = pg.mixer.find_channel()

            if channel: channel.play(sound)
            elif must_play: pg.mixer.Channel(1).play(sound)
            else: logging.warning(f"Sounds: No available channel to play sound {sound_name}")