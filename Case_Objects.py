import random
class Element():

    def __init__(self, configuration):
        self.configuration = configuration

    def update(self, adventurer):
        pass

    def __str__(self):
        return "Element"

    def show(self):
        print(self)

    def show_event(self):
        print("What i do is ...")


    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        pass


class B(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        #end
    def __str__(self):
        return "."

    def show(self):
        print(self)

    def show_event(self):
        print("Blank cell")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_treasure:
            if (from_x, from_y) == self.configuration.start_position:
                reward = 100
            else:
                reward = -1
        # else :
            # reward = 3
        else :
            if (from_x, from_y) == self.configuration.start_position :
                reward = -1
            else :
                reward = -1

        return [(((from_x, from_y), has_sword, has_key, has_treasure), 1.)], reward


class C(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)


    def update(self, adventurer):
        Element.update(self, adventurer)
        adventurer.die()
        #end
    def __str__(self):
        return "C"

    def show(self):
        print(self)

    def show_event(self):
        print("immediate death")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_treasure:
            reward = 100
        else :
            reward = -200
        return [((self.configuration.start_position, has_sword, has_key, has_treasure), 1.)], reward

class E(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        if adventurer.has_sword:
            return
        random_value = random.random()
        if random_value <= 0.7:
            print("Adventurer is victorious")
        else:
            adventurer.die()
        #End
    def __str__(self):
        return "E"

    def show(self):
        print(self)

    def show_event(self):
        print("a malicious foe is attacking the adventurer (the adventurer is victorious with p_enemy probability, fixed to 0.7, otherwise the adventurer is dead")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if not has_sword:
            reward = -1
            return  [((self.configuration.start_position, has_sword, has_key, has_treasure), 0.3),
                     (((from_x, from_y), has_sword, has_key, has_treasure), 0.7)], reward
        else:
            reward = -1
            return [(((from_x, from_y), has_sword, has_key, has_treasure), 1.)], reward

class K(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        adventurer.has_key = True
        print("Adventurer gets a key")
        return self.configuration.Dungeon.remove_element(self)
        #end

    def __str__(self):
        return "K"

    def show(self):
        print(self)

    def show_event(self):
        print("necessary to open the treasure's room")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_key:
            reward = -1
        else:
            reward = 100
        return [(((from_x, from_y), has_sword, True, has_treasure), 1.)], reward

class P(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        print("... to a non wall cell")
        return self.configuration.move_adventurer_to_non_wall_cell()
        #end


    def __str__(self):
        return "P"

    def show(self):
        print(self)

    def show_event(self):
        print("a magic portal teleports the agent to a random (non-wall) cell of the dungeon")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        reward = -1
        list_of_non_wall_cells = self.configuration.Dungeon.list_of_non_wall_cells()
        return  [((dest_pos, has_sword, has_key, has_treasure), 1./len(list_of_non_wall_cells)) for dest_pos in list_of_non_wall_cells], reward

class MP(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)


    def update(self, adventurer):
        Element.update(self, adventurer)
        print("... to a neighbouring cell")
        return self.configuration.move_adventurer_to_neighbouring_cell()
        #end

    def __str__(self):
        return "-"

    def show(self):
        print(self)

    def show_event(self):
        print("the pavement is moving! the adventurer is forced to take refuge in one of the neighbouring cells (at random)")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        reward = -1
        list_of_neighbouring_cells = self.configuration.Dungeon.list_of_neighbouring_cells((from_x, from_y))
        return  [((dest_pos, has_sword, has_key, has_treasure), 1./len(list_of_neighbouring_cells)) for dest_pos in list_of_neighbouring_cells], reward

class S(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)


    def update(self, adventurer):
        Element.update(self, adventurer)
        adventurer.has_sword = True
        print("Adventurer gets a sword")
        return self.configuration.Dungeon.remove_element(self)
        #end
    def __str__(self):
        return "S"

    def show(self):
        print(self)

    def show_event(self):
        print("To open the door of the treasure's room it is necesary to have the golden key")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_sword:
            reward = -1
        else:
            reward = 10

        if has_key and has_treasure :
            reward = -1

        return [(((from_x, from_y), True, has_key, has_treasure), 1.)], reward


class R(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        random_value = random.random()
        if random_value <= 0.1:
            adventurer.die()
        elif random_value <= 0.4:
            print("Back to the starting position (trap)")
            adventurer.position = self.configuration.start_position
        else:
            print("Nothing happen (trap)")

        return True

    def __str__(self):
        return "R"

    def show(self):
        print(self)

    def show_event(self):
        print("a trap that either kill the adventurer (with probability 0.1), bring "
              "the adventure to the starting cell through an underground tunnel (probability 0.3)"
              "or nothin happen (probability 0.6)")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_treasure:
            reward = 40
        else:
            reward = -1
        return  [((self.configuration.start_position, has_sword, has_key, has_treasure), 0.4),
                 (((from_x, from_y), has_sword, has_key, has_treasure), 0.6)], reward


class T(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        if adventurer.has_key:
            print("Adventurer gets the treasure!")
            adventurer.has_treasure = True
            return self.configuration.Dungeon.remove_element(self)
        return False


    def __str__(self):
        return "T"

    def show(self):
        print(self)

    def show_event(self):
        print("To open the door of the treasure's room it is necesary to have the golden key")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_treasure:
            reward = -1
            return [(((from_x, from_y), has_sword, has_key, True), 1.)], reward
        elif has_key:
            reward = 100
            return [(((from_x, from_y), has_sword, has_key, True), 1.)], reward
        else:
            reward = -1#0
            return [(((from_x, from_y), has_sword, has_key,  has_treasure), 1.)], reward

class W(Element):

    def __init__(self, configuration):
        Element.__init__(self, configuration)

    def update(self, adventurer):
        Element.update(self, adventurer)
        print("Back to the starting position (wall)")
        adventurer.position = self.configuration.start_position

    def __str__(self):
        return "W"

    def show(self):
        print(self)

    def show_event(self):
        print("a attempt to moving to a wall will bounce to the starting position")

    def get_list_dest_and_rewards(self,from_x, from_y, has_treasure, has_sword, has_key):
        if has_treasure :
            reward = 100
        else:
            reward = -1
        return [((self.configuration.start_position, has_sword, has_key, has_treasure), 1.)], reward

