import pygame
from pygame.locals import *
import pytmx
import numpy as np
import json
from units import Unit  # Your Unit class that loads from JSON

mapFile = "converted_map_csv.tmx"
classFile = "game_data/classes.json"  # Your JSON class data file
with open(classFile) as f:
    class_data = json.load(f)


class Tile:
    def __init__(self, image):
        self.image = image


class Tilemap:
    def __init__(self, file):
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
        self.image = pygame.Surface((240, 160))

    def render(self):
        self.image.fill((0, 0, 0))  # Clear previous
        for x in range(15):
            for y in range(10):
                tile = self.tileArray[y + self.yOffset][x + self.xOffset]
                if tile.image:
                    self.image.blit(tile.image, (x * 16, y * 16))

    def addOffsets(self, x, y):
        self.xOffset += x
        self.yOffset += y


class Cursor:
    def __init__(self):
        self.screenX = 0  # screen position
        self.screenY = 5
        self.x = 0  # map position
        self.y = 5
        self.image = pygame.image.load("pixil-frame-0.png").convert_alpha()


class Game:
    def run(self):
        pygame.init()
        gamescreen = pygame.display.set_mode((240, 160))
        pygame.display.set_caption("Tilemap + Unit Stats")
        font = pygame.font.SysFont(None, 18)

        tilemaptest = Tilemap(mapFile)
        cursor = Cursor()

        # Create your unit with JSON class data path and level
        archer = Unit("Neimi", "Archer", "Female", 5, 5, class_data=class_data, level=5)

        running = True
        clock = pygame.time.Clock()
        tilemaptest.render()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    moved = False
                    if event.key == K_UP:
                        if cursor.screenY > 0:
                            if cursor.screenY > 2:
                                cursor.screenY -= 1
                                moved = True
                            elif tilemaptest.yOffset > 0:
                                tilemaptest.addOffsets(0, -1)
                                moved = True
                            else:
                                cursor.screenY -= 1
                                moved = True
                    elif event.key == K_DOWN:
                        if cursor.screenY < 9:
                            if cursor.screenY < 7:
                                cursor.screenY += 1
                                moved = True
                            elif tilemaptest.yOffset < tilemaptest.mapHeight - 10:
                                tilemaptest.addOffsets(0, 1)
                                moved = True
                            else:
                                cursor.screenY += 1
                                moved = True
                    elif event.key == K_LEFT:
                        if cursor.screenX > 0:
                            if cursor.screenX > 2:
                                cursor.screenX -= 1
                                moved = True
                            elif tilemaptest.xOffset > 0:
                                tilemaptest.addOffsets(-1, 0)
                                moved = True
                            else:
                                cursor.screenX -= 1
                                moved = True
                    elif event.key == K_RIGHT:
                        if cursor.screenX < 14:
                            if cursor.screenX < 12:
                                cursor.screenX += 1
                                moved = True
                            elif tilemaptest.xOffset < tilemaptest.mapWidth - 15:
                                tilemaptest.addOffsets(1, 0)
                                moved = True
                            else:
                                cursor.screenX += 1
                                moved = True

                    # Update actual map coordinates
                    cursor.x = cursor.screenX + tilemaptest.xOffset
                    cursor.y = cursor.screenY + tilemaptest.yOffset

                    if moved:
                        tilemaptest.render()

            # Draw everything each frame
            gamescreen.fill((0, 0, 0))
            gamescreen.blit(tilemaptest.image, (0, 0))
            gamescreen.blit(cursor.image, (cursor.screenX * 16, cursor.screenY * 16))
            archer.draw(gamescreen, tilemaptest.xOffset, tilemaptest.yOffset)

            if cursor.x == archer.x and cursor.y == archer.y:
                pass

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
