import numpy as np
from mesa import Agent, Model
from collections import deque
from Utils.PriorityQueu import PriorityQueue


class Firefighter(Agent):
    def __init__(self, model, initialPos):
        super().__init__(model)
        self.maxActionPoints = 8
        self.actionPoints = 4
        self.carryingVictim = False
        self.knockedDown = False

    # TODO: Terminar lógica del step
    def step(self):
        while self.actionPoints > 0:
            self.move()

            self.actionPoints -= 1

        self.actionPoints = min(self.actionPoints + 4, self.maxActionPoints)

    # TODO: Cambiar la lógica del checkFire acorde a la nueva implementación
    def move(self):
        # Movimiento aleatorio a una celda vecina
        possiblePositions = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )

        if len(possiblePositions):
            options = np.random.permutation(len(possiblePositions))
            for i in options:
                if self.model.grid.is_cell_empty(possiblePositions[i]):
                    newPos = possiblePositions[i]
                    self.model.grid.move_agent(self, newPos)
                    self.pos = newPos
                    # Revisar si se necesita alguna interacción al moverse
                    self.checkPOI()
                    self.checkFire()
                    break

    # Revisar si en la posición del bombero hay un POI
    def checkPOI(self):
        # Revisar si hay un POI en la posición del bombero
        # poiAtPos = [p for p in self.model.POIs if p.pos == self.pos]
        x, y = self.pos
        poiAtPos = self.model.POIs[y][x]

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
    def checkFire(self):
        # Revisar si hay fuego en la posición del bombero
        # fireAtPos = [f for f in self.model.fires if f.pos == position and f.state == fireState]
        x, y = self.pos
        fireAtPos = self.model.fires[y][x]

        if fireAtPos != 0:
            if fireAtPos.state == "fire":
                return True
        else:
            return False

    # action -> "removeFire", "removeSmoke", "flipFire"
    # Apagar el fuego en la posición indicada
    def extinguishFire(self, position, action):

        # Rescatamos el fuego en la posición
        # fireAtPos = [f for f in self.model.fires if f.pos == position]
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

    def searchForPOIs(self):
        self.chooseEntry()
        poiPosition = self.selectPOI()
        safeDistance, safeRoute = self.safeRoute(poiPosition)
        quickDistance, quickRoute = self.shortRoute(poiPosition)

        print(safeDistance, safeRoute)
        print(quickDistance, quickRoute)
        # if quickDistance >= safeDistance / 3:
        #     damage = self.damage(quickRoute)
        #     if self.model.damageTokens + damage <= 12:
        #         self.strategy = quickRoute
        #         return

        # self.strategy = safeRoute

    def chooseEntry(self):
        entrance = np.random.randint(len(self.model.entrances))
        self.model.grid.move_agent(self.model.entrances[entrance])

    # A* para conseguir la ruta más corta al POI más cercano por el camino abierto
    def selectPOI(self):
        cells = self.model.cells

        POIfound = False

        queue = deque()
        queue.append(self.pos)
        visited = set(self.pos)

        while not POIfound:
            path = queue.popleft()
            x, y = path[-1]

            if cells[x][y].poi and (x, y) not in self.model.POIsFound:
                POIfound = True
                self.model.POIsFound.add((x, y))
                return (x, y)

            neighbors = self.model.getNeighbors(x, y)

            for nX, nY in neighbors:
                if (nX, nY) not in visited:
                    visited.add((nX, nY))
                    queue.append(path + [(nX, nY)])

    def heuristics(src, dest):
        return (abs(src[0] - dest[0]) + abs(src[0] - dest[0])) * 5

    def safeRoute(self, destination):
        n = self.model.width * self.model.height
        dist = np.zeros(n)
        dist[self.toInt(x, y)] = 0
        prev = [None] * n

        pq = PriorityQueue()

        pq.push(0, self.pos)
        x, y = self.pos

        while not pq.empty():
            _, u = pq.top()
            pq.pop()

            if u == destination:
                break

            for nX, nY in self.model.getNeighbors(u):
                newDistance = dist[self.__toInt(x, y)] + 1

                if newDistance < dist[self.__toInt(x, y)]:
                    dist[self.__toInt(nX, nY)] = newDistance
                    prev[self.__toInt(x, y)] = u
                    priority = newDistance + self.heuristics((nX, nY), destination)
                    pq.push(priority, (nX, nY))

        path = []
        u = destination
        x, y = destination
        if prev[self.__toInt(x, y)] is not None or u == self.destination:
            while u is not None:
                path.insert(0, u)
                u = prev[self.__toInt(x, y)]

        return dist[self.__toInt(x, y)], path

    def quickRoute(self, destination):
        n = self.model.width * self.model.height
        dist = np.zeros(n)
        dist[self.toInt(x, y)] = 0
        prev = [None] * n

        cells = self.model.cells

        pq = PriorityQueue()

        pq.push(0, self.pos)

        while not pq.empty():
            _, u = pq.top()
            pq.pop()

            x, y = u

            if u == destination:
                break

            for nX, nY in self.__getNeighborhood(cells, u):
                newDistance = dist[self.__toInt(x, y)] + cells[nX][nY]

                if newDistance < dist[self.__toInt(x, y)]:
                    dist[self.__toInt(nX, nY)] = newDistance
                    prev[self.__toInt(x, y)] = u
                    priority = newDistance + self.heuristics((nX, nY), destination)
                    pq.push(priority, (nX, nY))

        path = []
        u = destination
        x, y = destination
        if prev[self.__toInt(x, y)] is not None or u == self.destination:
            while u is not None:
                path.insert(0, u)
                u = prev[self.__toInt(x, y)]

        return dist[self.__toInt(x, y)], path

    def __toInt(self, x, y):
        return x * self.model.height + y

    def __isValid(matrix, position):
        (row, col) = position
        rows = len(matrix)
        cols = len(matrix[0])
        return 0 <= row < rows and 0 <= col < cols

    def __getNeighborhood(self, matrix, position):
        result = []

        (ren, col) = position

        new_position = ((ren - 1), col)
        if self.__isValid(matrix, new_position):
            result.append(new_position)

        new_position = ((ren + 1), col)
        if self.__isValid(matrix, new_position):
            result.append(new_position)

        new_position = (ren, (col - 1))
        if self.__isValid(matrix, new_position):
            result.append(new_position)

        new_position = (ren, (col + 1))
        if self.__isValid(matrix, new_position):
            result.append(new_position)

        return result
