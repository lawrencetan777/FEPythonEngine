import numpy as np
import pygame
from pygame.locals import *
import pytmx

mapFile = "testmap.tmx"


class Tile:
    def __init__(self, image):
        self.image = image


class Tilemap:
    def __init__(self, file):
        self.image = pygame.display.set_mode((240, 160))
        tmxData = pytmx.load_pygame(file)
        self.mapHeight = tmxData.height
        self.mapWidth = tmxData.width
        self.xOffset = 0
        self.yOffset = 0
        self.tileArray = []
        for y in range(self.mapHeight):
            row = []
            for x in range(self.mapWidth):
                tileImage = tmxData.get_tile_image(x, y, 0)
                row.append(Tile(tileImage))
            self.tileArray.append(row)

        self.tileArray = np.array(self.tileArray, dtype=object)

    def render(self):
        for x in range(15):
            for y in range(10):
                self.image.blit(self.tileArray[y + self.yOffset][x + self.xOffset].image, (x * 16, y * 16))

    def addOffsets(self, x,y):

        self.xOffset = self.xOffset + x
        self.yOffset = self.yOffset + y


class Game:
    def run(self):
        pygame.init()
        gamescreen = pygame.display.set_mode((240, 160))
        running = True
        tilemaptest.render()
        gamescreen.blit(tilemaptest.image, (0, 0))

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if tilemaptest.yOffset > 0:
                            tilemaptest.addOffsets(0, -1)
                    elif event.key == K_DOWN:
                        if tilemaptest.yOffset < tilemaptest.mapHeight - 10:
                            tilemaptest.addOffsets(0, 1)
                    elif event.key == K_LEFT:
                        if tilemaptest.xOffset > 0:
                            tilemaptest.addOffsets(-1, 0)
                    elif event.key == K_RIGHT:
                        if tilemaptest.xOffset < tilemaptest.mapWidth - 15:
                            tilemaptest.addOffsets(1, 0)

                    tilemaptest.render()
                    gamescreen.blit(tilemaptest.image, (0, 0))
            pygame.display.flip()


tilemaptest = Tilemap(mapFile)

game = Game()
game.run()
