class Player:
    def __init__(self, name: str, location):
        self.name = name
        self.location = location
        self.items = []

    def move(self, destination):
        """Moves the player to a new room."""
        self.location = destination
        print(f"🚶 You moved to {self.location.name}.")

    def collect_item(self):
        """Collects an item from the current room."""
        if self.location.item:
            picked_item = self.location.item
            self.items.append(picked_item)
            self.location.item = None
            print(f"✨ You collected '{picked_item.name}' ({picked_item.weight} kg)!")
        else:
            print("❌ There is no item to collect in this room.")