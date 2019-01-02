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


