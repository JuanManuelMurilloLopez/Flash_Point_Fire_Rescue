from Door import Door
from Wall import Wall

class Cell:
    def __init__(self, pos, wallLayout, doorLocations):
        self.pos = pos
        self.isAccessPoint = False
        self.walls = {"up": None, "right": None, "down": None, "left": None}
        self.doors = {"up": None, "right": None, "down": None, "left": None}

        # Añadir las paredes a la celda
        if wallLayout[0] == 1:
            wall = Wall()
            self.walls["up"] = wall
        if wallLayout[1] == 1:
            wall = Wall()
            self.walls["right"] = wall
        if wallLayout[2] == 1:
            wall = Wall()
            self.walls["down"] = wall
        if wallLayout[3] == 1:
            wall = Wall()
            self.walls["left"] = wall

        # Añadir las puertas a la celda
        for doorL in doorLocations:
            x1, y1, x2, y2, = doorL

            if self.pos == [x1, y1]:
                door = Door(x1, y1, x2, y2)
                if x1 == x2 and y1 + 1 == y2:
                    self.doors["up"] = door
                elif x1 == x2 and y1 - 1 == y2:
                    self.doors["down"] = door
                elif x1 + 1 == x2 and y1 == y2:
                    self.doors["right"] = door
                elif x1 - 1 == x2 and y1 == y2:
                    self.doors["left"] = door

            elif self.pos == [x2, y2]:
                door = Door(x2, y2, x1, y1)
                if x1 == x2 and y1 == y2 + 1:
                    self.doors["up"] = door
                elif x1 == x2 and y1 == y2 - 1:
                    self.doors["down"] = door
                elif x1 == x2 + 1 and y1 == y2:
                    self.doors["right"] = door
                elif x1 == x2 - 1 and y1 == y2:
                    self.doors["left"] = door

    # Regresa si hay una puerta en la celda (las destruidas no cuentan)
    def hasDoor(self):
        doors = any(door is not None for door in self.doors.values())
        if doors:
            door = [door for door in self.doors.values() if door is not None][0]

            if door.state == "destroyed":
                return False
            else:
                return True
        else:
            return False
    
    # Modifica el estado de la puerta
    def changeDoorStatus(self):
        door = [door for door in self.doors.values() if door is not None][0]

        if door.state == "open":
            door.close()
        if door.state == "closed":
            door.open()
