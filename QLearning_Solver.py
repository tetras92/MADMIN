from Action import *
from Case_Objects import *
from Game import Game
from Useful_methods import print_policy


class QLearning_Solver():

    def __init__(self, filename):
        self.QGame = Game(filename)
        configuration = self.QGame.config
        self.StatesDict = {((i,j), has_sword, has_key, has_treasure) : dict()
                           for i in range(configuration.X)
                           for j in range(configuration.Y)
                           for has_key in [True, False]
                           for has_treasure in [True, False]
                           for has_sword in [True, False] if (not has_treasure) or has_key}
        self.Reward_tab = dict()
        self.Q_table = dict()
        self.config = configuration
        for state in self.StatesDict:
            position, has_sword, has_key, has_treasure = state
            self.Reward_tab[state] = dict()
            self.Q_table[state] = dict()
            for action in Action.get_all_actions():
                dx, dy = action
                x, y = position
                new_x = x+dx
                new_y = y+dy
                if configuration.Dungeon.is_valid_position(new_x, new_y):
                    reward = self.associated_reward(new_x, new_y, has_sword, has_key, has_treasure)
                    self.Reward_tab[state][action] = reward
                    self.Q_table[state][action] = 0                                                 #initialization of Q_Table


    def associated_reward(self, from_x, from_y, has_sword, has_key, has_treasure):
        case_element = self.config.Dungeon.grid[from_x][from_y]
        return case_element.get_list_dest_and_rewards(from_x, from_y, has_treasure, has_sword, has_key)[1]

    def best_action_from_state(self, state):
        best_action = None
        expected_reward_associated = 0
        if random.random() < 0.1:
            L = list(self.Q_table[state].keys())
            return L[random.randint(0, len(L)-1)]

        for possible_action in self.Q_table[state]:
            if best_action == None or self.Q_table[state][possible_action] > expected_reward_associated:
                best_action = possible_action
                expected_reward_associated = self.Q_table[state][possible_action]
        return best_action

    def best_action_from_state_policy(self, state):
        best_action = None
        expected_reward_associated = 0
        for possible_action in self.Q_table[state]:
            if best_action == None or self.Q_table[state][possible_action] > expected_reward_associated:
                best_action = possible_action
                expected_reward_associated =  self.Q_table[state][possible_action]
        return best_action

    def run_Q_learning(self, max_episodes=100):
        episode = 0

        while episode < max_episodes:

            state = self.QGame.config.state
            action = self.best_action_from_state(state)
            self.QGame.config.Adventurer.move(action)
            reward = self.Reward_tab[state][action]
            state_after_move = self.QGame.config.state
            max_expected_reward_for_state_after_move = max(self.Q_table[state_after_move].values())
            self.Q_table[state][action] += (0.1 * (reward + 0.9 * max_expected_reward_for_state_after_move - self.Q_table[state][action]))
            if self.QGame.has_won():
                episode += 1
                self.QGame.config.reset()


        policy = {state : self.best_action_from_state_policy(state) for state in self.Q_table}
        return policy



if __name__ == '__main__':
    filename = "Instances/example_grid"
    # filename = "Instances/EASY_10_10"
    # filename = "Instances/MEDIUM_10_10"
    # filename = "Instances/bridge_to_victory"

    QL = QLearning_Solver(filename)

    G = Game(filename)
    if G.is_winnable():
        policy = QL.run_Q_learning()
        print_policy(policy, QL.config.X, QL.config.Y)
        G.play_with_policy(policy)
    else:
        print ("Game can not be won!!!")
