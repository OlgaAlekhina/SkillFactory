from random import randint

class Game:

    def __init__(self):
        self.players = [Player(), Computer()]

        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

    def play(self):

        self.players[0].position_fleet()
        self.players[1].position_fleet()

        winner = False
        first_players_turn = True
        while not winner:
            if first_players_turn:
                winner = self.players[0].take_turn()
                if winner:
                    print("Игра окончена! Вы победили!")
            else:
                winner = self.players[1].take_turn()
                if winner:
                    print("Игра окончена! Компьютер победил!")

            first_players_turn = not first_players_turn

class Board:

    def __init__(self):
        self.grid = [[' O |']*6 for i in range(6)]
        self.hit_count = 0

    def __str__(self):
        str_val = "    1 | 2 | 3 | 4 | 5 | 6 |\n"
        for i in range(6):
            str_val += f"{i + 1} |"
            for j in range(6):
                str_val += self.grid[i][j]
            if i != 5:
                str_val += "\n"
        return str_val

    def get_public_view(self):
        str_val = "    1 | 2 | 3 | 4 | 5 | 6 |\n"
        for i in range(6):
            str_val += f"{i + 1} |"
            for j in range(6):
                if self.grid[i][j] == ' ■ |':
                    str_val += ' O |'
                else:
                    str_val += self.grid[i][j]
            if i != 5:
                str_val += "\n"
        return str_val

    def add_boat(self, boat):
        width = 1
        height = 1
        if boat.orientation == "v":
            height = boat.size
        else:
            width = boat.size
        if (boat.x < 0) or (boat.y < 0) or (boat.x+width > 6) or (boat.y+height > 6):
            return False

        for x in range(-1, width + 1):
                for y in range(-1, height + 1):
                    if boat.y + y >= 0 and boat.y + y < 6 and boat.x + x >=0 and boat.x + x <6 and self.grid[boat.y + y][boat.x + x] != ' O |':
                        return False

        for x in range(width):
            for y in range(height):
                self.grid[boat.y + y][boat.x + x] = " ■ |"
        return True

    def attack(self, x, y):
        current_value = self.grid[y][x]
        if current_value == ' ■ |':
            self.grid[y][x] = ' X |'
            self.hit_count += 1
            return True
        elif current_value == ' O |':
            self.grid[y][x] = ' T |'
            return False
        else:
            return False

    def is_repeated(self, x, y):
        if self.grid[y][x] != ' O |' and self.grid[y][x] != ' ■ |':
            return True

    def is_defeated(self):
        if self.hit_count == 11:
            return True
        else:
            return False

class Boat:
    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None
        self.hits = 0  

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation

    def is_drowned(self, x, y):
        if (self.orientation == 'v' and x == self.x and y >= self.y and y < self.y + self.size) or \
                (self.orientation == 'h' and y == self.y and x >= self.x and x < self.x + self.size):
             self.hits += 1
             if self.hits == self.size:
                 return True
        return False

