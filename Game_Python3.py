from Configuration import Configuration
from Case_Objects import *
from Useful_methods import *
import os
import time
from getch import getch

class Game:

    def __init__(self, filename):
        self.config = self.load_game(filename)

    def play(self):
        self.show()
        while not self.has_won():

            print("Press z (up), q(right), s(down) or d(left)\n")
            print(">>> ")
            car = getch()
            # car = raw_input(">>> ")
            if car == "z":
                self.config.Adventurer.move(Action.UP)
            elif car == "s":
                self.config.Adventurer.move(Action.DOWN)
            elif car == "q":
                self.config.Adventurer.move(Action.LEFT)
            elif car == "d":
                self.config.Adventurer.move(Action.RIGHT)
            else:
                print("Error")

            self.show()

    def play_with_policy(self, policy_dict):
        while not self.has_won():
            self.show()
            state = self.config.get_state()
            action = policy_dict[state]
            # print (action)
            self.config.Adventurer.move(action)
            time.sleep(0.5)

    def is_winnable(self):
        DD_tab = [[0 for j in range(self.config.Y)] for i in range(self.config.X)]
        x_A, y_A = self.config.Adventurer.position
        DD_tab[x_A][y_A] = 1
        E = set()
        E.add(self.config.Adventurer.position)
        while len(E) != 0:
            current_pos = E.pop()
            x_c, y_c = current_pos
            Neigh_cells = self.config.Dungeon.list_of_neighbouring_cells(current_pos)
            for x, y in Neigh_cells:
                O = self.config.Dungeon.grid[x][y]
                if not isinstance(O, W) and not isinstance(O, C):
                    if DD_tab[x][y] == 0 or DD_tab[x][y] >  DD_tab[x_c][y_c] + 1:
                        DD_tab[x][y] = DD_tab[x_c][y_c] + 1
                        E.add((x, y))

        key_reachable = False
        Keys_set = set(self.config.Dungeon.list_of_keys_cells())
        # print(Keys_set)
        while not key_reachable and len(Keys_set) != 0:
            k_x, k_y= Keys_set.pop()
            if DD_tab[k_x][k_y] != 0:
                key_reachable = True

        t_x, t_y = self.config.Dungeon.treasure_position
        s = ""
        for i  in range(self.config.X):
            for j in range(self.config.Y):
                s += str(DD_tab[i][j]) + " "
            s += "\n"
        # print(s)

        return key_reachable and DD_tab[t_x][t_y] != 0

    def load_game(self,filename):
        return Configuration(filename)

    def has_won(self):
        return self.config.Adventurer.has_treasure and self.config.Adventurer.position == self.config.start_position

    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.config.show()

    @staticmethod
    def random_generation(n, m, level="HARD"):
        D = dict()
        with open(level, "r") as file:
            for line in file:
                L = line.split(" ")
                case_type = L[0]
                prop = float(L[1])/100
                nb = int(prop * n * m)
                D[case_type] = nb
        generate_file_game(generate_position_cells_t(n, m, D))
        return Game(".game")

if __name__ == '__main__':
    filename = "Instances/example_grid"
    # filename = "Instances/EASY_10_10"
    # filename = "Instances/MEDIUM_10_10"
    # filename = "Instances/bridge_to_victory"


    G = Game(filename)
    G.play()
