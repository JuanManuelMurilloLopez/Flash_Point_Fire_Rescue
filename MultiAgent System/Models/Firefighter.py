import numpy as np
from mesa import Agent, Model

from Fire import Fire

class Firefighter(Agent):
    def __init__(self, model, initialPos):
        super().__init__(model)
        self.pos = initialPos
        self.actionPoints = 4
        self.carryingVictim = False
        self.knockedDown = False

    def step(self):
        while self.actionPoints > 0:
            self.move()
            self.actionPoints -= 1

        self.actionPoints += 4

    def move(self):
        # Movimiento aleatorio a una celda vecina
        possiblePositions = self.model.grid.get_neighborhood(self.pos, moore = False, include_center = False)
        options = np.random.permutation(len(possiblePositions))
        if options:
            newPos = options[0]
            self.model.grid.move_agent(self, newPos)
            self.pos = newPos
            # Revisar si se necesita alguna interacción al moverse
            self.checkPOI()
            self.checkFire()

    # Revisar si en la posición del bombero hay un POI
    def checkPOI(self):
        # Revisar si hay un POI en la posición del bombero
        poiAtPos = [p for p in self.model.POIs if p.pos == self.pos]

        if poiAtPos:
            poiAtPos[0].reveal()
            # Si el POI es una víctima, la recuperamos
            if poiAtPos[0].victim == 1:
                self.carryingVictim = True
            # Si el POI era una falsa alarma, la eliminamos
            elif poiAtPos[0].victim == 0:
                self.model.POIs.remove(poiAtPos[0])

    # Revisar si en la posición dada hay fuego
    def checkFire(self, position, fireState):
        # Revisar si hay fuego en la posición del bombero
        fireAtPos = [f for f in self.model.fires if f.pos == position and f.state == fireState]

        if fireAtPos:
            return True
        else:
            return False

    # action -> "removeFire", "removeSmoke", "flipFire"
    # Apagar el fuego en la posición indicada
    def extinguishFire(self, position, action):

        # Rescatamos el fuego en la posición
        fireAtPos = [f for f in self.model.fires if f.pos == position]

        ### TERMINAR ESTO

        # Si no hay fuego no hacemos nada
        if not fireAtPos:
            return

        # Si hay fuego lo guardamos
        fire = fireAtPos[0]

        # Procedimiento dependiendo de la acción, quitamos action points y eliminamos o modificamos el fuego
        if fire.state == "smoke" and self.actionPoints >= 1 and action == "removeSmoke":
            self.model.fires.remove(fire)
            self.actionPoints -= 1
        elif fire.state == "fire" and self.actionPoints >= 2 and action == "removeFire":
            self.model.fires.remove(fire)
            self.actionPoints -= 2
        elif fire.state == "fire" and self.actionPoints >= 1 and action == "flipFire":
            fire.smoke()
            self.actionPoints -= 1

    def openCloseDoor(self, cell):
        # Abrir o cerrar puerta en la celda indicada (1 action point)
        if self.actionPoints >= 1:
            # TODO: Añadir lógica para modificar el estado de la puerta
            self.actionPoints -= 1

    def saveVictim(self, cell):
        # Llevar a la víctima afuera, 2 AP
        # TODO: Lógica para llevar la víctima a la salida
        pass

    def chopWall(self, cell, orientation):
        # Colocar daño en la pared para abrir camino (2 AP por daño, cuando la pared tiene 2 de daño se destruye)
        if self.actionPoints >= 2:
            # TODO: Lógica para el daño a la pared
            self.actionPoints -= 2