import os
import time
import random

game_start_time = 0
player_max_hp = 100

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_title():
    print(r"""
            )           (              (                   )       (        )   
  *   )  ( /(           )\ )    (      )\ )  *   )      ( /(       )\ )  ( /(   
` )  /(  )\()) (       (()/(    )\    (()/(` )  /(      )\()) (   (()/(  )\())  
 ( )(_))((_)\  )\       /(_))((((_)(   /(_))( )(_))    ((_)\  )\   /(_))((_)\   
(_(_())  _((_)((_)     (_))   )\ _ )\ (_)) (_(_())      _((_)((_) (_))    ((_)  
|_   _| | || || __|    | |    (_)_\(_)/ __||_   _|     | || || __|| _ \  / _ \  
  | |   | __ || _|     | |__   / _ \  \__ \  | |       | __ || _| |   / | (_) | 
  |_|   |_||_||___|    |____| /_/ \_\ |___/  |_|       |_||_||___||_|_\  \___/  
    """)

map1 = [
    list("#############################"),
    list("#P....I....##.......F......E#"),
    list("###.#####.####.#####.#####.##"),
    list("#..........I................#"),
    list("#.#####.######.#####.#####..#"),
    list("#......F....................#"),
    list("#.#####.#####.#####.#####...#"),
    list("#...........................#"),
    list("#############################"),
]
        
map2 = [
    list("#############################"),
    list("#P.......##.....I.....F....E#"),
    list("#####.#########.######.######"),
    list("#..........I................#"),
    list("#.#####.#####.#####.#######.#"),
    list("#..............F............#"),
    list("#.#####.#####.#####.#######.#"),
    list("#..................I........#"),
    list("#############################"),
]
        
map3 = [
    list("#############################"),
    list("#P.............##..........E#"),
    list("######..######.#######..#####"),
    list("#....I......................#"),
    list("#..#####.#####.#####.#####..#"),
    list("#...............F...........#"),
    list("#..#####.#####.#####.#####..#"),
    list("#..............I....F.......#"),
    list("#############################"),
]
        
map4 = [
    list("#############################"),
    list("#P.........I...............E#"),
    list("####..######.######.#####..##"),
    list("#.............F.............#"),
    list("#..#####.#####.#####.#####..#"),
    list("#.................I.........#"),
    list("#..#####.#####.#####.#####..#"),
    list("#...........................#"),
    list("#############################"),
]
        
map5 = [
    list("#############################"),
    list("#P............I......F.....E#"),
    list("#####..#####.######.#####..##"),
    list("#...........................#"),
    list("#..#####.#####.#####.#####..#"),
    list("#............I..............#"),
    list("#..#####.#####.#####.#####..#"),
    list("#...............F...........#"),
    list("#############################"),
]
        
maps = [map1, map2, map3, map4, map5]

def clone_maps():
    return [[row[:] for row in game_map] for game_map in maps]

current_map_index = 0
current_map = maps[current_map_index]

def find_player_start(game_map):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == "P":
                return x, y

def draw_map(game_map):
    clear()
    show_title()
    print("=" * 80)
    print(f"Hero: {hero}")
    print("Saved Friends:")
    if saved_friends:
        for friend in saved_friends:
            print(f"- {friend}")
    else:
        print("- None")
    
    print("=" * 80)

    for row in game_map:
        print(" ".join(row))
    
    print("=" * 80)
    
    print("Inventory:")
    for item, count in inventory.items():
        print(f"- {item}: {count}")

    print("=" * 80)

    print("WASD to move")

def has_remaining_friends(game_map):
    for row in game_map:
        if "F" in row:
            return True
    return False

