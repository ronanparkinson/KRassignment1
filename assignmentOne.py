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
        self.movesRemainging = 20
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
    def __init__(self, width=6,height=6):
        super().__init__()
        self.width = width
        self.height = height
        self.observers = []
        self.x_start, self.y_start = (0,0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
        self.totalCoinsAvailable = 0

    def thing_classes(self):
        return [agents.Wall, Rock, Coin, tableBasedAgent]

    def percept(self, agent):   
        return agent.location
       
    def add_Rock(self):
        for x in range(self.width):
            self.add_thing(Rock(), (x, random.randint(self.width -1)))
            print(f"Added rock at: {(x, random.randint(0, self.height - 1))}")
        for y in range(1, self.height - 1):
            self.add_thing(Rock(), (y, random.randint(self.height -1)))
            self.add_thing(Rock(), (y, random.randint(self.height -1)))
            print(f"Added rock at: {(y, random.randint(0, self.width - 1))}")



    def execute_action(self, agent, action):
        agent.bump = False
        print(agent.location)
        #chat
        if action == 'left':
            destination = (agent.location[0] - 1, agent.location[1])
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                agent.performance += 1
                print(f"Moved left to {agent.location}")
        elif action == 'right':
            destination = (agent.location[0] + 1, agent.location[1])
            agent.bump = self.move_to(agent, destination)
            #print(agent.bump)
            if agent.bump == True:
                agent.location = destination
                agent.performance += 1
                print(f"Moved right to {agent.location}")
        elif action == 'up':
            destination = (agent.location[0], agent.location[1] + 1)
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                agent.performance += 1
                print(f"Moved up to {agent.location}")
        elif action == 'down':
            destination = (agent.location[0], agent.location[1] - 1)
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                agent.performance += 1
                print(f"Moved down to {agent.location}")

    def move_to(self, thing, destination):
        #print(thing)
        thing.bump = self.some_things_at(destination, agents.Obstacle)
        if not thing.bump:
            for o in self.observers:
                o.thing_moved(thing)
            print("test")
            if self.some_things_at(destination, Coin):
                print("Found a coin!")
                agents.XYEnvironment.delete_thing(Coin)
                self.totalCoinsAvailable -= 1
        print(thing.bump)
        return thing.bump
    
    def add_thing(self, thing, location=None):
        print(f"Adding {thing} to the environment at {location}")
        return super().add_thing(thing, location)
    
    def delete_thing(self, thing):
        super().delete_thing(thing)
    
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

    def add_coins(self):
        for x in range(self.width):
            #self.add_thing(Coin(), (x, random.randint(self.width -1)))
            #self.add_thing(Coin(), (x, random.randint(self.width -1)))

            location = (x, random.randint(0, self.height - 1))
            self.add_thing(Coin(), location)  # Adding coins
            print(f"Added coin at {location}")  # Debugging print
            location = (x, random.randint(0, self.height - 1))
            self.add_thing(Coin(), location)  # Adding coins
            print(f"Added coin at {location}")
            self.totalCoinsAvailable += 2
            
        for y in range(1, self.height - 1):
            location = (random.randint(0, self.width - 1), y)
            self.add_thing(Coin(), location)  # Adding coins
            print(f"Added coin at {location}") 
            location = (random.randint(0, self.width - 1), y)
            self.add_thing(Coin(), location)  # Adding coins
            print(f"Added coin at {location}") 
            self.totalCoinsAvailable += 2

    def add_observer(self, observer):
        """Adds an observer to the list of observers.
        An observer is typically an EnvGUI.

        Each observer is notified of changes in move_to and add_thing,
        by calling the observer's methods thing_moved(thing)
        and thing_added(thing, loc)."""
        self.observers.append(observer)

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
       # print("!oops")
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def default_location(self, thing):
        location = (self.random_location_inbounds())
        while self.some_things_at(location, Rock) or self.some_things_at(location, Coin):
            # we will find a random location with no obstacles
            location = self.random_location_inbounds()
        print("huh...")        
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
  
class Rock(agents.Obstacle):
    pass

class Coin(agents.Thing):
    pass

def tableBasedAgent():
    #total moves from table equals 20 moves
    table = {
        ((0, 0), ): 'right',
        ((0, 0), (1, 0),): 'right',
        ((0, 0), (1, 0), (2, 0), ): 'up',
        ((0, 0), (1, 0), (2, 0), (2, 1), ): 'up'
    }
    return agents.Agent(agents.TableDrivenAgentProgram(table))


def RandomReflexAgent():
    pass

def AgentTypeThree():
    pass

#agents.compare_agents()
environment = GameEnvironment
agentsList = [tableBasedAgent]
result = agents.compare_agents(environment, agentsList, n=1, steps=20)

performance_tableBasedAgent = result[0][1]

print("performance of GameEnvironment", performance_tableBasedAgent)