class Player:
    def __init__(self):
        self.board = Board()
        self.fleet = [Boat("первый корабль", 3), Boat("второй корабль", 2), Boat("третий корабль", 2), Boat("четвертый корабль", 1), \
                      Boat("пятый корабль", 1), Boat("шестой корабль", 1), Boat("седьмой корабль", 1)]
        self.opponent = None

    def set_opponent(self, opponent):
        self.opponent = opponent

    def position_fleet(self):
        print("Давайте расположим ваши корабли на игровой доске.")

        for boat in self.fleet:
            self.position_boat(boat)

        print("Ваш флот готов к игре!")
        print("\n")

    def position_boat(self, boat):
        print(self.board)
        print("Вам нужно поставить", boat.label, ", состоящий из", boat.size, "палуб(ы) на игровую доску.")
        if boat.size == 1:
            orientation = "v"
        else:
            orientation = None
            while orientation is None:
                orientation = input("Выберите вертикальное или горизонтальное расположение: введите v или h. ")
                if (orientation != "v") and (orientation != "h"):
                    print("Вы должны ввести 'v' или 'h'. Попробуйте еще раз.")
                    orientation = None

        position = None
        while position is None:
            try:
                position = input("Введите координаты первой палубы корабля через запятую: сначала номер столбца, затем номер строки. ")
                coords = position.split(",")
                x = int(coords[0]) - 1
                y = int(coords[1]) - 1
                boat.set_orientation(orientation)
                boat.set_position(x,y)
                if not self.board.add_boat(boat):
                    raise Exception
            except ValueError:
                print("Вы ввели значения некорректно. Попробуйте еще раз.")
                position = None
            except:
                print("Вы должны выбрать положение, которое (1) находится в пределах доски, (2) находится как" + \
                      " минимум в 1 клетке от других кораблей.")
                position = None

    def take_turn(self):
        print("Это ваша доска:")
        print(self.board)
        print()

        while True:
            print("Это доска компьютера:")
            print(self.opponent.board.get_public_view())
            position = None
            while position is None:
                try:
                    position = input("Введите координаты вашего выстрела через запятую (номер столбца, номер строки): ")
                    coords = position.split(",")
                    x = int(coords[0]) - 1
                    y = int(coords[1]) - 1
                    repeat = self.opponent.board.is_repeated(x, y)
                    if (x < 0) or (x > 5) or (y < 0) or (y > 5):
                        raise Exception
                    elif repeat:
                        print("Вы уже стреляли в эту точку. Попробуйте еще раз.")
                        position = None
                except:
                    print(
                        "Координаты вашего выстрела должны быть в диапазоне от 1 до 6 включительно. Попробуйте еще раз.")
                    position = None

            hit_flag = self.opponent.board.attack(x, y)

            if hit_flag:
                killed = False 
                for boat in self.opponent.fleet:
                    killed = boat.is_drowned(x, y)
                    if killed:
                        break
                if killed: 
                    print("Вы потопили корабль!")
                else: 
                    print("Вы попали!")
                
                if self.opponent.board.is_defeated():
                    break
                else:
                        print("Стреляйте еще раз.")
            else:
                print("Вы промахнулись.")
                print("\n")
                break

        if self.opponent.board.is_defeated():
            return True
        else:
            return False

class Computer:

    def __init__(self):
        self.board = Board()
        self.fleet = [Boat("первый корабль", 3), Boat("второй корабль", 2), Boat("третий корабль", 2), Boat("четвертый корабль", 1), \
         Boat("пятый корабль", 1), Boat("шестой корабль", 1), Boat("седьмой корабль", 1)]
        self.opponent = None

    def set_opponent(self, opponent):
        self.opponent = opponent

    def position_fleet(self):

        for boat in self.fleet:
            self.position_boat(boat)

    def position_boat(self, boat):
        attemps = 0
        position = None
        while position is None:
            x = randint(1, 6) - 1
            y = randint(1, 6) - 1
            o = randint(0, 1)
            position = (x, y)
            attemps += 1
            if o == 0:
                orientation = "v"
            else:
                orientation = "h"
            boat.set_orientation(orientation)
            boat.set_position(x, y)
            if not self.board.add_boat(boat):
                position = None
            elif attemps > 2000:
                break

    def take_turn(self):
        while True:
            position = None
            while position is None:
                x = randint(0, 5)
                y = randint(0, 5)
                position = (x, y)
                repeat = self.opponent.board.is_repeated(x, y)
                if repeat:
                    position = None

            hit_flag = self.opponent.board.attack(x, y)
            
            if hit_flag:
                print("Компьютер попал в ваш корабль!")
                print("\n")
                if self.opponent.board.is_defeated():
                    break
            else:
                print("Компьютер промахнулся.")
                print("\n")
                break

        if self.opponent.board.is_defeated():
            return True
        else:
            return False

print('Начинаем игру "Морской бой"!')

game = Game()
game.play()