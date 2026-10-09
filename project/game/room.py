class Room:
    """Room: a name and an item inside (or None)."""
    def __init__(self, name, item=None):
        self.name = name
        self.item = item