def move_player(dx, dy):
    global player_x, player_y, current_map, current_map_index, game_maps

    new_x = player_x + dx
    new_y = player_y + dy

    target_tile = current_map[new_y][new_x]

    if target_tile == "#":
        return

    if target_tile == "E":
        if has_remaining_friends(current_map):
            clear()
            show_title()
            print("=" * 80)
            print("The exit is sealed.")
            print("You can feel the curse still lingering in this forest.")
            print("Save all possessed friends before leaving.")
            print("=" * 80)
            input("Press Enter to continue...")
            return
        else:
            clear()
            show_title()
            print("=" * 80)
            print("The path ahead opens.")
            print("You may proceed to the next area.")
            print("=" * 80)
            input("Press Enter to continue...")

            if current_map_index == len(maps) - 1:
                if len(saved_friends) == len(friends_to_save):
                    final_narration(hero)
                    player_hp = player_max_hp
                    result = bowser_battle(hero)
                    if result == "GAME_FINISHED":
                        return "GAME_FINISHED"
                else:
                    clear()
                    show_title()
                    print("=" * 80)
                    print("A strange force prevents you from moving forward.")
                    print("Someone is still trapped within the forest.")
                    print("=" * 80)
                    input("Press Enter to continue...")
                return

            current_map_index += 1
            current_map = game_maps[current_map_index]
            player_x, player_y = find_player_start(current_map)
            return

    if target_tile == "I":
        item = get_random_item()
        inventory[item] += 1

        clear()
        show_title()
        print("=" * 80)
        print(f"You found: {item}")
        print("It has been added to your inventory.")
        print("=" * 80)
        input("Press Enter to continue...")

        current_map[new_y][new_x] = "."

    if target_tile == "F":
        fight = encounter_friend()
        if fight:
            current_map[new_y][new_x] = "."
        else:
            return

    current_map[player_y][player_x] = "."
    player_x, player_y = new_x, new_y
    current_map[player_y][player_x] = "P"

