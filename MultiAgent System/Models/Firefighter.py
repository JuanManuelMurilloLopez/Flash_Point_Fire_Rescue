import numpy as np
from mesa import Agent, Model

class Firefighter(Agent):
    def __init__(self, model, initialPos):
        super().__init__(model)
        self.pos = initialPos
        self.actionPoints = 4
        self.carryingVictim = False
        self.knockedDown = False

    # TODO: Terminar lógica del step
    def step(self):
        while self.actionPoints > 0:
            self.move()
            self.actionPoints -= 1

        self.actionPoints += 4

    # TODO: Cambiar la lógica del checkFire acorde a la nueva implementación
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
        #poiAtPos = [p for p in self.model.POIs if p.pos == self.pos]
        poiAtPos = self.model.POIs[self.pos]

        if poiAtPos != 0:
            poiAtPos.reveal()
            # Si el POI es una víctima, la recuperamos
            if poiAtPos.victim == 1:
                self.carryingVictim = True
            # Si el POI era una falsa alarma, la eliminamos
            elif poiAtPos.victim == 0:
                self.model.POIs[self.pos] = 0
                self.model.activePois -= 1

    # Revisar si en la posición dada hay fuego
    def checkFire(self, position, fireState):
        # Revisar si hay fuego en la posición del bombero
        #fireAtPos = [f for f in self.model.fires if f.pos == position and f.state == fireState]
        fireAtPos = self.model.POIs[position]

        if fireAtPos != 0:
            if fireAtPos.state == fireState:
                return True
        else:
            return False

    # action -> "removeFire", "removeSmoke", "flipFire"
    # Apagar el fuego en la posición indicada
    def extinguishFire(self, position, action):

        # Rescatamos el fuego en la posición
        #fireAtPos = [f for f in self.model.fires if f.pos == position]
        fire = self.model.POIs[position]

        # Si no hay fuego no hacemos nada
        if fire == 0:
            return

        # Procedimiento dependiendo de la acción, quitamos action points y eliminamos o modificamos el fuego
        if fire.state == "smoke" and self.actionPoints >= 1 and action == "removeSmoke":
            self.model.POIs[position] = 0
            self.actionPoints -= 1
        elif fire.state == "fire" and self.actionPoints >= 2 and action == "removeFire":
            self.model.POIs[position] = 0
            self.actionPoints -= 2
        elif fire.state == "fire" and self.actionPoints >= 1 and action == "flipFire":
            fire.smoke()
            self.actionPoints -= 1

    # Cambia el estado de la puerta (Si no está destruida)
    def openCloseDoor(self):
        if self.actionPoints >= 1:
            cell = self.model.cells[self.pos]
            if cell.hasDoor():
                cell.changeDoorStatus()
                self.actionPoints -= 1
        else:
            return

    def saveVictim(self):
        # TODO: Lógica para llevar la víctima a la salida
        pass

    def chopWall(self, orientation):
        # Colocar daño en la pared para abrir camino (2 AP por daño, cuando la pared tiene 2 de daño se destruye)
        if self.actionPoints >= 2:

            # Obtenemos la celda
            cell = self.model.cells[self.pos]
            # Obtenemos la pared
            wall = cell.walls[orientation]

            # Verificamos que no esté destruida
            if wall.isDestroyed():
                return
            
            # Añadimos el daño a la pared
            wall.addDamage()
            # Agregamos el daño al contador del modelo
            self.model.damageTokens += 1

            # Revisamos si existía una puerta en esa pared
            door = cell.doors[orientation]
            if door:
                door.destroy()

            self.actionPoints -= 2
            