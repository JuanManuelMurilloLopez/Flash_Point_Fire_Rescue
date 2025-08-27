class Door:
    def __init__(self, x1, y1, x2, y2):
        self.cell1 = [x1, y1]
        self.cell2 = [x2, y2]
        self.state = "closed"

    def open(self):
        if self.state == "closed":
            self.state = "open"

    def close(self):
        if self.state == "open":
            self.state = "closed"

    def destroy(self):
        self.state = "destroyed"