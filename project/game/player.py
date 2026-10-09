class Player:
    """Player: name, current room, health and items."""
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.hp = 100
        self.items = []

    def move(self, room):
        self.location = room
        print(f"You moved to {room.name}.")

    def collect_item(self):
        item = self.location.item
        if item is None:
            print("No item in this room.")
            return
        self.items.append(item)       # add to inventory
        self.location.item = None     # remove from the room
        print(f"You collected {item.name}!")