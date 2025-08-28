from mesa import Agent, Model

class Fire(Agent):
    
    def __init__(self, position, state = "smoke"):
        self.pos = position
        self.state = state

    def fire(self):
        if self.state == "smoke":
            self.state = "fire"

    def smoke(self):
        if self.state == "fire":
            self.state = "smoke"


