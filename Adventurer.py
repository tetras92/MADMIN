class Adventurer:

    def __init__(self, configuration=None):
        self.configuration = configuration
        self.position = self.configuration.start_position
        self.has_sword = False
        self.has_key = False
        self.has_treasure = False


    def move(self, action):
        dx, dy = action
        x, y = self.position
        if self.configuration.Dungeon.is_valid_position(x=x+dx, y=y+dy):
            self.position = x+dx, y+dy
            self.configuration.Dungeon.update(self)

    def die(self):
        print("Adventurer dies")
        self.position = self.configuration.start_position
        self.configuration.reset()                               #AJOUTEE
        
