import os
import logging

def read_folder(path: str, type: None) -> list[str]:
    return os.listdir(path)