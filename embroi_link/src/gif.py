from pathlib import Path
import random

GIF_DIR = Path.cwd() / "embroi_link/res/gifs"


class Gif:
    def __init__(self):
        self.gif_paths = []
        self.load_gifs()

    def load_gifs(self):
        self.gif_paths = []
        for element in GIF_DIR.iterdir():
            if element.is_file():
                self.gif_paths.append(str(element))

    def get_random(self):
        return random.choice(self.gif_paths)
