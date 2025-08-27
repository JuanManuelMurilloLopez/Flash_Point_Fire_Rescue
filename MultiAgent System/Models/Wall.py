
class Wall:
    def __init__(self):
        self.damage = 0

    def addDamage(self):
        if self.damage < 2:
            self.damage += 1
    
    def isDestroyed(self):
        return self.damage == 2
    