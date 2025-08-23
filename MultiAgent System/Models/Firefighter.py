from mesa import Agent, Model

class Firefighter(Agent):
    
    def __init__(self, model):
        super().__init__(model)
        self.action_points = 0
        self.carryingVictim = False
        self.knockedDown = False

    def move(self):
        return
    
    def step(self):
        return
    
    def openCloseDoor(self):
        return
    
    def extinguish(self):
        return
    
    def chop(self):
        return
