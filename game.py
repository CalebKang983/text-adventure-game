import random


class Room:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def give_symbol(self):
        return self.symbol

    def __str__(self):
        return self.symbol

def generate_map(rows,cols):
    map = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            map[i][j] = Room("Empty","_")

    for i in range(rows):
         for j in range(cols):
            n = random.randint(1, 100)
            if n<=32:
                m = random.randint(1,4)
                if m == 1:
                    map[i][j] = Room("Physics classroom","P")
                elif m == 2:
                    map[i][j] = Room("Library","L")
                elif m == 3:
                    map[i][j] = Room("Bathroom","B")
                else:
                    map[i][j] = Room("Chemistry classroom","C")
            elif n >= 81:
                map[i][j] = Room("Warehouse","W")

    exit_location(map,rows, cols)
    return map

def print_map(game_map, player, if_block):
    if not if_block:
        for i, row in enumerate(game_map):
            for j, room in enumerate(row):
                if i == player.x and j == player.y:
                    print("*", end=" ")
                else:
                    print(room, end=" ")
            print()
    else:
        for i, row in enumerate(game_map):
            for j, room in enumerate(row):
                symbol = block_sight(room, player.x, player.y, i, j)
                print(symbol, end=" ")
            print()

ROOM_TYPES = [
    Room("Physics classroom","P"),
    Room("Library","L"),
    Room("Bathroom","B"),
    Room("Chemistry classroom","C"),
    Room("Empty","_"),
    Room("Warehouse","W"),
    Room("Exit","E")
]

def physics_classrooom(player):
    print("You are in the Physics classroom!")
    if player.has_key:
        choice = str(input("Are you going to use your key?(Y/N)"))
        if choice == "Y":
            print("You gain invincibility for one round!")
            player.invincible = True
            player.has_key = False
    else:
        print("The door is locked!")

def Library(player,game_map):
    print("You are in the Library!")
    if player.has_key:
        choice = str(input("Are you going to use your key?(Y/N)"))
        if choice == "Y":
            print("You found hints from a book!")
            hint(game_map)
    else:
        print("The door is locked!")

def hint(game_map):
    danger_num = []
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[i][j].name == "Chemistry classroom" or game_map[i][j].name == "Bathroom":
                danger_num.append((i+1, j+1))
    if len(danger_num) >= 2:
        selected = random.sample(danger_num, 2)
        print(f"Be careful! Dangerous rooms spotted at: (row,column){selected[0]} and {selected[1]}")
    elif len(danger_num) == 1:
        print(f"Be careful! One dangerous room spotted at: (row,column){danger_num[0]}")
    else:
        print("No dangerous rooms found!")

def bathroom(player):
    print("You are in a bathroom!")
    if player.has_bomb:
        choice = str(input("Are you going to use the bomb?(Y/N)"))
        if choice == "Yes":
            print("You destroyed the bathroom!")
    elif player.invincible:
        print("Your shield completed its mission")
        player.invincible = False
    else:
        print("You are sucked into the toilet! YOU ARE DIED!")

def Chemistry_classroom(player,rows,cols):
    print("You are in a Chemistry classroom!")
    if player.has_bomb:
        choice = str(input("Are you going to use the bomb?(Y/N)"))
        if choice == "Yes":
            print("You destroyed the Chemistry classroom!")
    elif player.invincible:
        print("Your shield completed its mission.")
        player.invincible = False
    else:
        print("You touched a unknown test tube! You are teleported!")
        teleport(player, rows,cols)

def teleport(player, rows,cols):
    r = random.randint(1, rows -1)
    c = random.randint(1, cols -1)
    player.x = r
    player.y = c

def Warehouse(player):
    print("You are in the Warehouse!")
    choice = str(input("Make your choice! Key or Bomb?(K/B)"))
    if choice != "K" and choice != "B":
        print("Undefined selection! Do it again!")
        Warehouse(player)
    elif choice == "K":
        player.has_key = True
        print("You picked up a key!")
    else:
        player.has_bomb = True
        print("You picked up a bomb!")

def Empty():
    print("Continue your journey!")

# def Exit():
#     print("Congratulations! You escaped from MUDD!")


def exit_location(game_map,rows,cols):
    n = random.randint(1,2)
    if n == 1:
        m = random.randint(0,rows - 1)
        game_map[m][cols-1] = Room("Exit","E")
    else:
        m = random.randint(0,cols-1)
        game_map[rows-1][m] = Room("Exit","E")

def block_sight(room, player_x, player_y, room_x, room_y):
    if room_x == player_x and room_y == player_y:
        return "*"
    elif room.symbol == "_":
        return "_"
    elif room.symbol == "E":
        return "E"
    elif room.symbol == "W":
        return "W"
    else:
        return "?"


class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.has_key = False
        self.has_bomb = False
        self.invincible = False

    def move(self, direction, game_map):
        dx, dy = 0, 0
        if direction == "w": dx = -1
        elif direction == "s": dx = 1
        elif direction == "a": dy = -1
        elif direction == "d": dy = 1

        new_x = self.x + dx
        new_y = self.y + dy

        if not (0 <= new_x < len(game_map)) or not (0 <= new_y < len(game_map[0])):
            print("Don't try to leave by penetrating the wall!")
        else:
            self.x = new_x
            self.y = new_y


def main():
    rows = int(input("Enter expected map size(rows):"))
    cols = int(input("Enter expected map size(cols):"))
    ifblock = str(input("Do you want to block your sight?(Y/N)"))
    if ifblock == "Y":
        if_block = True
    else:
        if_block = False

    game_map = generate_map(rows, cols)
    player = Player()

    print("Welcome to MUDD! Your mission is to ESCAPE!")
    print("The followings are the types of the rooms:")
    print("P is physics classroom.\nL is library.\nW is warehouse.\nB is bathroom.\nC is chemistry classroom.\nE is exit!")
    print("Don't forget: '*' is where you are!")
    print("HINT: Bathroom is somewhat dangerous!")
    print("Enjoy you journey!")

    while True:
        print_map(game_map, player, if_block)
        movement = input("Direction (w/a/s/d/quit): ")
        if movement == "quit":
            print("Game over")
            break
        elif movement in ["w", "a", "s", "d"]:
            player.move(movement, game_map)
        else:
            print("Undefined!")

        room = game_map[player.x][player.y]
        if room.name == "Physics classroom":
            physics_classrooom(player)
        elif room.name == "Library":
            Library(player,game_map)
        elif room.name == "Bathroom":
            bathroom(player)
        elif room.name == "Chemistry classroom":
            Chemistry_classroom(player, rows, cols)
        elif room.name == "Warehouse":
            Warehouse(player)
        elif room.name == "Exit":
            print("Congratulations! You escaped from MUDD!")
            break
        else:
            Empty()

main()
