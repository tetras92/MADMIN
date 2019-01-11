from Case_Objects import *
from Action import Action

class Dungeon:

    def __init__(self, n, m):
        self.grid = [[None for j in range(m)] for i in range(n)]
        self.size_x = m
        self.size_y = n
        self.start_position = (n-1, m-1)
        self.treasure_position = (0, 0)


    def is_valid_position(self, x, y):
        return x >= 0 and x < self.size_x and y >= 0 and y < self.size_y

    def list_of_non_wall_cells(self):
        L = list()
        for j in range(self.size_y):
            for i in range(self.size_x):
                if not isinstance(self.grid[j][i], W):
                    L.append((j, i))
        return L

    def list_of_neighbouring_cells(self, position):
        L = list()
        x, y = position
        for action in Action.get_all_actions():
            dx, dy = action
            if self.is_valid_position(x+dx, y+dy):
                L.append((x+dx, y+dy))
        return L

    def remove_element(self, element):
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i][j] is element:
                    self.grid[i][j] = B(None)
                    return True
        return False

    def list_of_keys_cells(self):
        L = list()
        for j in range(self.size_y):
            for i in range(self.size_x):
                if isinstance(self.grid[j][i], K):
                    L.append((j, i))
        return L

    def update(self, adventurer):
        x, y = adventurer.position
        self.grid[x][y].update(adventurer)

    def get(self, i, j):
        return self.grid[i][j]
