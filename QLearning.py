from Action import *
from Case_Objects import *
from Game import Game
import time
from Useful_methods import print_policy
class QLearning():

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
        self.current_policy = dict()
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

        # if isinstance(case_element, W):
        #     if has_treasure :
        #         reward = 100
        #     else:
        #         reward = -1
        #     return reward
        # elif isinstance(case_element, E):
        #     if not has_sword:
        #         reward = -1
        #         return  reward
        #     else:
        #         reward = 3
        #         return reward
        # elif isinstance(case_element, C):
        #     reward = -5
        #     return reward
        # elif isinstance(case_element, P):
        #     reward = 0
        #     return  reward
        # elif isinstance(case_element, MP):
        #     reward = 1
        #     return  reward
        # elif isinstance(case_element, R):
        #     if has_treasure:
        #         reward = 3
        #     else:
        #         reward = 0
        #     return reward
        # elif isinstance(case_element, T):
        #     if has_treasure:
        #         reward = 0
        #         return reward
        #     elif has_key:
        #         reward = 100
        #         return reward
        #     else:
        #         reward = 0
        #         return reward
        # elif isinstance(case_element, S):
        #     if has_sword:
        #         reward = 3
        #     else:
        #         reward = 5
        #     return reward
        # elif isinstance(case_element, K):
        #     if has_key:
        #         reward = 3
        #     else:
        #         reward = 10
        #     return reward
        # elif isinstance(case_element, B):
        #     if has_treasure:
        #         if (from_x, from_y) == self.config.start_position:
        #             reward = 10
        #         else:
        #             reward = 2
        #     else:
        #         reward = 3
        #     return reward
        # else:
        #     print("Error")
        #     exit(1001)


    def best_action_from_state(self, state):
        best_action = None
        expected_reward_associated = 0
        if random.random() < 0.5:
            L = list(self.Q_table[state].keys())
            return L[random.randint(0, len(L)-1)]

        for possible_action in self.Q_table[state]:
            if best_action == None or self.Q_table[state][possible_action] > expected_reward_associated:
                # if self.Q_table[state][possible_action] > expected_reward_associated:
                #     print("ame")
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

    def run_Q_learning(self, max_episodes=10000):
        episode = 0

        while episode < max_episodes:
            # self.QGame.show()
            episode += 1
            state = self.QGame.config.state
            action = self.best_action_from_state(state)
            self.QGame.config.Adventurer.move(action)
            reward = self.Reward_tab[state][action]
            state_after_move = self.QGame.config.state
            max_expected_reward_for_state_after_move = max(self.Q_table[state_after_move].values())
            self.Q_table[state][action] += (0.8 * (reward + 0.9 * max_expected_reward_for_state_after_move - self.Q_table[state][action]))
            if self.QGame.has_won():
                self.QGame.config.reset()
            # time.sleep(1)
            # self.QGame.show()

        policy = {state : self.best_action_from_state_policy(state) for state in self.Q_table}
        # print(episode)
        return policy



if __name__ == '__main__':
    QL = QLearning("AK_game")
    policy = QL.run_Q_learning()
    print_policy(policy, QL.config.X, QL.config.Y)
    G = Game("AK_game")
    G.play_with_policy(policy)
