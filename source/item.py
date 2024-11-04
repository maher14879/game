from source.visual import Visual

class Item():
    def __init__(self, name: str, visual: Visual, durability: int = None):
        self.name = name
        self.visual = visual
        self.durability = durability