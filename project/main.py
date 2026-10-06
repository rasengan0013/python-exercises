import sys
import json
import os
import random
import time
from game.item import Item
from game.room import Room
from game.player import Player


# 1. CONSTANTS & COLOR DEFINITIONS (ANSI)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"



# 2. FILE SAVE


def read_text_file(filename: str) -> str:
    """Reads and returns text from a file located in the script directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"{YELLOW}⚠️ File '{filename}' not found.{RESET}"


def save_game(player: Player, filename: str = "savegame.json") -> None:
    """Saves player state, location, HP, and inventory into a JSON file."""
    save_data = {
        "name": player.name,
        "hp": getattr(player, 'hp', 100),
        "location": player.location.name,
        "items": [item.name for item in player.items]
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
        print(f"\n{GREEN}💾 Game saved successfully to '{filename}'!{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Error saving game: {e}{RESET}")


def load_game(all_rooms: list, all_items: dict):
    """Loads saved game state from a JSON file and reconstructs Player object."""
    filename = "savegame.json"
    if not os.path.exists(filename):
        print(f"\n{YELLOW}⚠️ No save file found!{RESET}")
        return None, None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        saved_room = next((r for r in all_rooms if r.name == save_data["location"]), all_rooms[0])
        
        loaded_player = Player(save_data["name"], location=saved_room)
        loaded_player.hp = save_data.get("hp", 100)
        
        for item_name in save_data.get("items", []):
            if item_name in all_items:
                loaded_player.items.append(all_items[item_name])

        print(f"\n{GREEN}📂 Welcome back, {loaded_player.name}! Game loaded successfully.{RESET}")
        return loaded_player, save_data
    except Exception as e:
        print(f"\n{RED}❌ Failed to load save file: {e}{RESET}")
        return None, None



# 3. UI


def play_game():
    """Displays introductory lore from intro.txt."""
    print("\n" + read_text_file("intro.txt"))


def show_score():
    """Displays current score."""
    print(f"\n{CYAN}📊 Your current score: 1337 points{RESET}")


def show_inventory(player: Player):
    """Lists all items currently held in the player's inventory."""
    print(f"\n🎒 INVENTORY OF {player.name.upper()}")
    if not player.items:
        print("Your inventory is empty.")
    else:
        for index, item in enumerate(player.items, start=1):
            print(f"  {index}. {item.name} (Weight: {item.weight} kg)")


def move_menu(player: Player, rooms: list):
    """Handles room navigation menu and input parsing."""
    print("\n🚪 Available Rooms:")
    for idx, room in enumerate(rooms, start=1):
        status = f" {GREEN}(Current){RESET}" if room == player.location else ""
        print(f"  {idx}. {room.name}{status}")
    
    choice = input("Select a room number to move to: ").strip()
    if choice.isdigit():
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(rooms):
            dest_room = rooms[choice_idx]
            if dest_room == player.location:
                print(f"{YELLOW}⚠️ You are already in this room.{RESET}")
            else:
                player.move(dest_room)
        else:
            print(f"{RED}❌ Invalid room selection.{RESET}")
    else:
        print(f"{RED}❌ Please enter a valid number.{RESET}")


def show_location_info(player: Player):
    """Displays current location and any available item in it."""
    print(f"\n📍 Current Location: {CYAN}{player.location.name}{RESET}")
    if player.location.item:
        print(f"🔍 Item in room: {YELLOW}{player.location.item.name}{RESET} (Weight: {player.location.item.weight} kg)")
    else:
        print("🔍 Item in room: None")


def open_settings():
    """Displays settings configuration panel."""
    print("\n⚙️ SETTINGS")
    print("Sound: ON | Music: ON | Difficulty: MEDIUM")


def display_help():
    """Displays help text from instructions.txt."""
    print("\n" + read_text_file("instructions.txt"))



# 4. GAMEPLAY


