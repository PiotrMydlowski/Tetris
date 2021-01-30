#Tetris game by P Mydlowski via tutorial

import pygame
import random

pygame.init()

#Global variables

sWidth = 800
sHeight = 700
playWidth = 300
playHeight = 600
blockSize = 30

topLeftX = (sWidth - playWidth)//2
topLeftY = sHeight - playHeight

#Shape formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0..',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shapeColor = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,255),(128,0,128)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapeColor[shapes.index(shape)]
        self.rotation = 0

def createGrid(lockedPos = {}):
    grid = [[(0,0,0) for _ in range(playWidth//blockSize)] for _ in range(playHeight//blockSize)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(j, i) in lockedPos:
                grid[i][j] = lockedPos[(j, i)]

    return grid
            
def convertShapeFormat(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i,line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (int(pos[0] - 2), int(pos[1] - 4))

    return positions

def validSpace(shape, grid):
    acceptedPos = [[(j,i) for j in range(playWidth//blockSize) if grid[i][j] == (0,0,0)] for i in range(playHeight//blockSize)]
    acceptedPos = [k for x in acceptedPos for k in x]

    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in acceptedPos:
            if pos[1] > -1:
                return False

    return True

def checkLost(positions):

    for pos in positions:
        x, y = pos
        if y <1:
            return True

    return False

def getShape():
    return Piece(playWidth/blockSize/2,0,random.choice(shapes))

def drawTextMiddle(surface, text, size, color):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', size)
    label = font.render(text, 1, color)
    surface.blit(label, (topLeftX + playWidth//2 - label.get_width()//2,topLeftY + playHeight//2 - label.get_height()//2))


def drawGrid(surface, grid):
    
    sx = topLeftX
    sy = topLeftY

    for i in range (len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy +i*blockSize),(sx+playWidth, sy + i*blockSize))

    for j in range(len(grid[0])):
        pygame.draw.line(surface, (128,128,128), (sx + j*blockSize, sy),(sx + j*blockSize, sy + playHeight))

def clearRows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next Shape:', 1, (255,255,255))

    sx = topLeftX + playWidth + (sWidth - playWidth)//6
    sy = topLeftY + playHeight//2

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate (format):
        row = list(line)
        for j, col in enumerate (row):
            if col == '0':
                pygame.draw.rect(surface, shape.color,(sx + j*blockSize, sy + i*blockSize, blockSize, blockSize), 0)

    surface.blit(label, (sx, sy - label.get_height()))

    

def drawWindow(surface, grid, score=0, maxScore=0):
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))
    surface.blit(label, (topLeftX + playWidth//2 - label.get_width()//2,topLeftY - label.get_height()))

    pygame.draw.rect(surface, (255,0,0), (topLeftX, topLeftY, playWidth, playHeight), 4)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topLeftX + j*blockSize, topLeftY + i*blockSize, blockSize, blockSize), 0)

    drawGrid(surface, grid)

    font = pygame.font.SysFont('comicsans', 30)
    labelScore = font.render('Score: '+ str(score), 1, (255,255,255))
    sx = (sWidth - playWidth)//6
    sy = topLeftY + playHeight//2
    surface.blit(labelScore, (sx, sy - labelScore.get_height()))

    labelMaxScore = font.render('High score: '+ str(maxScore), 1, (255,255,255))
    surface.blit(labelMaxScore, (sx, sy - labelScore.get_height() - labelMaxScore.get_height()))

def updateScore(newScore):

    try:
        with open('score_tetris.txt','r') as f:
            lines = f.readlines()
            score = int(lines[0].strip())

    except:
            score = 0

    with open('score_tetris.txt','w') as f:
        if score < newScore:
            f.write(str(newScore))
            return newScore
        else:
            f.write(str(score))
            return score

def main(surface):

    lockedPos = {}
    grid = createGrid(lockedPos)
    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.3
    levelTime = 0
    score = 0
    maxScore = updateScore(0)

    while run:
        grid = createGrid(lockedPos)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()

        if levelTime/1000 > 5:
            levelTime = 0
            if fallSpeed > 0.1:
                fallSpeed -= 0.005

        if fallTime/1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not(validSpace(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x += 1

                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x -= 1

                if event.key == pygame.K_UP:
                    currentPiece.rotation += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.rotation -= 1

                if event.key == pygame.K_DOWN:
                    currentPiece.y += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.y -= 1  

        shapePos = convertShapeFormat(currentPiece)

        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color

        if changePiece:
            changePiece = False
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPos[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = getShape()
            score += 10 * clearRows(grid, lockedPos)

        if checkLost(lockedPos):
            drawTextMiddle(surface, "YOU LOST...", 90, (255,255,255))
            pygame.display.update()
            maxScore = updateScore(score)
            pygame.time.delay(1500)
            run = False        

        drawWindow(surface, grid, score, maxScore)
        drawNextShape(nextPiece, surface)
        pygame.display.update()

def mainMenu(win):
    run = True
    while run:
        win.fill((0,0,0))
        drawTextMiddle(win, "Press any key to play.", 90,(255,255,255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(win)

win = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('Tetris')
mainMenu(win)

pygame.quit()
quit()
