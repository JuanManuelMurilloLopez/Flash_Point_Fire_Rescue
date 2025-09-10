import numpy as np
from mesa import Agent, Model
from collections import deque
from Utils.PriorityQueu import PriorityQueue

INFINITE = 1_000_000


class Firefighter(Agent):
    def __init__(self, model, strategy, id):
        super().__init__(model)
        self.maxActionPoints = 8
        self.actionPoints = 4
        self.carryingVictim = False
        self.knockedDown = False
        self.strategy = strategy
        self.selectedStrategy = None
        self.id = id
        self.actions = []

    def step(self):

        self.outOfBuilding()
        self.actions = []

        if self.strategy == "random":
            self.randomStrategy()
        else:
            self.intelligentStrategy()

        self.actionPoints = min(self.actionPoints + 4, self.maxActionPoints)

    def outOfBuilding(self):
        x, y = self.pos

        if (x == 0 or x == self.model.width - 1) and (
            y == 0 or y == self.model.height - 1
        ):
            self.chooseEntry()

    def randomStrategy(self):
        while self.actionPoints > 0:
            # Movimiento aleatorio a una celda vecina
            possiblePositions = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False
            )

            if len(possiblePositions):
                options = np.random.permutation(len(possiblePositions))
                for i in options:
                    if self.move(possiblePositions[i]):
                        break

    def intelligentStrategy(self):
        if self.selectedStrategy == None:
            if self.carryingVictim:
                self.__getOut()
            else:
                self.searchForPOIs()
        self.useStrategy()

    # Handle player movement accounting for walls, doors, and AP spenditure
    def move(self, pos):
        # Failsafe
        if self.pos == pos:
            return True

        if (
            self.pos in self.model.entrances
            and self.actionPoints >= 2
            and self.carryingVictim
        ):
            self.__saveVictim()
            return True

        # No other player in next cell
        if self.model.grid.is_cell_empty(pos):
            x, y = self.pos
            direction = self.__moveDirection(self.pos, pos)

            # Open door in path
            if self.model.cells[y][x].doors[direction]:
                self.openCloseDoor()

            # Destroy wall to walk through
            elif self.model.cells[y][x].walls[direction]:
                self.chopWall(direction)

            elif self.model.fires[y][x]:
                self.extinguishFire(pos)

            # Calculate required AP to walk based if carrying a victim
            requiredAP = (lambda self: 2 if self.carryingVictim else 1)(self)
            if self.actionPoints >= requiredAP:
                self.model.grid.move_agent(self, pos)
                self.pos = pos
                self.actionPoints -= requiredAP
                # Revisar si se necesita alguna interacción al moverse
                self.checkPOI()
                self.checkFire()
                self.actions.append({"action": "move", "data": {"x": x, "y": y}})
            return True

        return False

    # TODO: Account and react to fire
    # Move until player runs out of AP or finishes its current strategy, thus
    # getting a new one
    def useStrategy(self):
        while self.actionPoints > 0:
            strategy = self.selectedStrategy
            # print(self.id, ": ", self.actionPoints, strategy)

            if strategy == None:
                return
            # Check if player has finished strategy
            if len(strategy) <= 1:
                if self.carryingVictim:
                    self.__getOut()
                else:
                    self.searchForPOIs()

            # Finish turn if player finishes strategy
            if len(strategy) == 0:
                self.selectedStrategy = None
                return

            step = strategy[0]
            if self.move(step):
                self.selectedStrategy = strategy[1:]
            else:
                break

    # Search for the closes POI relative to player's current position and
    # create a strategy to get to it
    def searchForPOIs(self):
        poiPosition = self.selectPOI()
        # Return if there is no more POIs in map not selected
        if not poiPosition:
            self.selectedStrategy = self.__strategyExtinguishFires()
            return

        safeStrategy = self.safeRoute(poiPosition)
        quickStrategy = self.quickRoute(poiPosition)

        # safeDistance, safeRoute = safeStrategy
        # quickDistance, quickRoute, quickDamage = quickStrategy

        # Select quickes strategy accounting for damage heuristic
        _strategy, self.selectedStrategy = self.chooseStrategy(
            safeStrategy, quickStrategy
        )
        return self.selectedStrategy

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
                print("Found a Victim at ", (x, y), "!")
            # Si el POI era una falsa alarma, la eliminamos
            elif poiAtPos.victim == 0:
                self.model.POIs[self.pos] = 0
                print("It was not a victim :(")
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
    def extinguishFire(self, position):

        # Rescatamos el fuego en la posición
        # fireAtPos = [f for f in self.model.fires if f.pos == position]
        fire = self.model.fires[position]

        # Si no hay fuego no hacemos nada
        if fire == 0:
            return

        action = ""
        # Procedimiento dependiendo de la acción, quitamos action points y eliminamos o modificamos el fuego
        if fire.state == "fire" and self.actionPoints >= 2:
            self.model.fires[position] = 0
            self.actionPoints -= 2
            action = "removeFire"
        elif fire.state == "smoke" and self.actionPoints >= 1:
            self.model.fires[position] = 0
            self.actionPoints -= 1
            action = "removeSmoke"

        if action:
            x, y = position
            self.actions.append({"action": action, "data": {"x": x, "y": y}})

    # Cambia el estado de la puerta (Si no está destruida)
    def openCloseDoor(self):
        if self.actionPoints >= 1:
            x, y = self.pos
            cell = self.model.cells[y][x]
            if cell.hasDoor():
                cell.changeDoorStatus()
                self.actions.append({"action": "openDoor", "data": {"x": x, "y": y}})
                self.actionPoints -= 1
        else:
            return

    def chopWall(self, orientation):
        # Colocar daño en la pared para abrir camino (2 AP por daño, cuando la pared tiene 2 de daño se destruye)
        if self.actionPoints >= 1:
            x, y = self.pos
            # Obtenemos la celda
            cell = self.model.cells[y][x]
            # Obtenemos la pared
            wall = cell.walls[orientation]
            # Verificamos que no esté destruida o destruimos
            while not wall.isDestroyed():
                # Añadimos el daño a la pared
                wall.addDamage()
                # Agregamos el daño al contador del modelo
                self.model.damageTokens += 1

                # Revisamos si existía una puerta en esa pared
                door = cell.doors[orientation]
                if door:
                    door.destroy()
                self.actions.append({"action": "chopWall", "data": {"x": x, "y": y}})

                self.actionPoints -= 1

    # Heuristic function to decide which strategy to use
    def chooseStrategy(self, safeStrategy, quickStrategy):
        safeDistance, safeRoute = safeStrategy
        quickDistance, quickRoute, quickDamage = quickStrategy

        if (
            safeDistance * 0.8 > quickDistance
            and quickDamage + self.model.damageTokens < 24 / 2
        ):
            return "Quick", quickRoute

        return "Safe", safeRoute

    def chooseEntry(self):
        entrances = list(self.model.entrances)
        option = np.random.permutation(len(entrances))
        for i in option:
            if self.model.grid.is_cell_empty(entrances[i]):
                self.model.grid.move_agent(self, entrances[i])
                break

    # Selecciona el primer POI disponible desde la entrada que no haya elegido
    # otro agente
    def selectPOI(self):
        cells = self.model.POIs

        POIfound = False

        queue = deque()
        queue.append(self.pos)
        visited = set({self.pos})

        while not POIfound:
            if not queue:
                return False

            path = queue.popleft()
            x, y = path

            if cells[y][x] and (x, y) not in self.model.POIsFound:
                POIfound = True
                self.model.POIsFound.add((x, y))
                return (x, y)

            neighbors = self.model.search(x, y)

            for nX, nY in neighbors:
                if (nX, nY) not in visited and self.__isValid(cells, (nX, nY)):
                    visited.add((nX, nY))
                    queue.append((nX, nY))

    def selectExit(self):
        # print("Select Exit")
        cells = self.model.cells

        exitFound = False

        queue = deque()
        queue.append(self.pos)
        visited = set()

        while not exitFound:
            if not queue:
                print("False", queue)
                return False, visited

            cell = queue.popleft()
            x, y = cell
            print(x, y)

            if (x, y) in self.model.entrances:
                exitFound = True
                return True, (x, y)

            if not (x, y) in visited:
                print("No visitado", (x, y))
                visited.add((x, y))

                neighbors = self.model.grid.get_neighborhood(
                    (x, y), moore=False, include_center=False
                )
                for nX, nY in neighbors:
                    if self.__isValid(cells, (nX, nY)):
                        queue.append((nX, nY))
                print(visited, queue)

    def selectFire(self):
        cells = self.model.fires

        fireFound = False

        queue = deque()
        queue.append(self.pos)
        visited = set({self.pos})

        while not fireFound:
            if not queue:
                return False

            path = queue.popleft()
            x, y = path

            if cells[y][x]:
                fireFound = True
                return (x, y)

            neighbors = self.model.search(x, y)

            for nX, nY in neighbors:
                if (nX, nY) not in visited and self.__isValid(cells, (nX, nY)):
                    visited.add((nX, nY))
                    queue.append((nX, nY))

        return False

    def safeRoute(self, destination):
        if not destination:
            raise Exception(f"There is no destination: {destination}")

        n = (self.model.width + 2) * (self.model.height + 2)
        dist = [INFINITE] * n
        prev = [None] * n
        dist[self.__toInt(self.pos)] = 1

        pq = PriorityQueue()

        pq.push(0, self.pos)

        while not pq.empty():
            _, currentPos = pq.top()
            pq.pop()

            if currentPos == destination:
                break

            # Costo acumulativo de la celda actual y moverse a la siguiente
            # celda
            x, y = currentPos
            cell = self.model.cells[y][x]

            for neighborPos in self.model.getNeighbors(x, y):
                newDistance = dist[self.__toInt(currentPos)] + 1
                direction = self.__moveDirection(currentPos, neighborPos)

                if newDistance < dist[self.__toInt(neighborPos)]:
                    if cell.doors[direction] and not cell.doors[direction].isOpen():
                        newDistance += 1

                    dist[self.__toInt(neighborPos)] = newDistance
                    prev[self.__toInt(neighborPos)] = currentPos
                    priority = newDistance + self.__heuristics(
                        (neighborPos), destination
                    )

                    pq.push(priority, (neighborPos))

        path = []
        u = destination

        while u is not None:
            path.insert(0, u)
            u = prev[self.__toInt(u)]

        if self.carryingVictim:
            x, y = destination

            if x - 1 == 0:
                path.append((0, y))
            elif x + 1 == self.model.width - 1:
                path.append((self.model.width - 1, y))
            elif y - 1 == 0:
                path.append((x, 0))
            elif y + 1 == self.model.height - 1:
                path.append((x, self.model.height - 1))

        return dist[self.__toInt(destination)], path

    def quickRoute(self, destination):
        if not destination:
            raise Exception(f"There is no destination: {destination}")
        n = (self.model.width + 2) * (self.model.height + 2)
        dist = [INFINITE] * n
        prev = [None] * n
        dist[self.__toInt(self.pos)] = 1
        cells = self.model.cells
        damage = 0

        pq = PriorityQueue()

        pq.push(0, self.pos)

        while not pq.empty():
            _, currentPos = pq.top()
            pq.pop()

            if currentPos == destination:
                break

            # Costo acumulativo de la celda actual y moverse a la siguiente
            # celda
            x, y = currentPos
            cell = self.model.cells[y][x]
            for neighborPos in self.__getAllNeighborhood(cells, (currentPos)):
                newDistance = dist[self.__toInt(currentPos)] + 1
                direction = self.__moveDirection(currentPos, neighborPos)
                if newDistance < dist[self.__toInt(neighborPos)]:
                    if cell.doors[direction] and not cell.doors[direction].isOpen():
                        newDistance += 1
                    elif cell.walls[direction]:
                        newDistance += 4 - cell.walls[direction].damage

                    dist[self.__toInt(neighborPos)] = newDistance
                    prev[self.__toInt(neighborPos)] = currentPos
                    priority = newDistance + self.__heuristics(
                        (neighborPos), destination
                    )
                    pq.push(priority, (neighborPos))

        path = []
        currentPos = destination

        cell = None
        while currentPos is not None:
            path.insert(0, currentPos)
            nextPos = prev[self.__toInt(currentPos)]
            if nextPos:
                direction = self.__moveDirection(currentPos, nextPos)
                x, y = currentPos
                cell = self.model.cells[y][x]
                if cell.walls[direction] and not cell.doors[direction]:
                    damage += 2

            currentPos = nextPos

        return dist[self.__toInt(destination)], path, damage

    def __toInt(self, pos):
        x, y = pos
        return x * (self.model.height + 2) + y

    def __heuristics(_self, src, dest):
        sX, sY = src
        try:
            dX, dY = dest
        except:
            raise Exception("Error en heuristica", dest)
        return (abs(sX - dX) + abs(sY - dY)) * 5

    def __isValid(self, matrix, position):
        (row, col) = position
        rows = len(matrix[0])
        cols = len(matrix)
        return 0 <= row < rows and 0 <= col < cols

    def __getAllNeighborhood(self, matrix, position):
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

    def __moveDirection(_self, currentPos, nextPos):
        x1, y1 = currentPos
        x2, y2 = nextPos

        # Up
        if x1 == x2 and y1 < y2:
            return "up"
        elif x1 == x2 and y1 > y2:
            return "down"
        # Horizontal
        elif y1 == y2 and x1 < x2:
            return "right"
        else:
            return "left"

    def __getOut(self):
        found, exitPos = self.selectExit()
        if not found:
            raise Exception(exitPos)
        _distance, self.selectedStrategy = self.safeRoute(exitPos)
        return self.selectedStrategy

    def __strategyExtinguishFires(self):
        firePos = self.selectFire()
        if not firePos:
            return None
        #     raise Exception("No fire found")
        _distance, strategy = self.safeRoute(firePos)
        return strategy

    def __saveVictim(self):
        self.actionPoints -= 2
        self.model.victimsRescued += 1
        print("Victim Saved: ", self.model.victimsRescued)
        self.carryingVictim = False
        options = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
        for i in options:
            if self.model.grid.is_cell_empty(i):
                self.model.grid.move_agent(self, i)
                return
