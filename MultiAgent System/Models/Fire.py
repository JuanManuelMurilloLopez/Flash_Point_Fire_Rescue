from mesa import Agent, Model

class Fire(Agent):
    
    def __init__(self, model, position, state = "smoke"):
        super().__init__(model)
        self.pos = position
        self.state = state

    def fire(self):
        if self.state == "smoke":
            self.state = "fire"

    def extinguish(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def smoke(self):
        if self.state == "fire":
            self.state = "smoke"


