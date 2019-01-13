class Action():
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


    @staticmethod
    def get_all_actions():
        return [Action.UP, Action.LEFT, Action.RIGHT, Action.DOWN]
