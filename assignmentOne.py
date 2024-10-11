import agents
import random

class GameEnvironment(agents.Environment):
    """2_D environment"""
    def __init__(self, width=8,height=8):
        super().__init__()
        self.width = width
        self.height = height
        self.observers = []
        self.x_start, self.y_start = (0,0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
        self.totalCoinsAvailable = 0
        self.add_coins()
        self.add_Rock()
        self.add_walls()

    def thing_classes(self):
        return [agents.Wall, Rock, Coin, tableBasedAgent]

    def percept(self, agent):   
        return agent.location
       
    def execute_action(self, agent, action):
        agent.bump = False
        #chat
        if action == 'left':
            destination = (agent.location[0] - 1, agent.location[1])
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                #agent.performance += 1
                print(f"Moved left to {agent.location}")
        elif action == 'right':
            destination = (agent.location[0] + 1, agent.location[1])
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                #agent.performance += 1
                print(f"Moved right to {agent.location}")
        elif action == 'up':
            destination = (agent.location[0], agent.location[1] + 1)
            agent.bump = self.move_to(agent, destination)
            if agent.bump == True:
                agent.location = destination
                #agent.performance += 1
                print(f"Moved up to {agent.location}")
        elif action == 'down':
            destination = (agent.location[0], agent.location[1] - 1)
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
            #print(agents.Environment.list_things_at())
            self.delete_thing(thing)
            self.totalCoinsAvailable -= 1
            thing.performance += 1
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

        for y in range(1, self.height - 1):
            self.add_thing(agents.Wall(), (0, y))
            self.add_thing(agents.Wall(), (self.width - 1, y))

    def add_coins(self):
            self.add_thing(Coin(), self.random_location_inbounds())  
            self.add_thing(Coin(), self.random_location_inbounds())  
            self.add_thing(Coin(), self.random_location_inbounds())  
            self.add_thing(Coin(), self.random_location_inbounds())  
            self.totalCoinsAvailable += 4

    def add_Rock(self):
            self.add_thing(Rock(), self.random_location_inbounds())
            self.add_thing(Rock(), self.random_location_inbounds())

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def default_location(self, thing):
        location = (self.random_location_inbounds())
        while self.some_things_at(location, Rock) or self.some_things_at(location, Coin):
            # we will find a random location with no obstacles
            location = self.random_location_inbounds()
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

  
class Rock(agents.Obstacle):
    pass

class Coin(agents.Thing):
    pass

def tableBasedAgent():
    #total moves from table equals 20 moves
    table = {
        ((3, 3), ): 'right',
        ((3, 3), (3, 4),): 'right',
        ((0, 0), (1, 0), (2, 0), ): 'up',
        ((0, 0), (1, 0), (2, 0), (2, 1), ): 'up'
    }
    return agents.Agent(agents.TableDrivenAgentProgram(table))


def RandomReflexAgent():
    pass

def ModelAgent():
    pass

environment = GameEnvironment
agentsList = [tableBasedAgent]
result = agents.compare_agents(environment, agentsList, n=20, steps=20)

performance_tableBasedAgent = result[0][1]

print("performance of GameEnvironment", performance_tableBasedAgent)