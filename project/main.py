import sys
import json
import os
from game.item import Item
from game.room import Room
from game.player import Player

# FILE & SAVE SYSTEM FUNCTIONS

def read_text_file(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"⚠️ File '{filename}' not found."

def save_game(player, filename="savegame.json"):
    save_data = {
        "name": player.name,
        "location": player.location.name,
        "items": [item.name for item in player.items]
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
        print(f"\n💾 Game saved successfully to '{filename}'!")
    except Exception as e:
        print(f"\n❌ Error saving game: {e}")

def load_game(all_rooms, all_items):
    filename = "savegame.json"
    if not os.path.exists(filename):
        print("\n⚠️ No save file found!")
        return None, None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        saved_room = next((r for r in all_rooms if r.name == save_data["location"]), all_rooms[0])
        
        loaded_player = Player(save_data["name"], location=saved_room)
        
        for item_name in save_data.get("items", []):
            if item_name in all_items:
                loaded_player.items.append(all_items[item_name])

        print(f"\n📂 Welcome back, {loaded_player.name}! Game loaded successfully.")
        return loaded_player, save_data
    except Exception as e:
        print(f"\n❌ Failed to load save file: {e}")
        return None, None

# GAME INTERFACE FUNCTIONS

def play_game():
    print("\n" + read_text_file("intro.txt"))

def show_score():
    print("\n📊 Your current score: 1337 points")

def show_inventory(player):
    print(f"\n🎒 INVENTORY OF {player.name.upper()}")
    if not player.items:
        print("Your inventory is empty.")
    else:
        for index, item in enumerate(player.items, start=1):
            print(f"  {index}. {item.name} (Weight: {item.weight} kg)")

def move_menu(player, rooms):
    print("\n🚪 Available Rooms:")
    for idx, room in enumerate(rooms, start=1):
        status = " (Current)" if room == player.location else ""
        print(f"  {idx}. {room.name}{status}")
    
    choice = input("Select a room number to move to: ").strip()
    if choice.isdigit():
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(rooms):
            dest_room = rooms[choice_idx]
            if dest_room == player.location:
                print("⚠️ You are already in this room.")
            else:
                player.move(dest_room)
        else:
            print("❌ Invalid room selection.")
    else:
        print("❌ Please enter a valid number.")

def show_location_info(player):
    print(f"\n📍 Current Location: {player.location.name}")
    if player.location.item:
        print(f"🔍 Item in room: {player.location.item.name} (Weight: {player.location.item.weight} kg)")
    else:
        print("🔍 Item in room: None")

def open_settings():
    print("\n⚙️ SETTINGS")
    print("Sound: ON | Music: ON | Difficulty: MEDIUM")

def display_help():
    print("\n" + read_text_file("instructions.txt"))

# GAME INITIALIZATION 

key_item = Item("Golden Key", 0.5)
sword_item = Item("Iron Sword", 3.2)
potion_item = Item("Health Potion", 0.8)

all_items = {
    "Golden Key": key_item,
    "Iron Sword": sword_item,
    "Health Potion": potion_item
}

hall = Room("Entrance Hall", key_item)
armory = Room("Armory", sword_item)
laboratory = Room("Alchemy Lab", potion_item)

all_rooms = [hall, armory, laboratory]

print("=" * 50)
print("       WELCOME TO THE FORGOTTEN CITADEL")
print("=" * 50)

player = None
if os.path.exists("savegame.json"):
    ans = input("Found a saved game! Do you want to continue? (y/n): ").strip().lower()
    if ans in ['y', 'yes']:
        player, _ = load_game(all_rooms, all_items)

if not player:
    name = input("Enter your name: ").strip()
    if not name:
        name = "Arthur"
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("❌ Invalid age input. Shutting down...")
        sys.exit()

    if age < 12:
        print("You are a minor. Program shutting down...")
        sys.exit()
    else:
        print(f"\nWelcome, {name}! You are {age} years old.")

    player = Player(name, location=hall)

#  MAIN GAME LOOP 

while True:
    print("\n" + "=" * 40)
    print(f"MAIN MENU | Location: {player.location.name}")
    print("=" * 40)
    print("1. play      - Read intro & story")
    print("2. score     - Show your score")
    print("3. move      - Move to another room")
    print("4. collect   - Collect item in current room")
    print("5. location  - Look around current room")
    print("6. inventory - Show inventory")
    print("7. help      - Display instructions")
    print("8. save      - Save game state")
    print("9. load      - Load game state")
    print("10. settings - Open settings")
    print("11. lopeta   - Exit the program")
    print("=" * 40)
    
    command = input("Enter command: ").strip().lower()
    
    if command in ["play", "1"]:
        play_game()
        
    elif command in ["score", "2"]:
        show_score()
        
    elif command in ["move", "3"]:
        move_menu(player, all_rooms)
        
    elif command in ["collect", "4"]:
        player.collect_item()
        
    elif command in ["location", "5"]:
        show_location_info(player)
        
    elif command in ["inventory", "6"]:
        show_inventory(player)
        
    elif command in ["help", "7"]:
        display_help()

    elif command in ["save", "8"]:
        save_game(player)

    elif command in ["load", "9"]:
        loaded_p, _ = load_game(all_rooms, all_items)
        if loaded_p:
            player = loaded_p
        
    elif command in ["settings", "10"]:
        open_settings()
        
    elif command in ["lopeta", "11"]:
        print("\n👋 Goodbye! Thanks for playing!")
        break
        
    else:
        print("\n❌ Unknown command! Please try again.")