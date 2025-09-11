
class Poi():
    
    def __init__(self, position, victim):
        self.pos = position
        self.rescued = False
        self.revealed = False
        self.lost = False
        self.victim = victim
        self.state = "alive" if victim else "fake"


    def reveal(self):
        self.revealed = True

    def rescue(self):
        if self.victim and not self.rescued:
            self.rescued = True
            self.state = "rescued" 

    def lose(self):
        if self.victim and not self.rescued:
            self.lost = True
            self.state = "dead" 

