from Action import *
from Case_Objects import *
from Configuration import Configuration
from Useful_methods import *
import os
import time
#from getch import getch
# from gurobipy import *


class MDP_Solver():

    def __init__(self,filename):
        self.config = self.load_game(filename)
        self.StatesDict = {((i,j), has_sword, has_key, has_treasure) : dict()
                           for i in range(self.config.X)
                           for j in range(self.config.Y)
                           for has_key in [True, False]
                           for has_treasure in [True, False]
                           for has_sword in [True, False] if (not has_treasure) or has_key}
        self.Reward_tab = dict()
        nb = 0
        for state in self.StatesDict:
            position, has_sword, has_key, has_treasure = state
            self.Reward_tab[state] = dict()
            for action in Action.get_all_actions():
                # print(action)
                dx, dy = action
                x, y = position
                new_x = x+dx
                new_y = y+dy
                if self.config.Dungeon.is_valid_position(new_x, new_y):
                    #L : list of new positions and proba
                    L, reward = self.list_of_dest_position_proba_and_rewards(new_x, new_y, has_sword, has_key, has_treasure)
                    self.Reward_tab[state][action] = reward
                    nb += 1
                    for etat_destination, proba in L:
                        if action not in self.StatesDict[state]:
                            self.StatesDict[state][action] = set()
                        self.StatesDict[state][action].add((etat_destination, proba))

        # print("end mdp solver")

    def list_of_dest_position_proba_and_rewards(self, from_x, from_y, has_sword, has_key, has_treasure):
        case_element = self.config.Dungeon.grid[from_x][from_y]
        return case_element.get_list_dest_and_rewards(from_x, from_y, has_treasure, has_sword, has_key)


    def __str__(self):
        s = ""
        for state, associated_set in self.StatesDict.items():
            s += str(state)
            s += " : "
            s += str(associated_set)
            s += "\n"
        return s

    def run_value_iteration(self, epsilon):
        max_dif_i = 100 # never choose epsilo > 100
        #initialization
        i = 0
        States_Value_Table = {state : 0. for state in self.StatesDict}
        States_best_actions_Table = {state : None for state in self.StatesDict}
        #iterations
        while max_dif_i > epsilon:
            L = list()
            for state, value in States_Value_Table.items():
                best_action = None
                new_value = 0
                for action, Set_of_couple_of_dest_stat_proba in self.StatesDict[state].items():
                    state_action_value = self.Reward_tab[state][action]
                    for dest_stat, proba in Set_of_couple_of_dest_stat_proba:
                        state_action_value += 0.9 * States_Value_Table[dest_stat]*proba     #facteur d'actualisation = 0.9
                    if best_action == None or state_action_value > new_value:
                        best_action = action
                        new_value = state_action_value
                L.append(abs(value - new_value))
                max_dif_i = max(L)
                # print (max_dif_i)
                States_Value_Table[state] = new_value
                States_best_actions_Table[state] = best_action #.append(best_action)
            i += 1
        #calcul of optimal policy
        return States_best_actions_Table


    # def run_linear_programming_resolution(self):
    #     m = Model("MADI")
    #     #initialization
    #     #Dict correspondance state --> num variable
    #     State2varnumDict = dict()
    #     num = 0
    #     x = list()   #liste des objets variables gurobi
    #     for state in self.StatesDict:
    #         State2varnumDict[state] = num
    #         # x.append(m.addVar(name="x%d"%num))
    #         x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="x_%d"%num))
    #         # une variable par etat
    #         m.update()
    #         num += 1
    #     m.update()
    #     #les contraintes
    #     for state in self.StatesDict:
    #         for action, Set_of_couple_of_dest_stat_proba in self.StatesDict[state].items():
    #             c = LinExpr()
    #             c += x[State2varnumDict[state]]
    #             for dest_stat, proba in Set_of_couple_of_dest_stat_proba:
    #                 c -= 0.9*proba*x[State2varnumDict[dest_stat]]
    #                 # print(c)
    #             cst = m.addConstr(c >= self.Reward_tab[state][action], "Cstr state {} action {}".format(state, action))
    #             m.update()
    #             # print(cst)
    #     m.update()
    #     #l'objectif
    #     obj = LinExpr()
    #
    #     for i in range(len(x)):
    #         obj += x[i]
    #     m.setObjective(obj, GRB.MINIMIZE)
    #     m.update()
    #     # print(obj)
    #     m.optimize()
    #
    #     # Politique
    #     States_best_actions_Table = {state : None for state in self.StatesDict}
    #     for state in self.StatesDict:
    #         best_action = None
    #         best_value = 0
    #         for action, Set_of_couple_of_dest_stat_proba in self.StatesDict[state].items():
    #             state_action_value = self.Reward_tab[state][action]
    #             for dest_stat, proba in Set_of_couple_of_dest_stat_proba:
    #                 state_action_value += 0.9 * proba * x[State2varnumDict[dest_stat]].x
    #             if best_action == None or state_action_value > best_value:
    #                 best_action = action
    #                 best_value = state_action_value
    #         States_best_actions_Table[state] = best_action
    #     # print(States_best_actions_Table)
    #     return States_best_actions_Table

    def play(self):
        while not self.has_won():
            G.show()
            print("Press z (up), q(right), s(down) or d(left)\n")
            # print(">>> ")
            # car = getch()
            car = raw_input(">>> ")
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
            time.sleep(2)

            G.show()

    def play_with_policy(self, policy_dict):
        while not self.has_won():
            self.show()
            state = self.config.get_mdp_state()
            action = policy_dict[state]
            # print (action)
            self.config.Adventurer.move(action)
            time.sleep(1)

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
                    if DD_tab[x][y] == 0 or DD_tab[x][y] > DD_tab[x_c][y_c] + 1:
                        DD_tab[x][y] = DD_tab[x_c][y_c] + 1
                        E.add((x, y))

        key_reachable = False
        Keys_set = set(self.config.Dungeon.list_of_keys_cells())
        print(Keys_set)
        while not key_reachable and len(Keys_set) != 0:
            k_x, k_y = Keys_set.pop()
            if DD_tab[k_x][k_y] != 0:
                key_reachable = True

        t_x, t_y = self.config.Dungeon.treasure_position
        s = ""
        for i in range(self.config.X):
            for j in range(self.config.Y):
                s += str(DD_tab[i][j]) + " "
            s += "\n"
        print(s)

        return key_reachable and DD_tab[t_x][t_y] != 0

    def load_game(self, filename):
        return Configuration(filename)

    def has_won(self):
        return self.config.Adventurer.has_treasure and self.config.Adventurer.position == self.config.start_position

    def update(self):
        return 0

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
                prop = float(L[1]) / 100
                nb = int(prop * n * m)
                D[case_type] = nb
        generate_file_game(generate_position_cells_t(n, m, D))
        # print("end .game")
        return MDP_Solver(".game")




if __name__ == '__main__':
    # G = MDP_Solver.random_generation(10, 10, "EASY")
    G = MDP_Solver("bridge_to_victory")       #toujours un espace avant retour a la ligne
    # G = MDP_Solver("AK_game")       #toujours un espace avant retour a la ligne

    policy = G.run_value_iteration(0.01)
    # policy = G.run_linear_programming_resolution()
    print_policy(policy, G.config.X, G.config.Y)

    if G.is_winnable():
        G.play_with_policy(policy)