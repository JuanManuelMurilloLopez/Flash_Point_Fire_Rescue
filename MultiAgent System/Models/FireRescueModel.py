from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run

from ..Utils.getGrid import getGrid
from ..Utils.BoardInitialConfig import boardConfig
from ..Models.Firefighter import Firefighter
from ..Models.Fire import Fire
from .POIAgent import POIAgent

import numpy as np
import random
from collections import deque

class FireRescueModel(Model):
    def __init__(self, width = 8, height = 6, agents = 6, victimsMarkers = 10, board = boardConfig, ambulancePos = [0,0]):
        super().__init__()

        # Medidas del grid del edificio
        self.width = width
        self.height = height

        # Se le agregan 2 para añadir el exterior
        self.grid = MultiGrid(width + 2, height + 2, torus = False)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Grid": getGrid,
                "Steps": lambda model: model.steps,
                "VictimsRescued": lambda model: model.victimsRescued,
                "VictimsLost": lambda model: model.victimsLost
            },
            agent_reporters={}
        )

        # Variables para conocer el estatus del juego
        self.victimsRescued = 0
        self.victimsLost = 0
        self.damageTokens = 0

        # Información del tablero
        self.board = board
        # TODO: Modificar la posición de la ambulancia a la correcta
        self.ambulancePos = ambulancePos

        # Añadimos los POI iniciales
        self.POIs = []
        for poiData in board["POILocations"]:
            # Creamos el agente en la posición indicada
            poi = POIAgent(self, (poiData[0], poiData[1]), poiData[3])
            self.grid.place_agent(poi, (poi.pos))
            self.schedule.add(poi)
            self.POIs.append(poi)

        # Añadimos el fuego inicial
        self.fires = []
        # Creamos el agente en la posición indicada
        for pos in board["fireLocations"]:
            fire = Fire(self, pos)
            self.grid.place_agent(fire, pos)
            self.schedule.add(fire)
            self.fires.append(fire)

        # Añadir los Firefighters
        for i in range(agents):
            # TODO: Verificar las posiciones en las que se deben posicionar los bomberos inicialmente
            pos = [0, 0]
            fireFighter = Firefighter(self, pos)
            self.grid.place_agent(fireFighter, pos)
            self.schedule.add(fireFighter)
        
        
    def advanceFire(self):
        # Simular los dados
        diceX, diceY = random.randrage(self.width), random.randrange(self.height)
        agents = self.grid.get_cell_list_contents([diceX, diceY])

        # Si no hay fuego, añadir humo
        if not agents:
            fire = Fire(self, [diceX, diceY], state = "smoke")
            self.grid.place_agent(fire, [diceX, diceY])
            self.schedule.add(fire)
        else:
            # Cambiar el humo a fuego y verificar explosiones
            for agent in agents:
                if isinstance(agent, Fire):
                    if agent.state == "smoke":
                        agent.fire()
                    elif agent.state == "fire":
                        self.explosion([diceX, diceY])

    # TODO: Añadir lógica de las explosiones
    def explosion(self, pos):
        pass

    # Cuando un firefighter está en knockout, moverlo a la posición de la ambulancia
    def moveToAmbulance(self, firefighter):
        self.grid.remove_agent(firefighter)
        self.grid.place_agent(firefighter, self.ambulancePos)
        firefighter.pos = self.ambulancePos

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
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # TODO: verificar paredes/puertas con self.board_config
                neighbors.append((nx, ny))
        return neighbors

    # Añadir la lógica del step
    def step(self):
        self.schedule.step()
        self.advanceFire()
    
    # Verificación de los estatus del juego
    def victory(self):
        return self.victimsRescued >= 7
    
    def defeat(self):
        return (self.victimsLost >= 4 or self.buildingCollapse())
    
    def buildingCollapse(self):
        return self.damageTokens >= 24
    
    # Añadir los nuevos POI al final de cada ronda
    def replendishPOI(self):
        # Refactorizar para no ocupar esa sintaxis en currentPOIs
        currentPOIs = [a for a in self.POIs if not a.rescued and not a.lost]
        newPOIsNeeded = 3 - len(currentPOIs)

        if newPOIsNeeded == 0:
            return
        # También cambiar esto
        freePositions = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid.is_cell_empty((x, y))]
        
        for _ in range(newPOIsNeeded):
            if not freePositions:
                break
            pos = self.random.choice(freePositions)
            freePositions.remove(pos)
            victimOrFalseAlarm = self.random.choice([0, 1])
            poi = POIAgent(self, pos, victimOrFalseAlarm)
            self.grid.place_agent(poi, pos)
            self.schedule.add(poi)
            self.POIs.append(poi)

    
        