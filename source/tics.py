import pygame as pg
import logging

class tics():
    def __init__(self):
        self.tick_speed = int()
        self.current_tick = float()
    
    def update(self, dt: float) -> bool:
        """Updates current_tick

        Args:
            dt (float): delta time

        Returns:
            bool: Whether a tick update has occured
        """
        self.current_tick += dt
        if self.current_tick >= self.tick_speed:
            self.current_tick -= self.tick_speed
            return True
        else: return False