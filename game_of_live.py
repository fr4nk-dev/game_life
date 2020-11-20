import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25
dimCW = width / nxC
dimCH = height / nyC

gamestate = np.zeros((nxC, nyC))

gamestate[5, 3] = 1
gamestate[5, 4] = 1
gamestate[5, 5] = 1

gamestate[21, 21] = 1
gamestate[22, 22] = 1
gamestate[22, 23] = 1
gamestate[21, 23] = 1
gamestate[20, 23] = 1

pauseExect = False
while True:

    buffer = np.copy(gamestate)

    screen.fill(bg)

    time.sleep(0.1)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()

        if(sum(mouseClick) > 0):
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY/dimCH))
            buffer[celX, celY] = not mouseClick[2]

    for x in range(0, nxC):
        for y in range(0, nyC):
            if not pauseExect:
                n_neigh = gamestate[(x - 1) % nxC, (y - 1) % nyC] + \
                    gamestate[(x - 1) % nxC, (y) % nyC] + \
                    gamestate[(x - 1) % nxC, (y + 1) % nyC] + \
                    gamestate[(x) % nxC, (y + 1) % nyC] + \
                    gamestate[(x + 1) % nxC, (y + 1) % nyC] + \
                    gamestate[(x + 1) % nxC, (y) % nyC] + \
                    gamestate[(x + 1) % nxC, (y - 1) % nyC] + \
                    gamestate[(x) % nxC, (y - 1) % nyC]

                if gamestate[x, y] == 0 and n_neigh == 3:
                    buffer[x, y] = 1

                elif gamestate[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    buffer[x, y] = 0

            poly = [
                (x * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y+1) * dimCH),
                (x * dimCW, (y+1) * dimCH)
            ]
            if buffer[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 2)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gamestate = np.copy(buffer)
    pygame.display.flip()
