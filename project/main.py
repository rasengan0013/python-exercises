import sys
from game.item import Item
from game.room import Room
from game.player import Player

def play_game():
    print("\n🎮 Game started! Have fun!")
    print("(This is a fictional game command)")

def show_score():
    print("\n📊 Your current score: 1337 points")
    print("(This is a fictional score)")

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
    print("Sound: ON")
    print("Music: ON")
    print("Difficulty: MEDIUM")
    print("(These are fictional settings)")

def display_help():
    print("\n📖 HELP INFORMATION")
    print("Available commands:")
    print("  play      - Start the game")
    print("  score     - Show your score")
    print("  move      - Move to another room")
    print("  collect   - Collect item from current room")
    print("  location  - Inspect current room and items")
    print("  inventory - View inventory")
    print("  help      - Show this help")
    print("  settings  - Open settings")
    print("  lopeta    - Exit the program")

# --- GAME INITIALIZATION ---

# 1. Create items (Item)
key_item = Item("Golden Key", 0.5)
sword_item = Item("Iron Sword", 3.2)
potion_item = Item("Health Potion", 0.8)

# 2. Create rooms (Room)
hall = Room("Entrance Hall", key_item)
armory = Room("Armory", sword_item)
laboratory = Room("Alchemy Lab", potion_item)

all_rooms = [hall, armory, laboratory]

# 3. Player registration
name = input("Enter your name: ").strip()
try:
    age = int(input("Enter your age: "))
except ValueError:
    print("❌ Invalid age input. Shutting down...")
    sys.exit()

if age < 12:
    print("You are a minor. Program shutting down...")
    sys.exit()
else:
    print(f"\nWelcome, {name}!")
    print(f"You are {age} years old.")

# 4. Create Player object with initial location
player = Player(name, location=hall)

# --- MAIN GAME LOOP ---

while True:
    print("\n" + "=" * 40)
    print(f"MAIN MENU | Location: {player.location.name}")
    print("=" * 40)
    print("1. play      - Start the game")
    print("2. score     - Show your score")
    print("3. move      - Move to another room")
    print("4. collect   - Collect item in current room")
    print("5. location  - Look around current room")
    print("6. inventory - Show inventory")
    print("7. help      - Display help information")
    print("8. settings  - Open settings")
    print("9. lopeta    - Exit the program")
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
        
    elif command in ["settings", "8"]:
        open_settings()
        
    elif command in ["lopeta", "9"]:
        print("\n👋 Goodbye! Thanks for playing!")
        break
        
    else:
        print("\n❌ Unknown command! Please try again.")