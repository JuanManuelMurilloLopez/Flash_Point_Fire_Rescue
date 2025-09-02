import numpy as np
from collections import deque
from Utils.PriorityQueu import PriorityQueue


def searchForPOIs(self):
    self.chooseEntry()
    poiPosition = self.selectPOI()
    self.makeRoute(poiPosition)


def chooseEntry(self):
    entrance = np.random.randint(len(self.model.entrances))
    self.model.grid.move_agent(self.model.entrances[entrance])


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


def makeRoute(self, position):
    pq = PriorityQueue()

    pq.push(0, self.pos)
    x, y = self.pos
    dist = np.zeros(self.model.width * self.model.height)
    dist[self.to_int(x, y)] = 0
    while not pq.empty():
        currentDistance, u = pq.top()
        pq.pop()

        currentCell = self.model.cells[x][y]

        if u == position:
            break

        for nX, nY in self.model.getNeighbors(x, y):
            newDistance = dist[self.to_int(x, y)] + 1


def to_int(self, x, y):
    return x + self.model.height * y
