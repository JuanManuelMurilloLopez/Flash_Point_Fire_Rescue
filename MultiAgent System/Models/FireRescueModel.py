from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run

from Utils.getGrid import getGrid
from Utils.BoardInitialConfig import boardConfig
from .Firefighter import Firefighter
from .Fire import Fire
from .Poi import Poi
from .Cell import Cell

import numpy as np
import random
from collections import deque


class FireRescueModel(Model):
    def __init__(
        self, width=8, height=6, noOfAagents=6, victimsMarkers=10, board=boardConfig
    ):
        super().__init__()

        # Medidas del grid del edificio
        self.width = width
        self.height = height

        # Nos indica en que ronda está el juego
        self.round = 0

        # Se le agregan 2 para añadir el exterior
        self.grid = SingleGrid(width + 2, height + 2, torus=False)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={
                "Grid": getGrid,
                "Steps": lambda model: model.round,
                "VictimsRescued": lambda model: model.victimsRescued,
                "VictimsLost": lambda model: model.victimsLost,
            },
            agent_reporters={},
        )

        # Variables para conocer el estatus del juego
        self.victimsRescued = 0
        self.victimsLost = 0
        self.damageTokens = 0

        # Número de POIs disponibles
        self.totalVictims = 10
        self.totalFalseAlarms = 5
        # Quitar los iniciales
        for x, y, value in board["POILocations"]:
            if value == 1:
                self.totalVictims -= 1
            else:
                self.totalFalseAlarms -= 1

        # Última tirada de dados
        self.dice = [0, 0]

        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                wallLayout = board["cells"][y][x]
                cell = Cell([x, y], wallLayout, board["doorLocations"])
                row.append(cell)
            self.cells.append(row)

        # Información del tablero
        self.board = board

        # TODO: Modificar la posición de la ambulancia a la correcta
        self.ambulancePos = board["ambulancePosition"]

        # Añadimos los POI iniciales
        self.activePois = 3
        self.POIs = np.zeros((height + 2, width + 2), dtype=object)
        for poiData in board["POILocations"]:
            # Creamos el POI en la posición indicada
            x, y = poiData[0], poiData[1]
            poi = Poi((x, y), poiData[2])
            self.POIs[x][y] = poi

        # Añadimos los POI iniciales
        """self.POIs = []
        for poiData in board["POILocations"]:
            # Creamos el agente en la posición indicada
            poi = Poi((poiData[0], poiData[1]), poiData[2])
            self.POIs.append(poi)
        """

        # Añadimos el fuego inicial
        self.fires = np.zeros((height + 2, width + 2), dtype=object)
        for pos in board["fireLocations"]:
            fire = Fire(pos, state="fire")
            self.fires[pos] = fire

        # Añadimos el fuego inicial
        """self.fires = []
        # Creamos el agente en la posición indicada
        for pos in board["fireLocations"]:
            fire = Fire(self, pos)
            self.fires.append(fire)
        """

        # Creación de los bomberos
        # possiblePositions = np.random.permutation(board["spawnPoints"])

        possiblePositions = []
        for i in range(width):
            possiblePositions.append([i, 0])
            possiblePositions.append([i, height])

        for i in range(height):
            possiblePositions.append([0, i])
            possiblePositions.append([width, i])

        # Añadir los Firefighters
        for i in range(noOfAagents):
            pos = possiblePositions[i]
            fireFighter = Firefighter(self, pos)
            self.grid.place_agent(fireFighter, pos)
            self.schedule.add(fireFighter)

    # Método utilizado para simular el tirado de dados
    def rollDice(self):
        self.dice = (random.randrange(self.width), random.randrange(self.height))

    # Método utilizado para avanzar el fuego en el tablero después de cada ronda
    def advanceFire(self):
        self.rollDice()

        # Buscamos si ya hay fuego en esa localidad
        # firesAtPos = [f for f in self.fires if f.pos == self.dice]
        firesAtPos = self.fires[self.dice]

        # Si no hay fuego en esa localidad, se coloca un nuevo marcador como smoke
        if firesAtPos == 0:
            fire = Fire(self.dice, state="smoke")
            self.fires[self.dice] = fire

            # Si había bomberos en la localidad, serán derrotados
            firefighterAtPos = self.grid.get_cell_list_contents([self.dice])
            if firefighterAtPos:
                self.moveToAmbulance(firefighterAtPos[0])
                firefighterAtPos[0].knockedDown = True

            # Si había POIs en la localidad, serán perdidos
            # PoiAtPos = [p for p in self.POIs if p.pos == self.dice]
            PoiAtPos = self.POIs[self.dice]

            if PoiAtPos != 0:
                # Revelamos el POI y si era una víctima la añadimos a las perdidas
                PoiAtPos.reveal()
                if PoiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[self.pos] = 0
                self.activePois -= 1

        else:
            # Si es humo, lo hacemos fuego
            if fire.state == "smoke":
                fire.fire()

            # Si es fuego, creamos una explosión
            elif fire.state == "fire":
                self.explosion(self.dice)

    # TODO: Añadir lógica para cuando las celdas adyacentes estén fuera del tablero
    def explosion(self, pos):

        ### Arriba ###
        upPos = (pos[0], pos[1] + 1)
        upFire = self.fires[upPos]
        if upFire != 0:
            # Si ya había fuego, empezar shockwave
            if upFire.state == "fire":
                self.shockwave(upPos, "up")
        else:
            # Si no había fuego, añadirlo
            upFire = Fire(upPos)
            self.fires[upPos] = upFire

            cell = self.cells[pos[1]][pos[0]]
            # Revisar si había una pared
            # Si hay pared y aún no está destruida, aumentar daño
            if cell.walls["up"]:
                if not cell.walls["up"].isDestroyed():
                    cell.walls["up"].addDamage()
                    self.damageTokens += 1

            # Revisar si había una puerta
            # Si hay puerta y no está destruida, destruirla
            if cell.doors["up"]:
                if not cell.doors["up"].isDestroyed():
                    cell.doors["up"].destroy()

            # Si había bomberos en la localidad, serán derrotados
            firefighterAtPos = self.grid.get_cell_list_contents([upPos])
            if firefighterAtPos:
                self.moveToAmbulance(firefighterAtPos[0])
                firefighterAtPos[0].knockedDown = True

            # Si había POIs en la localidad, serán perdidos
            PoiAtPos = self.POIs[upPos]

            if PoiAtPos != 0:
                # Revelamos el POI y si era una víctima la añadimos a las perdidas
                PoiAtPos.reveal()
                if PoiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[upPos] = 0
                self.activePois -= 1

        ### Abajo ###
        downPos = (pos[0], pos[1] - 1)
        downFire = self.fires[downPos]
        if downFire != 0:
            # Si ya había fuego, empezar shockwave
            if downFire.state == "fire":
                self.shockwave(downPos, "down")
        else:
            # Si no había fuego, añadirlo
            downFire = Fire(downPos)
            self.fires[downPos] = downFire

            cell = self.cells[pos[1]][pos[0]]
            # Revisar si había una pared
            # Si hay pared y aún no está destruida, aumentar daño
            if cell.walls["down"]:
                if not cell.walls["down"].isDestroyed():
                    cell.walls["down"].addDamage()
                    self.damageTokens += 1

            # Revisar si había una puerta
            # Si hay puerta y no está destruida, destruirla
            if cell.doors["down"]:
                if not cell.doors["down"].isDestroyed():
                    cell.doors["down"].destroy()

            # Si había bomberos en la localidad, serán derrotados
            firefighterAtPos = self.grid.get_cell_list_contents([downPos])
            if firefighterAtPos:
                self.moveToAmbulance(firefighterAtPos[0])
                firefighterAtPos[0].knockedDown = True

            # Si había POIs en la localidad, serán perdidos
            PoiAtPos = self.POIs[downPos]

            if PoiAtPos != 0:
                # Revelamos el POI y si era una víctima la añadimos a las perdidas
                PoiAtPos.reveal()
                if PoiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[downPos] = 0
                self.activePois -= 1

        ### Derecha ###
        rPos = (pos[0] + 1, pos[1])
        rFire = self.fires[rPos]
        if rFire != 0:
            # Si ya había fuego, empezar shockwave
            if rFire.state == "fire":
                self.shockwave(rPos, "right")
        else:
            # Si no había fuego, añadirlo
            rFire = Fire(rPos)
            self.fires[rPos] = rFire

            cell = self.cells[pos[1]][pos[0]]
            # Revisar si había una pared
            # Si hay pared y aún no está destruida, aumentar daño
            if cell.walls["right"]:
                if not cell.walls["right"].isDestroyed():
                    cell.walls["right"].addDamage()
                    self.damageTokens += 1

            # Revisar si había una puerta
            # Si hay puerta y no está destruida, destruirla
            if cell.doors["right"]:
                if not cell.doors["right"].isDestroyed():
                    cell.doors["right"].destroy()

            # Si había bomberos en la localidad, serán derrotados
            firefighterAtPos = self.grid.get_cell_list_contents([rPos])
            if firefighterAtPos:
                self.moveToAmbulance(firefighterAtPos[0])
                firefighterAtPos[0].knockedDown = True

            # Si había POIs en la localidad, serán perdidos
            PoiAtPos = self.POIs[rPos]

            if PoiAtPos != 0:
                # Revelamos el POI y si era una víctima la añadimos a las perdidas
                PoiAtPos.reveal()
                if PoiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[rPos] = 0
                self.activePois -= 1

        ### Izquierda ###
        lPos = (pos[0] - 1, pos[1])
        lFire = self.fires[lPos]
        if lFire != 0:
            # Si ya había fuego, empezar shockwave
            if lFire.state == "fire":
                self.shockwave(lPos, "left")
        else:
            # Si no había fuego, añadirlo
            lFire = Fire(lPos)
            self.fires[lPos] = lFire

            cell = self.cells[pos[1]][pos[0]]
            # Revisar si había una pared
            # Si hay pared y aún no está destruida, aumentar daño
            if cell.walls["left"]:
                if not cell.walls["left"].isDestroyed():
                    cell.walls["left"].addDamage()
                    self.damageTokens += 1

            # Revisar si había una puerta
            # Si hay puerta y no está destruida, destruirla
            if cell.doors["left"]:
                if not cell.doors["left"].isDestroyed():
                    cell.doors["left"].destroy()

            # Si había bomberos en la localidad, serán derrotados
            firefighterAtPos = self.grid.get_cell_list_contents([lPos])
            if firefighterAtPos:
                self.moveToAmbulance(firefighterAtPos[0])
                firefighterAtPos[0].knockedDown = True

            # Si había POIs en la localidad, serán perdidos
            PoiAtPos = self.POIs[lPos]

            if PoiAtPos != 0:
                # Revelamos el POI y si era una víctima la añadimos a las perdidas
                PoiAtPos.reveal()
                if PoiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[lPos] = 0
                self.activePois -= 1

    def shockwave(self, pos, direction):
        # Mapear direcciones a vectores
        directions = {"up": (0, 1), "down": (0, -1), "right": (1, 0), "left": (-1, 0)}
        dx, dy = directions[direction]

        x, y = pos
        while True:
            x += dx
            y += dy

            # Detener si salimos del tablero
            if not (0 <= x < self.width + 2 and 0 <= y < self.height + 2):
                break

            pos = (x, y)
            cell = self.cells[y][x]

            # Dañar pared
            if cell.walls.get(direction):
                if not cell.walls[direction].isDestroyed():
                    cell.walls[direction].addDamage()
                    self.damageTokens += 1
                break

            # Destruir puerta si existe
            if cell.doors.get(direction):
                if not cell.doors[direction].isDestroyed():
                    cell.doors[direction].destroy()
                break

            # Colocar fuego
            fire = self.fires[y][x]
            if fire == 0:
                fire = Fire(pos, state="fire")
                self.fires[y][x] = fire
                cell.fire = fire
                break

            # Verificar bomberos
            firefighterAtPos = self.grid.get_cell_list_contents([pos])
            for ff in firefighterAtPos:
                self.moveToAmbulance(ff)
                ff.knockedDown = True

            # Verificar POIs
            poiAtPos = self.POIs[y][x]
            if poiAtPos != 0:
                poiAtPos.reveal()
                if poiAtPos.victim == 1:
                    self.victimsLost += 1
                self.POIs[y][x] = 0
                self.activePois -= 1

    def flashover(self):
        pass

    # Cuando un firefighter está en knockout, moverlo a la posición de la ambulancia
    def moveToAmbulance(self, firefighter):
        self.grid.remove_agent(firefighter)
        self.grid.place_agent(firefighter, self.ambulancePos)
        firefighter.pos = self.ambulancePos
        firefighter.knockedDown = False

    # BFS para sacar a las víctimas
    def bfs(self, start, goal):
        queue = deque()
        queue.append([start])
        visited = set([start])

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (x, y) == goal:
                return path

            neighbors = self.getNeighbors(x, y)

            for nX, nY in neighbors:
                if (nX, nY) not in visited:
                    visited.add((nX, nY))
                    queue.append(path + [(nX, nY)])
        return None

    # Encontrar los vecinos (Falta validar, se pidió a Chat)
    def getNeighbors(self, x, y):
        # Explicar / comentar código
        neighbors = []
        directions = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}

        currentCell = self.cells[y][x]

        for dir, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # Si hay pared, no se puede pasar
                if currentCell.walls[dir] is not None:
                    continue
                # Si hay puerta cerrada, no se puede pasar
                if (
                    currentCell.doors[dir] is not None
                    and not currentCell.doors[dir].isOpen
                ):
                    continue

            neighbors.append((nx, ny))

        return neighbors

    # Añadir la lógica del step
    def step(self):
        # Simular los dados
        self.dice = (random.randrange(self.width), random.randrange(self.height))
        if self.round != 0:
            self.advanceFire()
            self.replendishPOI()
        self.schedule.step()
        self.advanceFire()

    # Verificación de los estatus del juego
    def victory(self):
        return self.victimsRescued >= 7

    def defeat(self):
        return self.victimsLost >= 4 or self.buildingCollapse()

    def buildingCollapse(self):
        return self.damageTokens >= 24

    # Añadir los nuevos POI al final de cada ronda
    def replendishPOI(self):

        newPOIsNeeded = 3 - self.activePois

        if newPOIsNeeded == 0:
            return

        else:
            for _ in range(newPOIsNeeded):
                # Tiramos los dados
                self.rollDice()

                # Si hay fuego en la celda, eliminarlo antes de colocar el POI
                for fire in list(self.fires):
                    if fire.pos == self.dice and fire.state == "fire":
                        self.fires.remove(fire)
                        break

                # Si aún quedan fichas de ambos, se inicializa el POI al azar
                if self.totalVictims > 0 and self.totalFalseAlarms > 0:
                    victim = np.random.randint(0, 2)
                    poi = Poi(self.dice, victim)
                    self.POIs[self.dice] = poi

                # Si solo hay víctimas, se inicializa como víctima
                elif self.totalVictims > 0:
                    poi = Poi(self.dice, 1)
                    self.POIs[self.dice] = poi

                # Si solo hay falsas alarmas, se inicializa como falsa alarma
                elif self.totalFalseAlarms > 0:
                    poi = Poi(self.dice, 0)
                    self.POIs[self.dice] = poi

                else:
                    print("Ya no hay POI disponibles")
