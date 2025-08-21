from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run

from ..Utils.getGrid import getGrid

class FireRescueModel(Model):
    def __init__(self, width = 8, height = 6, agents = 6, victimsMarkers = 10, damageCounters = 24):
        super().__init__()

        self.grid = MultiGrid(width, height, torus = False)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters = {
                "Grid" : getGrid,
                "Steps": lambda model : model.steps
            },
            agent_reporters = {}
        )

        self.damageCounters = damageCounters
        self.ambulanceParkingSpot = [0,0]
        
    def step(self):
        return
    
    def victory(self):
        return
    
    def defeat(self):
        return
    
    def buildingCollapse(self):
        return
    
    def replendishPOI(self):
        return
        