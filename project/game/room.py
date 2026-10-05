class Room:
    def __init__(self, name: str, item=None):
        self.name = name
        self.item = item

    def __str__(self):
        return self.name