def interact_with_guardian(player: Player):
    """
    Handles encounter logic with the Guardian at the Sanctuary Gate.
    Offers 3 completion routes:
      1. Combat (Direct Attack)
      2. Stealth (Subduing with Potion + Key)
      3. Diplomacy / Riddle Negotiation
    """
    if player.location.name != "Sanctuary (Gate)":
        print(f"\n{YELLOW}⚠️ You can only interact with the Guardian at the Citadel Gate in Sanctuary!{RESET}")
        return

    inventory_names = [item.name for item in player.items]
    
    print(f"\n{CYAN}🗿 ANCIENT GUARDIAN BLOCKS THE CRYSTAL OF FATES!{RESET}")
    print("Choose your approach:")
    print("1. Combat Route (Strength)")
    print("2. Stealth Route (Intellect)")
    print("3. Diplomacy Route (Riddle)")

    choice = input("Choose path (1/2/3): ").strip()

    # Route 1: Strength / Combat
    if choice == "1":
        if "Iron Sword" not in inventory_names:
            print(f"\n{RED}❌ You need at least the 'Iron Sword' from the Armory to fight the Guardian!{RESET}")
            return

        item_count = len(player.items)
        win_chance = 50 if item_count == 1 else (75 if item_count == 2 else 100)

        print(f"\n{RED}😱 Dread grips your heart as an overwhelming aura radiates from the ancient construct...{RESET}")
        time.sleep(1.5)
        
        hp_color = GREEN if player.hp > 40 else RED
        print(f"\n⚔️ [PATH 1 - STRENGTH PREVIEW]")
        print(f"❤️ Your Current HP: {hp_color}{player.hp} HP{RESET}")
        print(f"🎒 Items prepared: {item_count}/3")
        print(f"📊 Calculated Win Chance: {CYAN}{win_chance}%{RESET}")
        
        if win_chance < 100:
            print(f"{YELLOW}⚠️ Warning: You have a {100 - win_chance}% chance of taking damage and retreating!{RESET}")
        else:
            print(f"{GREEN}✨ Your victory is guaranteed (100%)!{RESET}")

        confirm = input("\nDo you want to proceed with the attack? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{YELLOW}🛡️ You backed away safely to prepare further.{RESET}")
            return

        print(f"\n{BOLD}⚔️ Attacking the Guardian...{RESET}")
        time.sleep(2)
        
        roll = random.randint(1, 100)
        
        if roll <= win_chance:
            time.sleep(1)
            print(f"\n{GREEN}🔥 You charge with overwhelming power! The Guardian's magical core shatters!{RESET}")
            print(f"{GREEN}🏆 VICTORY (Route 1)! You retrieved the Crystal of Fates through force!{RESET}")
            sys.exit()
        else:
            damage = 40
            player.hp -= damage
            time.sleep(1)
            print(f"\n{RED}💥 The Guardian blocked your blow and knocked you back!{RESET}")
            print(f"{RED}💔 You lost {damage} HP! Current HP: {player.hp}{RESET}")
            
            if player.hp <= 0:
                time.sleep(1)
                print(f"\n{RED}☠️ GAME OVER: You succumbed to your injuries...{RESET}")
                sys.exit()
            else:
                print(f"{YELLOW}💡 Tip: Collect more items or heal up before attacking again!{RESET}")

    # Route 2: Stealth
    elif choice == "2":
        if "Golden Key" in inventory_names and "Health Potion" in inventory_names:
            print(f"\n{CYAN}🧪 Preparing sleep mixture...{RESET}")
            time.sleep(1.5)
            print(f"{GREEN}The Guardian falls into a deep slumber. You slip past quietly and unlock the gate!{RESET}")
            print(f"{GREEN}🏆 VICTORY (Route 2)! You retrieved the Crystal of Fates without raising an alarm!{RESET}")
            sys.exit()
        else:
            print(f"\n{RED}❌ You need both the 'Golden Key' (Entrance) and 'Health Potion' (Alchemy Lab) for stealth!{RESET}")

    # Route 3: Diplomacy
    elif choice == "3":
        print(f"\n{CYAN}🗣️ The Guardian turns its ancient gaze upon you...{RESET}")
        time.sleep(1)
        print(f"{BOLD}\"To pass without bloodshed, answer this: What has keys but no locks, space but no room, and you can enter but not go in?\"{RESET}")
        
        answer = input("Your answer: ").strip().lower()
        if "keyboard" in answer:
            time.sleep(1)
            print(f"\n{GREEN}🗿 The Guardian bows respectfully: \"Wise traveler, you may pass.\"")
            print(f"🏆 VICTORY (Route 3)! You unlocked the gate using wisdom and peace!{RESET}")
            sys.exit()
        else:
            time.sleep(1)
            print(f"\n{RED}❌ The Guardian shakes its head. \"Incorrect answer.\" You back away.{RESET}")

    else:
        print(f"{RED}❌ Invalid selection.{RESET}")



# 5. INITIALIZATION & SETUP


# Initialize Game Objects (Items and Rooms)
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
sanctuary = Room("Sanctuary (Gate)", None)

all_rooms = [hall, armory, laboratory, sanctuary]

# Banner Display
print("=" * 50)
print(f"{BOLD}       WELCOME TO THE FORGOTTEN CITADEL{RESET}")
print("=" * 50)

# Check for Save Game
player = None
if os.path.exists("savegame.json"):
    ans = input("Found a saved game! Do you want to continue? (y/n): ").strip().lower()
    if ans in ['y', 'yes']:
        player, _ = load_game(all_rooms, all_items)

# Player Registration
if not player:
    name = input("Enter your name: ").strip()
    if not name:
        name = "Arthur"
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print(f"{RED}❌ Invalid age input. Shutting down...{RESET}")
        sys.exit()

    if age < 12:
        print(f"{RED}You are a minor. Program shutting down...{RESET}")
        sys.exit()
    else:
        print(f"\nWelcome, {name}! You are {age} years old.")

    player = Player(name, location=hall)
    player.hp = 100



# 6. MAIN GAME LOOP


while True:
    print("\n" + "=" * 40)
    print(f"MAIN MENU | Location: {CYAN}{player.location.name}{RESET} | HP: {GREEN if player.hp > 40 else RED}{player.hp}{RESET}")
    print("=" * 40)
    print("1. play       - Read intro & story")
    print("2. score      - Show your score")
    print("3. move       - Move to another room")
    print("4. collect    - Collect item in current room")
    print("5. location   - Look around current room")
    print("6. inventory  - Show inventory")
    print("7. interact   - Interact with Guardian / Gate")
    print("8. help       - Display instructions")
    print("9. save       - Save game state")
    print("10. load      - Load game state")
    print("11. settings  - Open settings")
    print("12. lopeta    - Exit the program")
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

    elif command in ["interact", "7"]:
        interact_with_guardian(player)
        
    elif command in ["help", "8"]:
        display_help()

    elif command in ["save", "9"]:
        save_game(player)

    elif command in ["load", "10"]:
        loaded_p, _ = load_game(all_rooms, all_items)
        if loaded_p:
            player = loaded_p
        
    elif command in ["settings", "11"]:
        open_settings()
        
    elif command in ["lopeta", "12"]:
        print(f"\n{CYAN}👋 Goodbye! Thanks for playing!{RESET}")
        break
        
    else:
        print(f"\n{RED}❌ Unknown command! Please try again.{RESET}")