boardConfiguration = {
    "cells": [
        [
            # Exterior superior
            # 0
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
        ],
        [
            # Fondo
            # 7
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
        ],
    ],
    "POILocations": [],
    "fireLocations": [],
    "doorLocations": [],
    "accessPoints": [],
    "ambulancePosition": [
        [0, 4],
        [0, 5],
        [3, 7],
        [4, 7],
        [5, 0],
        [6, 0],
        [9, 3],
        [9, 4],
    ],
}

file = open("config.txt")


# Configure cells
def setCells(chunk):
    row = [[0, 1, 0, 0]]
    for cell in chunk.split(" "):
        row.append(list(map(int, cell)))

    row.append([0, 0, 0, 1])
    boardConfiguration["cells"].insert(-1, row)


def setPoiLocations(chunk):
    y, x, v = chunk.split(" ")
    v = (lambda v: 1 if v == "v" else 0)(v)
    boardConfiguration["POILocations"].append([int(x), int(y), v])


def setFireLocations(chunk):
    y, x = list(map(int, chunk.split(" ")))
    boardConfiguration["fireLocations"].append([x, y])


def setDoorLocations(chunk):
    y, x, y2, x2 = list(map(int, chunk.split(" ")))
    boardConfiguration["doorLocations"].append([x, y, x2, y2])


def setAccessPoints(chunk):
    y, x = list(map(int, chunk.split(" ")))
    boardConfiguration["accessPoints"].append([x, y])


length = 0
strategy = -1
strategies = [
    setCells,
    setPoiLocations,
    setFireLocations,
    setDoorLocations,
    setAccessPoints,
]

for chunk in iter(lambda: file.readline(), ""):
    if chunk[-2] == " ":
        chunk = chunk[:-2]
    chunk = chunk.replace("\n", "")
    if len(chunk) != length:
        length = len(chunk)
        strategy += 1
    chunk.split(" ")
    strategies[strategy](chunk)

file.close()

print(boardConfiguration)
