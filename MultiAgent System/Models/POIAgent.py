from mesa import Agent, Model

class POIAgent(Agent):
    
    def __init__(self, model, position, victim):
        super().__init__(model)
        self.pos = position
        self.rescued = False
        self.revealed = False
        self.lost = False
        self.victim = victim

    def reveal(self):
        self.revealed = True
        if not self.victim:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def rescue(self):
        if self.victim and not self.rescued:
            self.rescued = True
            self.model.victimsRescued += 1
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def lose(self):
        if self.victim and not self.rescued:
            self.lost = True
            self.model.victimsLost += 1
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

