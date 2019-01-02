import random
from Case_Objects import *
from Dungeon import Dungeon
from Adventurer import Adventurer
class Configuration:

    def __init__(self, filename):
        with open(filename) as file:
            line = file.readline()
            dimL = line.split(" ")
            n = int(dimL[0])
            m = int(dimL[1])
            self.Dungeon = Dungeon(n, m)
            self.X = self.Dungeon.size_x
            self.Y = self.Dungeon.size_y
            self.start_position = self.Dungeon.start_position
            for i in range(n):
                line = file.readline()
                ElemL = line.split(" ")
                for j in range(m):
                    elmnt = ElemL[j][:1]
                    self.add_element(elmnt, i, j)

        self.Adventurer = Adventurer(self)

    def get_adventurer_position(self):
        return self.Adventurer.position


    def move_adventurer_to_non_wall_cell(self):
        #L : list of non-wall cells
        L = self.Dungeon.list_of_non_wall_cells()
        self.Adventurer.position = L[random.randint(0, len(L)-1)]
        self.Dungeon.update(self.Adventurer)
        return True

    def move_adventurer_to_neighbouring_cell(self):
        cell_x, cell_y = self.Adventurer.position
        #L : list of neighbouring cells
        L = self.Dungeon.list_of_neighbouring_cells(self.Adventurer.position)
        self.Adventurer.position = L[random.randint(0, len(L)-1)]
        self.Dungeon.update(self.Adventurer)
        return True

    def add_element(self, type, i, j):
        if type == "B":
            self.Dungeon.grid[i][j] = B(self)
        elif type == "T":
            self.Dungeon.grid[i][j] = T(self)
        elif type == "R":
            self.Dungeon.grid[i][j] = R(self)
        elif type == "C":
            self.Dungeon.grid[i][j] = C(self)
        elif type == "S":
            self.Dungeon.grid[i][j] = S(self)
        elif type == "K":
            self.Dungeon.grid[i][j] = K(self)
        elif type == "E":
            self.Dungeon.grid[i][j] = E(self)
        elif type == "P":
            self.Dungeon.grid[i][j] = P(self)
        elif type == "-":
            self.Dungeon.grid[i][j] = MP(self)
        elif type == "W":
            self.Dungeon.grid[i][j] = W(self)
        else:
            exit(1000)

    def get_mdp_state(self):
        return (self.Adventurer.position, self.Adventurer.has_sword, self.Adventurer.has_key, self.Adventurer.has_treasure)

    def __str__(self):
        s = ""
        for i in range(self.X):
            for j in range(self.Y):
                if (i, j) != self.Adventurer.position:
                    s += str(self.Dungeon.grid[i][j])
                    s += " "
                else:
                    s += "* "
            s += "\n"
        s += "="*(self.Y * 2)
        s += "\n"
        return s

    def show(self):
        print(self)
