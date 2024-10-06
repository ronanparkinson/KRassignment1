import agents
import random
import collections


class Agent(agents.Thing):
    """An Agent is a subclass of Thing with one required instance attribute 
    (aka slot), .program, which should hold a function that takes one argument,
    the percept, and returns an action. (What counts as a percept or action 
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method. If it were a method, then the
    program could 'cheat' and look at aspects of the agent. It's not supposed
    to do that: the program can only look at the percepts. An agent program
    that needs a model of the world (and of the agent itself) will have to
    build and maintain its own model. There is an optional slot, .performance,
    which is a number giving the performance measure of the agent in its
    environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        #self.movesRemainging = 20
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False

class GameEnvironment(agents.Environment):
    """2_D environment"""
    def __init__(self, width=6,height=6, movesLeft=20):
        super().__init__()
        self.width = width
        self.height = height
        self.x_start, self.y_start = (0,0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
        self.totalCoinsAvailable = 0

    def thing_classes(self):
        return [agents.Wall, Rock, Coin, tableBasedAgent]

    def percept(self, agent):
        #print("test")
        
        return agent.location
       
    def add_coins(self):
        for x in range(self.width):
            self.add_thing(Coin(), (x, random.choice(len(self.width -1))))
            self.add_thing(Coin(), (x, random.choice(len(self.width -1))))
            print("Coin test")
            self.totalCoinsAvailable += 2
            
        for y in range(1, self.height - 1):
            self.add_thing(Coin(), (y, random.choice(len(self.height -1))))
            self.add_thing(Coin(), (y, random.choice(len(self.height -1))))
            print("Coin test 2")
            self.totalCoinsAvailable += 2
    
    def add_Rock(self):
        for x in range(self.width):
            self.add_thing(Rock(), (x, random.choice(len(self.width -1))))
            print("Rock test")
        for y in range(1, self.height - 1):
            self.add_thing(Rock(), (y, random.choice(len(self.height -1))))
            self.add_thing(Rock(), (y, random.choice(len(self.height -1))))
            print("Rock 2test")

    def execute_action(self, agent, action):
        agent.bump = False
        print(agent.location)
        if action == 'left':
            agent.direction = agents.Direction.L
            
            agent.performance += 1
         #   print("l")
        elif action == 'right':
            agent.direction = agents.Direction.R
            agent.performance += 1
            print(agent.performance)
       #     print("r")
        elif action == 'up':
            agent.direction = agents.Direction.U
            agent.performance += 1
            print(agent.performance)
       #     print("u")
        elif action == 'down':
            agent.direction = agents.Direction.D
            agent.performance += 1
            print(agent.performance)
          #  print("d")
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agents.Direction.move_forward(self, agent.location))
        #print(agent.performance)

    def move_to(self, thing, destination):
        thing.bump = self.some_things_at(destination, Rock)
        print("different test")
        if not thing.bump:
            if self.some_things_at(destination, Coin):
                print("Found a coin!")
                self.things.remove(Coin)
                self.totalCoinsAvailable -= 1
                thing.location = destination
            if(thing.performance == 20):
                self.is_done()
        return thing.bump
    
    def add_thing(self, thing, location=None):
        #print("test")
        return super().add_thing(thing, location)
    
    def add_walls(self): 
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width):
            self.add_thing(agents.Wall(), (x, 0))
            self.add_thing(agents.Wall(), (x, self.height - 1))
          #  print("Wall test")

        for y in range(1, self.height - 1):
            self.add_thing(agents.Wall(), (0, y))
            self.add_thing(agents.Wall(), (self.width - 1, y))
          #  print("Wall test 2")

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
       # print("!oops")
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def default_location(self, thing):
        location = self.random_location_inbounds()
        while self.some_things_at(location, Rock) or self.some_things_at(location, Coin):
            # we will find a random location with no obstacles
            location = self.random_location_inbounds()
      #  print("huh...")        
        return location

    def random_location_inbounds(self, exclude=None):
        """Returns a random location that is inbounds (within walls if we have walls)"""
        location = (random.randint(self.x_start, self.x_end),
                    random.randint(self.y_start, self.y_end))
        if exclude is not None:
            while location == exclude:
                location = (random.randint(self.x_start, self.x_end),
                            random.randint(self.y_start, self.y_end))
        return location
  #  def move_rock(self):
  #      if self.movesLeft == 15 | self.movesLeft == 10 | self.move_rock == 5:
  #          self.things
  
class Rock(agents.Thing):
    pass

class Coin(agents.Thing):
    pass

def tableBasedAgent():
    #total moves from table equals 20 moves
    table = {
    (((0, 0), Coin()),): 'right',   
    (((1, 0,), None),): 'right', 
    (((2, 0), Coin()),): 'up',       
    (((2, 1), None),): 'left',   
    (((1, 1), None),): 'right', 
    (((2, 1), Rock()),): 'up',
    (((2, 2), None),): 'right',
    (((3 ,2), None),): 'down',
    (((3, 1), None),): 'right',
    (((4, 1), Coin()),): 'up',
    (((4, 2), Rock()),): 'left',
    (((3, 2), None),): 'up',
    (((3, 3), None),): 'up',
    (((3, 4), Coin()),): 'right',
    (((4, 4), None),): 'up',
    (((4, 5), None),): 'right',
    (((5, 5), None),): 'down',
    (((5, 4), None),): 'down',
    (((4, 4), None),): 'left',
    (((3, 4), None),): 'up'
    }
    return agents.Agent(agents.TableDrivenAgentProgram(table))


def AgentTypeTwo():
    pass

def AgentTypeThree():
    pass

#agents.compare_agents()
environment = GameEnvironment
agentsList = [tableBasedAgent]
result = agents.compare_agents(environment, agentsList, n=1, steps=20)

performance_tableBasedAgent = result[0][1]

print("performance of GameEnvironment", performance_tableBasedAgent)