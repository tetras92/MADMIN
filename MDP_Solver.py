from gurobipy import *
from Game import Game
from Useful_methods import *


class MDP_Solver():

    def __init__(self, configuration):
        self.StatesDict = {((i,j), has_sword, has_key, has_treasure) : dict()
                           for i in range(configuration.X)
                           for j in range(configuration.Y)
                           for has_key in [True, False]
                           for has_treasure in [True, False]
                           for has_sword in [True, False] if (not has_treasure) or has_key}
        self.Reward_tab = dict()
        nb = 0
        self.config = configuration
        for state in self.StatesDict:
            position, has_sword, has_key, has_treasure = state
            self.Reward_tab[state] = dict()
            for action in Action.get_all_actions():
                # print(action)
                dx, dy = action
                x, y = position
                new_x = x+dx
                new_y = y+dy
                if configuration.Dungeon.is_valid_position(new_x, new_y):
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


    def run_linear_programming_resolution(self):
        m = Model("MADI")
        #initialization
        #Dict correspondance state --> num variable
        State2varnumDict = dict()
        num = 0
        x = list()   #liste des objets variables gurobi
        for state in self.StatesDict:
            State2varnumDict[state] = num
            # x.append(m.addVar(name="x%d"%num))
            x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="x_%d"%num))
            # une variable par etat
            m.update()
            num += 1
        m.update()
        #les contraintes
        for state in self.StatesDict:
            for action, Set_of_couple_of_dest_stat_proba in self.StatesDict[state].items():
                c = LinExpr()
                c += x[State2varnumDict[state]]
                for dest_stat, proba in Set_of_couple_of_dest_stat_proba:
                    c -= 0.9*proba*x[State2varnumDict[dest_stat]]
                    # print(c)
                m.addConstr(c >= self.Reward_tab[state][action], "Cstr state {} action {}".format(state, action))
                m.update()
        m.update()
        #l'objectif
        obj = LinExpr()

        for i in range(len(x)):
            obj += x[i]
        m.setObjective(obj, GRB.MINIMIZE)
        m.update()
        # print(obj)
        m.optimize()
        print("=====> ", m.Runtime)
        # Politique
        States_best_actions_Table = {state : None for state in self.StatesDict}
        for state in self.StatesDict:
            best_action = None
            best_value = 0
            for action, Set_of_couple_of_dest_stat_proba in self.StatesDict[state].items():
                state_action_value = self.Reward_tab[state][action]
                for dest_stat, proba in Set_of_couple_of_dest_stat_proba:
                    state_action_value += 0.9 * proba * x[State2varnumDict[dest_stat]].x
                if best_action == None or state_action_value > best_value:
                    best_action = action
                    best_value = state_action_value
            States_best_actions_Table[state] = best_action
        # print(States_best_actions_Table)
        return States_best_actions_Table



if __name__ == '__main__':

    filename = "HARD_10_10"
    G = Game("Instances/"+filename)
    mdp_solver = MDP_Solver(G.config)
    # policy = mdp_solver.run_value_iteration(0.01)                           # ITERATION VALUE

    policy = mdp_solver.run_linear_programming_resolution()               # LINEAR PROGRAMING
    print_policy(policy, G.config.X, G.config.Y)

    # if G.is_winnable():
    #     G.play_with_policy(policy)
