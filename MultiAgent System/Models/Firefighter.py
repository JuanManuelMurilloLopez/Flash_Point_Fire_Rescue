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

    def checkPOI(self):
        # Revisar si hay un POI en la posición del firefighter
        for poi in self.model.POIs:
            if self.pos[0] == poi[0] and self.pos[1] == poi[1]:
                if poi[2] == 1:
                    # Victima encontrada
                    self.carryingVictim = True
                    # TODO: implementar ruta a la salida
                elif poi[2] == 0:
                    # Falsa alarma
                    # TODO: quitar POI del tablero
                    return


    def checkFire(self):
        # Si la casilla en la que está tiene fuego, apagarlo (siguiendo las reglas del juego)
        agentsInCell = self.model.grid.get_cell_list_contents([self.pos])

        for agent in agentsInCell:
            if isinstance(agent, Fire):
                if agent.state == "fire":
                    self.knockedDown = True
                    self.model.moveToAmbulance(self)
                elif agent.state == "smoke":
                    # TODO: Lógica para elegir aleatoreamente si se apaga o no
                    pass

        if self.pos in self.model.fireLocations:
            # TODO: Implementar apagar fuego
            pass

    def openCloseDoor(self, cell):
        # Abrir o cerrar puerta en la celda indicada (1 action point)
        if self.actionPoints >= 1:
            # TODO: Añadir lógica para modificar el estado de la puerta
            self.actionPoints -= 1

    # action -> "removeFire", "removeSmoke", "flipFire"
    def extinguishFire(self, cell, action):
        # Apagar fuego en la celda indicada (1 AP para humo, 2 AP para fuego)
        agents = self.model.grid.get_cell_list_contents([cell])
        for agent in agents:
            if isinstance(agent, Fire):
                if agent.state == "smoke" and self.actionPoints >= 1 and action == "removeSmoke":
                    agent.extinguish()
                    self.actionPoints -= 1
                elif agent.state == "fire" and self.actionPoints >= 2 and action == "removeFire":
                    agent.extinguish()
                    self.actionPoints -= 1
                elif agent.state == "fire" and self.actionPoints >= 1 and action == "flipFire":
                    agent.smoke()
                    self.actionPoints -= 1

    def saveVictim(self, cell):
        # Llevar a la víctima afuera, 2 AP
        # TODO: Lógica para llevar la víctima a la salida
        pass

    def chopWall(self, cell):
        # Colocar daño en la pared para abrir camino (2 AP por daño, cuando la pared tiene 2 de daño se destruye)
        if self.actionPoints >= 2:
            # TODO: Lógica para el daño a la pared
            self.actionPoints -= 2