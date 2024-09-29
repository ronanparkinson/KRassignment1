import agents
import random

class GameEnvironment(agents.Environment):
    """2_D environment"""
    def __init__(self, width=6,height=6):
        super.__init__()
        self.width = width
        self.height = height
        self.x_start, self.y_start = (3, 3)
        self.x_end, self.y_end = (self.width, self.height)
        self.startingLocation = self.x_start, self.y_end
        self.state = self.height, self.width

    def percept(self, agent):
        return self.state
    
    def execute_action(self, agent, action):
        agent.thud = False
        if action == 'left':
            agent.direction += agents.Direction.L
        if action == 'right':
            agent.direction += agents.Direction.R
        if action == 'up':
            agent.direction += agents.Direction.U
        if action == 'down':
            agent.direction += agents.Direction.D
    
    def starting_location(self, agent):
        agent.location = self.state
        self.add_thing(agent.location)

    def add_thing(self, thing, location=None):
        return super().add_thing(thing, location)
    
    def add_walls(self):
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width):
            self.add_thing(agents.Wall(), (x, 0))
            self.add_thing(agents.Wall(), (x, self.height - 1))
        for y in range(1, self.height - 1):
            self.add_thing(agents.Wall(), (0, y))
            self.add_thing(agents.Wall(), (self.width - 1, y))

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def add_coins(self):
        for x in range(self.width):
            self.add_thing(Coin(), (x, random.choice(len(self.width))))
            self.add_thing(Coin(), (x, random.choice(len(self.width))))
        for y in range(1, self.height - 1):
            self.add_thing(Coin(), (x, random.choice(len(self.height))))
            self.add_thing(Coin(), (x, random.choice(len(self.height))))
    
    def add_Rock(self):
        for x in range(self.width):
            self.add_thing(Rock(), (x, random.choice(len(self.width))))
        for y in range(1, self.height - 1):
            self.add_thing(Rock(), (x, random.choice(len(self.height)))) 



class Rock(agents.Thing):
    pass

class Coin(agents.Thing):
    pass

def AgentTypeOne():
    pass

def AgentTypeTwo():
    pass

def AgentTypeThree():
    pass