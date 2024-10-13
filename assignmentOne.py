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
    def __init__(self, width=8,height=8):
        super().__init__()
        self.width = width
        self.height = height
        self.visited = []
        self.x_start, self.y_start = (0,0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
        self.totalCoinsAvailable = 0
        self.add_coins()
        self.add_Rock()
        self.add_walls()

    def thing_classes(self):
        return [agents.Wall, Rock, Coin, tableBasedAgent, RandomReflexAgent, ModelAgent]

    def percept(self, agent):   
        return agent.location #, agent.visited
       
    def execute_action(self, agent, action):
        agent.bump = False
        #chat
        if action == 'left':
            print('test')
            destination = (agent.location[0] - 1, agent.location[1])
            wasVisited = self.isVisited(destination)
            if wasVisited == True:
                print("Location was already visited!")
                return
            else:
                agent.bump = self.move_to(agent, destination)
                if agent.bump == True:
                    agent.location = destination
                    #agent.performance += 1
                    print(f"Moved left to {agent.location}")
        elif action == 'right':
            print('testTwo')
            destination = (agent.location[0] + 1, agent.location[1])
            wasVisited = self.isVisited(destination)
            if wasVisited == True:
                print("Location was already visited!")
                return
            else:
                agent.bump = self.move_to(agent, destination)
                if agent.bump == True:
                    agent.location = destination
                    #agent.performance += 1
                    print(f"Moved right to {agent.location}")
        elif action == 'up':
            print('test3')
            destination = (agent.location[0], agent.location[1] + 1)
            wasVisited = self.isVisited(destination)
            if wasVisited == True:
                print("Location was already visited!")
                return
            else:
                agent.bump = self.move_to(agent, destination)
                if agent.bump == True:
                    agent.location = destination
                    #agent.performance += 1
                    print(f"Moved up to {agent.location}")
        elif action == 'down':
            print('test4')
            destination = (agent.location[0], agent.location[1] - 1)
            wasVisited = self.isVisited(destination)
            if wasVisited == True:
                print("Location was already visited!")
                return
            else:
                agent.bump = self.move_to(agent, destination)
                if agent.bump == True:
                    agent.location = destination
                #  agent.performance += 1
                    print(f"Moved down to {agent.location}")

    def move_to(self, thing, destination):
        #print(thing)
        thing.bump = self.some_things_at(destination, agents.Obstacle)
        thing.location = destination
        #print("test")
        if self.some_things_at(destination, Coin):
            print("Found a coin!")
            self.delete_thing(thing)
            self.totalCoinsAvailable -= 1
            thing.performance += 1
        #print(thing.bump)
        return thing.bump
    
    def isVisited(self, location):
        wasVisited = False
        for spot in self.visited:
            if location == spot:
                wasVisited == True
        return wasVisited
        
    def add_thing(self, thing, location=None):
        if location is None:
            location = self.random_location_inbounds()  # Ensure the agent has a location
        thing.location = location  # Set the thing's location
        print(f"Adding {thing} to the environment at {location}")
        return super().add_thing(thing, location)
    
    def delete_thing(self, thing):
        super().delete_thing(thing)
    
    def add_walls(self): 
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width):
            self.add_thing(agents.Wall(), (x, 0))
            self.add_thing(agents.Wall(), (x, self.height - 1))

        for y in range(1, self.height - 1):
            self.add_thing(agents.Wall(), (0, y))
            self.add_thing(agents.Wall(), (self.width - 1, y))

    def add_coins(self):
            self.add_thing(Coin(), self.random_location_inbounds())
            self.totalCoinsAvailable += 1

    def add_Rock(self):
            self.add_thing(Rock(), self.random_location_inbounds())
            self.add_thing(Rock(), self.random_location_inbounds())

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def random_location_inbounds(self, exclude=None):
        """Returns a random location that is inbounds (within walls if we have walls)"""
        location = (random.randint(self.x_start, self.x_end),
                    random.randint(self.y_start, self.y_end))
        if exclude is not None:
            while location == exclude:
                location = (random.randint(self.x_start, self.x_end),
                            random.randint(self.y_start, self.y_end))
        return location

  
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


def RandomReflexSoftware(moveList):
    return lambda percept: random.choice(moveList)

def RandomReflexAgent():
    return agents.Agent(agents.RandomAgentProgram(['left', 'right', 'up', 'down']))

def ModelAgentSoftware(moveList):

    move = random.choice(moveList)

    def program(percept):
        visitedLocation = []
        visited = False
        location = percept

        for pastVisited in visitedLocation:
            if location == pastVisited:
                visited == True
            else:
                visitedLocation.append(location)    
        return visited
    
    return move, program

def ModelAgent():
    return Agent(ModelAgentSoftware(['left', 'right', 'up', 'down']))



environment = GameEnvironment
agentsList = [RandomReflexAgent]
result = agents.compare_agents(environment, agentsList, n=1, steps=20)

performance_tableBasedAgent = result[0][1]
#performance_RandomReflexAgent = result[1][1]


