class POI():
    def __init__(self, x, y, victim):
        self.position = [x, y]
        # True -> Victim, False -> False Alarm
        self.victim = victim
        self.rescued = False
        self.lost = False
