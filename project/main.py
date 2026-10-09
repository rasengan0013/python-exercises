import os
import json
import random
from game.item import Item
from game.room import Room
from game.player import Player

SAVE_FILE = "savegame.json"


# ---------- 1. READING TEXT FILES ----------

def read_file(filename):
    """Reads intro.txt / instructions.txt located next to main.py."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return f"File {filename} not found."


# ---------- 2. CREATING THE WORLD ----------

def create_world():
    """Creates items and rooms. Returns (list of rooms, dict of items)."""
    key = Item("Golden Key", 0.5)
    sword = Item("Iron Sword", 3.2)
    potion = Item("Health Potion", 0.8)

    rooms = [
        Room("Entrance Hall", key),
        Room("Armory", sword),
        Room("Alchemy Lab", potion),
        Room("Sanctuary"),
    ]
    items = {i.name: i for i in (key, sword, potion)}
    return rooms, items


# ---------- 3. SAVE / LOAD ----------

def save_game(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "location": player.location.name,
        "items": [i.name for i in player.items],
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Game saved!")


def load_game(rooms, items):
    """Returns a new player built from the save file, or None if there is no save."""
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return None

    with open(SAVE_FILE, encoding="utf-8") as f:
        data = json.load(f)

    # find the room by name (fall back to the first room)
    room = next((r for r in rooms if r.name == data["location"]), rooms[0])
    player = Player(data["name"], room)
    player.hp = data["hp"]

    # put collected items back into the inventory and remove them from the rooms
    for name in data["items"]:
        player.items.append(items[name])
    for r in rooms:
        if r.item and r.item.name in data["items"]:
            r.item = None

    print(f"Welcome back, {player.name}!")
    return player


# ---------- 4. MENU COMMANDS ----------

def move_menu(player, rooms):
    for number, room in enumerate(rooms, start=1):
        print(f"{number}. {room.name}")
    choice = input("Room number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(rooms):
        player.move(rooms[int(choice) - 1])
    else:
        print("Invalid choice.")


def show_location(player):
    print(f"Location: {player.location.name}")
    item = player.location.item
    print(f"Item here: {item.name} ({item.weight} kg)" if item else "Item here: none")


def show_inventory(player):
    if not player.items:
        print("Inventory is empty.")
    for i in player.items:
        print(f"- {i.name} ({i.weight} kg)")


# ---------- 5. BOSS: THE GUARDIAN (3 ways to win) ----------

def guardian(player):
    """Returns True if the game is over (victory or death)."""
    if player.location.name != "Sanctuary":
        print("The Guardian is only in the Sanctuary.")
        return False

    names = [i.name for i in player.items]
    print("1. Fight  2. Stealth  3. Riddle")
    choice = input("Choose: ").strip()

    if choice == "1":                                   # FIGHT
        if "Iron Sword" not in names:
            print("You need the Iron Sword!")
            return False
        chance = min(100, 25 + 25 * len(player.items))  # 1 item = 50%, 2 = 75%, 3 = 100%
        print(f"Win chance: {chance}%")
        if random.randint(1, 100) <= chance:
            print("VICTORY! You took the Crystal of Fates by force!")
            return True
        player.hp -= 40
        print(f"The Guardian hit you! HP: {player.hp}")
        if player.hp <= 0:
            print("GAME OVER")
            return True

    elif choice == "2":                                 # STEALTH
        if "Golden Key" in names and "Health Potion" in names:
            print("VICTORY! The Guardian sleeps, you take the Crystal!")
            return True
        print("You need the Golden Key and the Health Potion.")

    elif choice == "3":                                 # RIDDLE
        answer = input("What has keys but no locks? ").strip().lower()
        if "keyboard" in answer:
            print("VICTORY! The Guardian lets you pass!")
            return True
        print("Wrong answer.")

    else:
        print("Invalid choice.")
    return False


# ---------- 6. MAIN PROGRAM ----------

def main():
    rooms, items = create_world()

    print("=== THE FORGOTTEN CITADEL ===")
    name = input("Enter your name: ").strip() or "Arthur"
    player = Player(name, rooms[0])

    while True:
        print(f"\n[{player.location.name} | HP: {player.hp}]")
        print("1 play  2 move  3 collect  4 location  5 inventory")
        print("6 interact  7 help  8 save  9 load  10 lopeta")
        command = input("Command: ").strip().lower()

        if command in ("play", "1"):
            print(read_file("intro.txt"))
        elif command in ("move", "2"):
            move_menu(player, rooms)
        elif command in ("collect", "3"):
            player.collect_item()
        elif command in ("location", "4"):
            show_location(player)
        elif command in ("inventory", "5"):
            show_inventory(player)
        elif command in ("interact", "6"):
            if guardian(player):
                break
        elif command in ("help", "7"):
            print(read_file("instructions.txt"))
        elif command in ("save", "8"):
            save_game(player)
        elif command in ("load", "9"):
            player = load_game(rooms, items) or player
        elif command in ("lopeta", "10"):
            print("Goodbye!")
            break
        else:
            print("Unknown command.")


main()