print("performance of GameEnvironment", performance_tableBasedAgent)
#print("performance of GameEnvironment Two", performance_RandomReflexAgent)


#Q2

import random
from agents import Agent
from search import Problem, breadth_first_graph_search, depth_first_graph_search
from assignmentOne import GameEnvironment

class Rock(agents.Obstacle):
    pass

class Coin(agents.Thing):
    pass

class RandomAgent(Agent):
    def __init__(self):
        super().__init__()
        self.program = self.possibleMoves

    def possibleMoves(self):
        return random.choice(['left', 'right', 'up', 'down'])
    
class SearchEnvironment(GameEnvironment):

    def __init__(self, width=8, height=8):
        super().__init__(width, height)
        self.add_coins()
        self.add_Rock()

    def add_coins(self):
        return super().add_coins()
    def add_Rock(self):
        return super().add_Rock()
    
class CoinProblem(Problem):
    def __init__(self, initial_state, width, height):
        print("Initial state:", initial_state)
        self.width = width
        self.height = height
        self.x_start, self.y_start = (0,0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
        super().__init__(initial_state)

    def actions(self, state):
        print('actions', state)
        (x, y), _, _ = state
        print("Current state:", state)
        print("testing new moves here!")
        moves = []

        if x > 0:
            moves.append('left')
        if x < self.width - 1:
            moves.append('right')
        if y > 0 and (x, y - 1):
            moves.append('down')
        if y < self.height - 1:
            moves.append('up')
        
        return moves
    
    def result(self, state, action):
        print('result', state )
        (x, y), coin_location, rocks_locations = state
        coin_location = set(coin_location)
        rocks_locations = set(rocks_locations)

        if action == 'left':
            print('left')
            destination = (x - 1, y)
            if destination in rocks_locations:
                print('in rocks')
                return (x, y), tuple(coin_location), tuple(rocks_locations)
            if GameEnvironment.is_inbounds(self, destination):
                print('iiiii')
                if (x, y) in coin_location:
                    coin_location.remove((x, y))
                return (destination, tuple(coin_location), tuple(rocks_locations))
        elif action == 'right':
            print('right')
            destination = (x + 1, y)
            if destination in rocks_locations:
                print('in rocks')
                return ((x, y), tuple(coin_location), tuple(rocks_locations))
            if GameEnvironment.is_inbounds(self, destination):
                print('aaaa')
                if (x, y) in coin_location:
                    coin_location.remove((x, y))
                return (destination, tuple(coin_location), tuple(rocks_locations))
        elif action == 'up':
            print('up')
            destination = (x, y + 1 )
            if destination in rocks_locations:
                print('in rocks')
                return (x, y), tuple(coin_location), tuple(rocks_locations)
            if GameEnvironment.is_inbounds(self, destination):
                print('mmmmm')
                if (x, y) in coin_location:
                    coin_location.remove((x, y))
                return (destination, tuple(coin_location), tuple(rocks_locations))
        elif action == 'down':
            print('down')
            destination = (x, y - 1)
            if destination in rocks_locations:
                print('in rocks')
                return (x, y), tuple(coin_location), tuple(rocks_locations)
            if GameEnvironment.is_inbounds(self, destination):
                print('hhhhh')
                if (x, y) in coin_location:
                    coin_location.remove((x, y))
                return (destination, tuple(coin_location), tuple(rocks_locations))
        
    def goal_test(self, state):

        if state is None:
            print("State is None in goal_test")
            return False  # Invalid state, not a goal
        
        print('goal state', state)
        self.state = state
        (x, y), coin_location, rocks_locations= state
        print('coin location', coin_location)
        
        return len(coin_location) == 0

    
    def step_cost(self, action):
        if action == 'left' or  action == 'right':
            return 5
        if action == 'up':
            return 1
        if action == 'down':
            return 2 
        
def get_inital_state_from_env(env):
    agent_location = None
    coin_location = set()
    rocks_locations = set()

    for thing in env.things:
        if isinstance(thing, Coin):
            coin_location.add(thing.location)
        elif isinstance(thing, Rock):
            rocks_locations.add(thing.location)
        elif isinstance(thing, Agent):
            agent_location = thing.location

    return(agent_location, tuple(coin_location), tuple(rocks_locations))
    
if __name__ == '__main__':
    agent = RandomAgent()
    coin = Coin()
    rock = Rock()

    env = SearchEnvironment(width=8, height=8)
    env.add_thing(agent, (0, 0))
    env.add_thing(coin, env.random_location_inbounds())
    env.add_thing(rock, env.random_location_inbounds())


    initial_state = get_inital_state_from_env(env)
    print("Initial state:", initial_state)  # For debugging
    
    coin_problem = CoinProblem(initial_state, env.width, env.height)

    goal_node = depth_first_graph_search(coin_problem)

    if goal_node:
        print("Solution found!")
        print("Solution steps:", goal_node.solution())
        print("Path to solution:", [node.state for node in goal_node.path()])
        print("Total cost:", goal_node.path_cost)
else:
    print("No solution found.")