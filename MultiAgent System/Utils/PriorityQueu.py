# Pérez, P. (2022). tc2008b. Github. https://github.com/Manchas2k4/tc2008b

import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, priority, value):
        heapq.heappush(self.queue, (priority, value))

    def pop(self):
        if self.queue:
            heapq.heappop(self.queue)

    def top(self):
        if self.queue:
            return self.queue[0]