def use_item():
    global inventory
    
    clear()
    show_title()
    print("=" * 80)
    print("Choose an item to use:\n")

    usable_items = [item for item, count in inventory.items() if count > 0]

    if not usable_items:
        print("You have no items.")
        input("\nPress Enter to continue...")
        return None

    for i, item in enumerate(usable_items, 1):
        print(f"{i}. {item} (x{inventory[item]})")

    print("=" * 80)

    choice = input("Enter number: ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(usable_items):
        print("Invalid choice.")
        input("Press Enter...")
        return None

    item = usable_items[int(choice) - 1]
    inventory[item] -= 1

    if item == "Healing Potion":
        return "heal"
    elif item == "Power Surge":
        return 2
    elif item == "Guardian Barrier":
        return "shield"
    elif item == "Fate Talisman":
        return "luck"

    input("\nPress Enter to continue...")
    return 0

def show_bowser_art():
    print(r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠲⣄⢀⡀⠀⠀⠀⠀⠀⠀⢀⠄⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠈⠳⣕⢄⠀⠀⠀⠀⢠⣏⠀⠀⣹⡆⠀⠀⠀⠀⠀⠀⣀⡀⣀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⡿⡷⣄⣤⣾⣿⣯⣿⣿⣿⣧⡀⠀⠀⢀⠀⠀⠈⣻⣿⣻⢿⣶⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⠀⡖⣯⢳⣿⣿⣿⡟⠛⡞⣿⣽⣿⣿⣧⣼⠃⢸⣧⣷⣿⡟⣷⣯⡟⣾⢻⡞⣿⡆⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠠⠤⣀⡀⠀⠀⠀⠀⣀⣼⣧⠽⠒⠋⠉⠉⠉⠉⠉⠙⠓⠿⠿⠛⠋⠉⣄⠀⢻⣿⣿⡿⣽⣳⢯⡿⣽⢯⡿⣽⣷⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠱⡀⠀⠈⠉⢓⢾⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⡄⠀⠐⢹⣿⡷⣯⢿⡽⣯⢿⡽⣷⣿⠀⢀⣤⣷⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⢦⠀⣠⢯⡿⠋⠀⠀⠀⠀⢀⣀⠀⠀⢀⣠⣆⣴⡄⣀⠀⢄⠂⠄⡷⠻⣦⣤⣾⣿⣽⣯⡿⣽⢿⣾⡉⢏⡿⣿⣿⣻⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣵⠟⠀⢀⡠⠔⠚⠉⣡⡈⠉⠉⠛⠻⣿⣿⣿⣷⣮⣦⣴⣾⣷⣿⠿⠿⠾⣌⣛⡟⠉⣻⣯⣿⣧⠨⣽⣿⣞⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⡔⠁⠀⠀⠀⣀⢴⣹⠶⢳⣀⠀⢻⣿⣛⡹⠿⠿⣿⣭⠝⠀⠀⠀⠀⠈⠹⣷⣤⣿⣈⣽⣻⠵⠿⠿⣭⣿⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣼⡟⠀⣸⠀⠀⠀⠀⣦⣾⣿⣿⣿⣿⡿⠟⠚⠋⢄⡀⠀⢰⠋⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠈⠀⠀⠐⠋⣟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢄⡀⠀⠀⠀⠈⡷⡿⠀⠀⡇⠀⠀⢠⣮⣁⣽⣿⣿⠟⠋⠁⠀⠀⢀⠞⠻⣦⢾⣦⡾⠁⠀⢠⢶⣷⡀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⣠⡾⣼⡟⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠉⠲⢤⣠⡴⣹⠃⠀⠀⣧⠀⢠⣾⣿⣿⣿⠏⠀⠀⠀⠱⣽⠞⢻⠦⡤⢿⣌⢿⣿⣤⠀⠈⣿⠿⣷⡄⣀⠀⠀⠀⣠⠹⣄⣠⠾⢋⡴⢇⢣⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⢷⡟⠀⠀⠀⣿⢤⠘⣿⣿⣿⡏⠀⢠⡀⠀⠀⣸⣷⢪⠝⣰⢃⡞⢮⣿⣿⡄⠀⢹⣶⣿⣿⣶⡴⢶⣿⣲⣯⣿⣿⡏⡙⣬⠼⠋⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠁⠀⠀⣸⠇⢸⣿⠏⣿⣿⡁⠀⠀⢿⣆⡾⠀⣿⣇⠹⣆⢏⡸⢆⡈⣹⣷⡀⢸⠏⢸⣿⣿⣷⣿⣿⣿⣿⣿⣾⣇⣾⢀⣶⣆⣀⣀⣀⣰⠶⡿⢱⠎⣀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⠀⠀⢀⡏⢀⣿⣽⠲⢾⣿⡇⠀⠠⢜⢢⠟⣦⡼⢧⢋⡖⢎⡱⠮⢵⡏⡹⡇⠀⠑⣿⡿⠛⣿⣿⣿⣿⡿⣭⣟⣹⣿⣿⣾⣿⡟⢏⡱⢌⢣⡱⢣⣫⢖⢧⣋⠖⠄
⠀⠀⠀⠀⢠⠀⠀⠀⡘⠁⣼⡿⠁⠀⠀⠉⠛⠦⣵⣎⣦⠕⢊⣀⣊⣜⠸⣏⡛⡛⠞⡹⠳⣷⠀⠀⠀⠁⠀⠋⠉⠉⠉⠀⠻⣧⣿⣿⣿⣿⢣⡙⣌⠲⣩⢲⡱⣣⠏⣎⣓⡬⠆⠀
⠀⠀⠀⠀⠎⠀⠀⠠⠁⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⢢⡔⡿⠀⠑⠨⠙⠶⣥⣆⣑⠌⢣⡀⠀⠀⠀⢀⠀⣀⠂⣄⡾⢩⣿⣹⣻⣿⠋⠛⠛⠶⣇⢇⡚⡥⢞⡭⣚⠼⣱⡀
⠀⠀⠀⠀⣽⠀⠀⠄⢐⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⣌⠳⣼⡅⠈⡲⢦⣉⠒⡰⢈⠉⡉⢉⣽⡷⣶⣟⡛⠻⢤⡃⠊⡤⣞⣿⣿⣿⣿⣆⠀⠀⣠⠞⢾⡴⡙⡮⠆⠉⢚⠀⠃
⠀⠀⠀⠀⣯⠽⠖⠖⢻⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢌⠻⣜⢛⢦⡁⢆⡉⡙⠁⠂⠀⣴⡞⢯⡜⢧⡹⣛⣦⡀⠉⠓⠛⠶⠾⣿⣿⣿⣿⣷⣦⣽⣦⣤⠷⠋⠁⠀⠀⠀⠀⠀
⢀⣠⠴⠚⠁⢠⠠⡀⠼⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢌⢣⡝⡌⠦⡉⢆⡐⠄⠁⣴⣞⠳⣜⢣⠞⣥⠳⣍⠞⣵⡀⠀⠀⠀⠀⠀⠉⠙⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⠻⢦⣱⣌⢢⡑⣌⠲⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⡜⡲⠜⢨⠓⠈⢄⣠⣴⢛⢧⠪⡝⣌⢧⣋⠶⡹⢌⡻⢼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠉⠉⠉⢉⡇⠀⠀⠀⠀⠀⠀⠀⠀⡀⢢⠑⡬⢱⢩⠟⠙⠛⠛⠒⣳⢏⠶⣙⠼⣘⠦⣍⢮⡱⣍⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⠀⠀⠄⢢⢅⢣⠚⡔⢣⠏⠀⠀⠀⠀⠀⣟⢎⡳⣉⠮⢥⢫⠴⣢⢓⢾⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⢀⠇⡸⢃⠼⡘⠟⣸⠟⠀⠀⠀⠀⠀⢸⣛⡜⢣⡛⡼⣃⢟⡼⣣⢟⡻⢼⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⠃⠀⠀⠀⠀⠠⠨⣐⢪⢑⡋⣎⣱⠽⠃⠀⠀⠀⠀⠀⠀⣿⢄⡏⢧⡙⢶⠩⡞⢴⢣⠎⣽⡷⣿⣻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⣏⠉⣻⣆⠀⠀⠀⠀⠀⠀⠀⠈⠚⠾⠧⠾⠥⠿⠼⠾⠾⠽⠾⠓⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠦⣀⠀⢀⡤⠒⢦⣠⠖⠚⣟⡎⠙⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠒⠤⠞⠻⠦⢄⡟⠋⠒⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)


def encounter_friend():
    global player_hp, saved_friends, retries
    lucky_strike = False

    clear()
    show_title()
    print("=" * 80)
    print("You encounter a possessed friend.")
    print("Their presence radiates hostile energy.")
    print("=" * 80)

    while True:
        clear()
        show_title()
        print("=" * 80)
        print("You encounter a possessed friend.")
        print("Their presence radiates hostile energy.")
        print("=" * 80)
        choice = input("1. Fight\n2. Retreat\nEnter: ")
        
        if choice == "1":
            break
        
        elif choice == "2":
            print("\nYou step back, gathering your strength.")
            input("Press Enter to continue...")
            return False
        
        else:
            print("\nInvalid choice.")
            print("Please choose 1 to Fight or 2 to Retreat.")
            input("Press Enter...")
            continue

    enemy_hp = random.randint(80, 120)

    enemy = {
        "hp": enemy_hp,
        "attack_min": 10,
        "attack_max": 15
    }

    shield = 0
    damage_multiplier = 1
    heal_retries = 5

    while True:
        clear()
        show_title()
        print("=" * 80)
        print("Battle Begins!\n")
        print(f"Hero: {hero}\n")
        print(f"Your HP: {player_hp}/{player_max_hp}")
        print(f"Shield: {shield}")
        print(f"Heal in a row: {heal_retries}/5")
        print(f"Possessed friend HP: {enemy['hp']}")
        print("=" * 80)

        print("1. Attack")
        print("2. Heal")
        print("3. Use Item")

        action = input("\nChoose action: ")

        if action == "1":
            if lucky_strike:
                base_dmg = 25
                lucky_strike = False
            else:
                base_dmg = random.randint(15, 25)
            dmg = int(base_dmg * damage_multiplier)
            enemy["hp"] -= dmg
            damage_multiplier = 1
            heal_retries = 5
            print(f"\nYou dealt {dmg} damage!")

        elif action == "2":
            if heal_retries <= 0:
                print("You can only heal yourself 5 times in a row. You attacked instead.")
                if lucky_strike:
                    base_dmg = 25
                    lucky_strike = False
                else:
                    base_dmg = random.randint(15, 25)
                dmg = int(base_dmg * damage_multiplier)
                enemy["hp"] -= dmg
                damage_multiplier = 1
                heal_retries = 5
                print(f"\nYou dealt {dmg} damage!")
            else:
                heal = random.randint(15, 25)
                player_hp += heal
                heal_retries -= 1
                player_hp = min(player_hp, player_max_hp)
                print(f"\nYou healed {heal} HP!")

        elif action == "3":
            heal_retries = 5
            result = use_item()
            
            if result is None:
                continue
            if result == "heal":
                heal = player_max_hp // 2
                player_hp += heal
                player_hp = min(player_hp, player_max_hp)
                print(f"\nYou healed {heal} HP!")
            elif result == 2:
                damage_multiplier = 2
                print("\nYour next attack will deal double damage!")
            elif result == "shield":
                shield += 50
                print("\nA barrier absorbs the next 50 damage!")
            elif result == "luck":
                lucky_strike = True
                print("\nYour next attack will deal max damage!")
            
            input("\nPress Enter to continue...")


        else:
            print("\nInvalid action.")
            input("Press Enter...")
            continue

        if enemy["hp"] <= 0:
            clear()
            show_title()
            print("=" * 80)
            print("The curse shatters!")
            remaining = [f for f in friends_to_save if f not in saved_friends]
            friend = random.choice(remaining)
            saved_friends.append(friend)
            print(f"{friend} has been freed from the curse!")
            print("=" * 80)

            reward_count = random.randint(1, 2)
            for _ in range(reward_count):
                item = get_random_item()
                inventory[item] += 1
                print(f"You received: {item}")

            input("\nPress Enter to continue...")
            return True

        enemy_dmg = random.randint(enemy["attack_min"], enemy["attack_max"])
        original_dmg = enemy_dmg

        if shield > 0:
            absorbed = min(shield, enemy_dmg)
            shield -= absorbed
            enemy_dmg -= absorbed

        player_hp -= enemy_dmg
        player_hp = min(player_hp, player_max_hp)
        print(f"\nThe enemy dealt {original_dmg} damage!")
        input("Press Enter...")

        if player_hp <= 0:
            while True:
                clear()
                show_title()
                print("=" * 80)
                print("You were defeated.")
                print("The curse overwhelms you.")
                print("=" * 80)

                retry = input("1. Try Again\n2. Rest\nEnter: ").strip()
                
                if retry == "1":
                    retries += 1
                    player_hp = player_max_hp
                    enemy = {
                        "hp": enemy_hp,
                        "attack_min": 15,
                        "attack_max": 25
                        }
                    shield = 0
                    damage_multiplier = 1
                    break
                
                elif retry == "2":
                    retries += 1
                    player_hp = player_max_hp
                    return False
                
                else:
                    print("Invalid choice. Please enter 1 or 2.")
                    input("Press Enter...")
                    continue
            
def bowser_battle(hero):
    global player_hp, retries

    player_hp = player_max_hp
    ALLY_HEAL_PER_TURN = 10
    lucky_strike = False
    BASE_MULTIPLIER = 1.5
    damage_multiplier = BASE_MULTIPLIER
    shield = 100

    bowser = {
        "hp": 1000,
        "attack_min": 20,
        "attack_max": 40,
        "heal_min": 20,
        "heal_max": 40
    }

    clear()
    show_title()
    print("=" * 80)
    print("FINAL BATTLE")
    print("Bowser emerges from the shadows.")
    print("=" * 80)
    input("Press Enter to begin the battle...")

    while bowser["hp"] > 0 and player_hp > 0:
        clear()
        show_title()
        print("=" * 80)
        print("BOWSER – FINAL BATTLE\n")
        show_bowser_art()
        print(f"Hero: {hero}")
        print(f"Your HP: {player_hp}/{player_max_hp}")
        print(f"Shield: {shield}")
        print(f"Bowser HP: {bowser['hp']}")
        print("=" * 80)

        print("1. Attack")
        print("2. Heal")
        print("3. Use Item")

        choice = input("\nChoose action: ").strip()

        if choice == "1":
            if lucky_strike:
                base_dmg = 35
                lucky_strike = False
            else:
                base_dmg = random.randint(20, 35)

            dmg = int(base_dmg * damage_multiplier)
            bowser["hp"] -= dmg
            damage_multiplier = BASE_MULTIPLIER
            print(f"\nYou strike Bowser for {dmg} damage!")

        elif choice == "2":
            heal = random.randint(20, 35)
            player_hp += heal
            player_hp = min(player_hp, player_max_hp)
            print(f"\nYou recover {heal} HP!")

        elif choice == "3":
            result = use_item()
            
            if result is None:
                continue
            
            if result == "heal":
                heal = player_max_hp // 2
                player_hp += heal
                player_hp = min(player_hp, player_max_hp)
                print(f"\nYou healed {heal} HP!")
                
            elif result == 2:
                damage_multiplier += 2
                print("\nYour next attack will deal double damage!")
                
            elif result == "shield":
                shield += 50
                print("\nA barrier absorbs the next 50 damage!")
            
            elif result == "luck":
                lucky_strike = True
                print("\nYour next attack will deal max damage!")
            
            input("\nPress Enter to continue...")


        else:
            print("\nInvalid action.")
            input("Press Enter...")
            continue

        player_hp += ALLY_HEAL_PER_TURN
        player_hp = min(player_hp, player_max_hp)
        print(f"Your friends helped you gain {ALLY_HEAL_PER_TURN} HP!")

        if bowser["hp"] <= 0:
            break

        action = random.choice(["attack", "heal"])
        
        if action == "heal" and bowser["hp"] < 800:
            heal = random.randint(bowser["heal_min"], bowser["heal_max"])
            bowser["hp"] = min(bowser["hp"] + heal, 1000)
            print(f"Bowser regenerates {heal} HP!")
            
        else:
            dmg = random.randint(bowser["attack_min"], bowser["attack_max"])
            original_dmg = dmg
            
            if shield > 0:
                absorbed = min(shield, dmg)
                shield -= absorbed
                dmg -= absorbed
                
            player_hp -= dmg
            print(f"Bowser attacks for {original_dmg} damage!")

        player_hp = min(player_hp, player_max_hp)

        if player_hp <= 0:
            while True:
                clear()
                show_title()
                print("=" * 80)
                print("You fall to the ground, exhausted.")
                print("=" * 80)

                retry = input("1. Try Again\n2. Give Up\nEnter: ").strip()

                if retry == "1":
                    retries += 1
                    player_hp = player_max_hp
                    shield = 100
                    bowser["hp"] = 1000
                    break
                elif retry == "2":
                    defeat_narration(hero)
                    show_ending_screen(hero, player_hp, retries)
                    return "GAME_FINISHED"
                else:
                    print("Invalid choice.")
                    input("Press Enter...")
                    continue

        input("\nPress Enter to continue...")

    clear()
    show_title()
    print("=" * 80)
    print("Bowser roars one final time.")
    print("The curse shatters completely.")
    print("You are victorious.")
    print("=" * 80)

    ending_narration(hero)
    show_ending_screen(hero, player_hp, retries)
    return "GAME_FINISHED"
            
def get_random_item():
    items = [
        "Healing Potion",
        "Power Surge",
        "Guardian Barrier",
        "Fate Talisman"
    ]
    return random.choice(items)

def ending_narration(hero):
    clear()
    show_title()
    print("=" * 80)

    narration = [
        "Silence falls across the forest.",
        "",
        "Bowser lets out a final roar, his strength finally exhausted.",
        "The dark power that once twisted the land begins to crumble.",
        "",
        "Light breaks through the trees.",
        "The forest breathes once more.",
        "",
        f"{hero} stands firm, battered but unbroken.",
        "Around them, familiar figures begin to move.",
        "",
        "One by one, the friends once lost to darkness awaken.",
        "Their eyes clear.",
        "Their strength restored.",
        "",
        "Together, they had endured.",
        "Together, they had overcome.",
        "",
        "The curse is no more.",
        "The journey has ended.",
        "",
        "But the legend of this battle will be remembered."
    ]

    for line in narration:
        print(line)
        time.sleep(0.7)

    print("=" * 80)
    input("Press Enter to continue...")

def defeat_narration(hero):
    clear()
    show_title()
    print("=" * 80)

    narration = [
        "The final blow lands.",
        "",
        "Your strength fails, and the ground rushes toward you.",
        "The world grows distant as the echoes of battle fade.",
        "",
        "Bowser stands tall amid the ruins of the forest.",
        "His victory is absolute.",
        "",
        f"{hero} lies defeated, unable to rise once more.",
        "The courage that carried you this far is no longer enough.",
        "",
        "Around you, the forest falls silent.",
        "The light that once returned now fades again.",
        "",
        "Your friends rush to your side,",
        "but even together, they know the truth.",
        "",
        "This battle cannot be won today.",
        "",
        "Bowser’s power tightens its grip on the land.",
        "The paths close.",
        "Hope retreats into legend.",
        "",
        "Though your journey ends here,",
        "the story of your struggle will not be forgotten.",
        "",
        "For even in defeat,",
        "a hero’s stand still echoes through time."
    ]

    for line in narration:
        print(line)
        time.sleep(0.7)

    print("=" * 80)
    input("Press Enter to view your final results...")

def get_play_time():
    return int(time.time() - game_start_time)

def calculate_grade(player_hp, retries):
    hp_score = int((player_hp / player_max_hp) * 40)
    hp_score = max(0, min(40, hp_score))

    play_time = get_play_time()

    if play_time <= 600:
        time_score = 40
    elif play_time <= 900:
        time_score = 30
    elif play_time <= 1200:
        time_score = 20
    elif play_time <= 1500:
        time_score = 10
    else:
        time_score = 5

    retry_score = max(0, 20 - (retries * 3))

    score = hp_score + time_score + retry_score
    score = max(0, min(80, score))

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return score, grade

def show_ending_screen(hero, player_hp, retries):
    clear()
    show_title()
    print("=" * 80)

    score, grade = calculate_grade(player_hp, retries)
    play_time = get_play_time()
    formatted_time = format_time(play_time)

    print("THE END\n")
    print(f"Hero: {hero}")
    print(f"Final HP: {player_hp}")
    print(f"Retries: {retries}")
    print(f"Time Played: {formatted_time}")
    print(f"Score: {score}")
    print(f"Grade: {grade}")

    print("=" * 80)
    input("Press Enter to return to the main menu...")

def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def play_narration():
    clear()
    show_title()
    print("=" * 80)

    narration = [
        "Long ago, the land existed in harmony.",
        "",
        "Forests flourished beneath open skies, and travelers walked without fear.",
        "Ten close friends journeyed together, bound not only by friendship,",
        "but by trust forged through countless shared adventures.",
        "",
        "Their path led them deep into an ancient forest,",
        "a place spoken of in legends and half-forgotten warnings.",
        "",
        "Without warning, the light dimmed.",
        "The wind ceased.",
        "The forest itself seemed to hold its breath.",
        "",
        "From the shadows emerged Bowser.",
        "",
        "With overwhelming force, he cast a powerful curse across the land.",
        "Dark energy surged through the forest, bending paths and sealing exits.",
        "",
        "One by one, the friends were bound by the spell.",
        "Their wills clouded.",
        "Their movements no longer their own.",
        "",
        "The forest transformed into a living prison.",
        "Every familiar trail vanished.",
        "Hope itself seemed to fade.",
        "",
        "Yet fate was not finished."
    ]

    for line in narration:
        print(line)
        time.sleep(0.5)

    print("=" * 80)
    input("Press Enter to choose the hero who escaped...")

def choose_character():
    heroes = [
        "Mario",
        "Luigi",
        "Princess Peach",
        "Toad",
        "Princess Daisy",
        "Yoshi",
        "Rosalina",
        "Pauline",
        "Toadette",
        "Donkey Kong"
    ]

    while True:
        clear()
        show_title()
        print("=" * 80)
        print("Choose the hero who escaped the curse:\n")

        for i, hero in enumerate(heroes, 1):
            print(f"{i}. {hero}")

        print("=" * 80)

        choice = input("Enter number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(heroes):
            return heroes[int(choice) - 1]

        else:
            print("\nInvalid choice. Please enter a valid number.")
            input("Press Enter to try again...")

def escape_narration(hero):
    clear()
    show_title()
    print("=" * 80)

    narration = [
        f"When the curse spread through the forest, {hero} felt its presence closing in.",
        "",
        "The air grew heavy, pressing against every breath.",
        "Shadows stretched across the ground, binding all who stood within reach.",
        "",
        f"{hero} moved through the forest as the land itself began to change.",
        "Paths twisted without warning.",
        "Roots rose from the earth, and familiar trails vanished.",
        "",
        "Cries echoed through the trees — voices once filled with laughter,",
        "now distant and hollow, lost to the power of the spell.",
        "",
        f"In that moment, {hero} resisted.",
        "Not through strength alone, but through unwavering resolve.",
        "",
        "A narrow path revealed itself, unseen by the curse.",
        "It was brief.",
        "It was dangerous.",
        "But it was enough.",
        "",
        f"{hero} ran as the forest sealed itself behind them.",
        "The darkness could not follow.",
        "",
        f"Standing alone at the forest’s edge, {hero} understood the truth.",
        "There would be no turning back.",
        "",
        "To save the others, the curse must be broken.",
        "One friend at a time.",
        "",
        f"And so, {hero} stepped forward, ready to face the shadowed forest."
    ]

    for line in narration:
        print(line)
        time.sleep(0.5)

    print("=" * 80)
    input("Press Enter to begin your journey...")

def final_narration(hero):
    clear()
    show_title()
    print("=" * 80)

    narration = [
        "The forest grows silent.",
        "",
        "The shadows that once twisted the paths now retreat,",
        "their hold weakened with every friend freed from the curse.",
        "",
        f"{hero} stands at the heart of the forest, no longer alone.",
        "One by one, familiar voices answer the call.",
        "",
        "Those once bound by darkness now stand together again.",
        "Their strength is no longer scattered — it is focused.",
        "",
        "Together, they empower their hero.",
        "",
        "From this moment on, their support is constant.",
        "At the end of every battle round,",
        "the hero is restored by 10 HP through their combined strength.",
        "",
        "Their resolve sharpens every strike.",
        "Each attack now carries a permanent 1.5× damage multiplier,",
        "turning every blow into a force driven by unity.",
        "",
        "Healing is no longer limited.",
        "The hero may recover health without restriction,",
        "as long as the battle continues.",
        "",
        "A powerful barrier forms around the hero.",
        "A shield with 80 durability surrounds them,",
        "ready to absorb incoming damage before harm can reach their body.",
        "",
        "Yet one presence remains.",
        "",
        "Bowser.",
        "",
        "The source of the curse still watches from beyond the forest.",
        "His power has not vanished — it has only withdrawn.",
        "",
        f"The friends gather close, placing their trust in {hero}.",
        "They know what must be done.",
        "",
        "This battle cannot be fought alone.",
        "",
        "With united resolve, they prepare for the final confrontation.",
        "",
        "The path ahead is clear.",
        "The final battle awaits."
    ]

    for line in narration:
        print(line)
        time.sleep(0.6)

    print("=" * 80)
    input("Press Enter to face the final battle...")

def help_screen():
    clear()
    show_title()
    print("=" * 80)

    print("HELP & GAME GUIDE\n")

    print("MOVEMENT CONTROLS:")
    print("  W - Move Up")
    print("  A - Move Left")
    print("  S - Move Down")
    print("  D - Move Right")
    print("  Q - Quit the game")
    print()

    print("MAP SYMBOLS:")
    print("  P - Player")
    print("  F - Possessed Friend")
    print("  I - Item")
    print("  E - Exit (locked until all friends are saved)")
    print("  # - Wall")
    print("  . - Open Path")
    print()

    print("BATTLE ACTIONS:")
    print("  1. Attack  - Deal damage to the enemy")
    print("  2. Heal    - Recover HP (You can only heal 5 times in a row)")
    print("  3. Use Item- Use items from your inventory")
    print()

    print("ITEMS:")
    print("  Healing Potion   - Restores 50 amount of HP")
    print("  Power Surge      - Boosts your next attack damage 2x")
    print("  Guardian Barrier - Absorbs incoming 50 damage")
    print("  Fate Talisman    - Guarantees a max damage strike")
    print()

    print("SCORING SYSTEM:")
    print("  - Higher final HP = higher score")
    print("  - Faster completion time = higher score")
    print("  - Fewer retries = higher score")
    print()

    print("GOAL:")
    print("  Save all possessed friends, then defeat Bowser.")
    print("  Strategy, timing, and resource management matter!")
    print()

    print("=" * 80)
    input("Press Enter to return to the main menu...")

def opening_screen():
    clear()
    show_title()
    print("=" * 80)
    print("1. Play")
    print("2. Help")
    print("3. Exit")
    print("=" * 80)
    return input("Enter: ")

while True:
    choice = opening_screen()

    if choice == "1":
        game_start_time = time.time()
        inventory = {
            "Healing Potion": 0,
            "Power Surge": 0,
            "Guardian Barrier": 0,
            "Fate Talisman": 0
            }
        game_maps = clone_maps()
        current_map_index = 0
        current_map = game_maps[current_map_index]
        player_x, player_y = find_player_start(current_map)
        player_hp = player_max_hp
        retries = 0

        play_narration()
        hero = choose_character()
        escape_narration(hero)
        
        characters = [
            "Mario",
            "Luigi",
            "Princess Peach",
            "Toad",
            "Princess Daisy",
            "Yoshi",
            "Rosalina",
            "Pauline",
            "Toadette",
            "Donkey Kong"
        ]
        
        saved_friends = []
        friends_to_save = [c for c in characters if c != hero]

        while True:
            draw_map(current_map)
            move = input("Move: ").lower()
            
            if move == "w":
                result = move_player(0, -1)
            elif move == "s":
                result = move_player(0, 1)
            elif move == "a":
                result = move_player(-1, 0)
            elif move == "d":
                result = move_player(1, 0)
            elif move == "q":
                break
                
            if result == "GAME_FINISHED":
                break

    elif choice == "2":
        help_screen()

    elif choice == "3":
        print("\nThank you for playing!\n")
        break

    else:
        print("\nInvalid choice. Please enter 1 to play the game, 2 to view tutorial and 3 to exit.")
        input("Press Enter...")
        continue
