"""import asyncio
import pygame

pygame.init()
pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()


async def main():
    count = 60

    while True:
        print(f"{count}: Hello from Pygame")
        pygame.display.update()
        await asyncio.sleep(0)  # You must include this statement in your main loop. Keep the argument at 0.

        if not count:
            pygame.quit()
            return
        
        count -= 1
        clock.tick(60)

asyncio.run(main())

"""
import pygame
import time
import random
import asyncio



pygame.init()
screen = pygame.display.set_mode((400,460))
clock = pygame.time.Clock()

async def main():
    global running
    running = True

    random.seed()
    
    SEGMENT_WIDTH = 1 * 20
    SEGMENT_BORDER = SEGMENT_WIDTH / 20
    
    board = [[0 for _ in range(10)] for _ in range(22)]
    bag = []
    global gravity
    gravity = 48 # frames per drop
    softDropMult = 6
    global score
    global level
    global lines
    level = 0
    lines = 0
    score = 0
    global font
    font = pygame.font.Font(None,20)
    
    LINE_SCORES = [0,100,300,500,800]
    LEVEL_GRAV = [48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2,1]
    NON_I_KICKS = {
        "01":[( 0, 0),(-1, 0),(-1,+1),( 0,-2),(-1,-2)],
        "10":[( 0, 0),(+1, 0),(+1,-1),( 0,+2),(+1,+2)],
        "12":[( 0, 0),(+1, 0),(+1,-1),( 0,+2),(+1,+2)],
        "21":[( 0, 0),(-1, 0),(-1,+1),( 0,-2),(-1,-2)],
        "23":[( 0, 0),(+1, 0),(+1,+1),( 0,-2),(+1,-2)],
        "32":[( 0, 0),(-1, 0),(-1,-1),( 0,+2),(-1,+2)],
        "30":[( 0, 0),(-1, 0),(-1,-1),( 0,+2),(-1,+2)],
        "03":[( 0, 0),(+1, 0),(+1,+1),( 0,-2),(+1,-2)],
        "02":[( 0, 0),(+1, 0),(+2, 0),(+1,+1),(+2,+1)],#,(-1, 0),(-2, 0),(-1,+1),(-2,+1),( 0,-1),(+3, 0),(-3, 0)
        "13":[( 0, 0),( 0,+1),( 0,+2),(-1,+1),(-1,+2)],#,( 0,-1),( 0,-2),(-1,-1),(-1,-2),(+1, 0),( 0,+3),( 0,-3)
        "20":[( 0, 0),(-1, 0),(-2, 0),(-1,-1),(-2,-1)],#,(+1, 0),(+2, 0),(+1,-1),(+2,-1),( 0,+1),(-3, 0),(+3, 0)
        "31":[( 0, 0),( 0,+1),( 0,+2),(+1,+1),(+1,+2)] #,( 0,-1),( 0,-2),(+1,-1),(+1,-2),(-1, 0),( 0, 3),( 0,-3)
    }
    I_KICKS = {
        "01":[( 0, 0),(-2, 0),(+1, 0),(-2,-1),(+1,+2)],
        "10":[( 0, 0),(+2, 0),(-1, 0),(+2,+1),(-1,-2)],
        "12":[( 0, 0),(-1, 0),(+2, 0),(-1,+2),(+2,-1)],
        "21":[( 0, 0),(+1, 0),(-2, 0),(+1,-2),(-2,+1)],
        "23":[( 0, 0),(+2, 0),(-1, 0),(+2,+1),(-1,-2)],
        "32":[( 0, 0),(-2, 0),(+1, 0),(-2,-1),(+1,+2)],
        "30":[( 0, 0),(+1, 0),(-2, 0),(+1,-2),(-2,+1)],
        "03":[( 0, 0),(-1, 0),(+2, 0),(-1,+2),(+2,-1)],
        "02":[( 0, 0),(-1, 0),(-2, 0),(1, 0),(2, 0),(0, 1)],
        "13":[( 0, 0),( 0,+1),( 0,+2),(0,-1),(0,-2),(-1, 0)],
        "20":[( 0, 0),(+1, 0),(+2, 0),(-1, 0),(-2, 0),(0,-1)],
        "31":[( 0, 0),( 0,+1),( 0,+2),(0,-1),(0,-2),(1, 0)]
    }
    MINO_MATRICES = [
        [[-2,-1],[-1,-1],[0,-1],[1,-1]], #i
        [[-1.5,-1.5],[-1.5,-0.5],[-0.5,-0.5],[0.5,-0.5]], #j
        [[-1.5,-0.5],[-0.5,-0.5],[0.5,-0.5],[0.5,-1.5]], #l
        [[-1,-1],[-1,0],[0,0],[0,-1]], #o
        [[-1.5,-0.5],[-0.5,-0.5],[-0.5,-1.5],[0.5,-1.5]], #s
        [[-1.5,-0.5],[-0.5,-1.5],[-0.5,-0.5],[0.5,-0.5]], #t
        [[-1.5,-1.5],[-0.5,-1.5],[-0.5,-0.5],[0.5,-0.5]] #z
    ]
    
    
    class Mino:
        def __init__(self, posX, posY, pieceType):
            self.posX = posX
            self.posY = posY
            self.matrix = [[0,0],[0,0],[0,0],[0,0]]
            for idx1,block in enumerate(MINO_MATRICES[pieceType]):
                self.matrix[idx1][0] = block[0]
                self.matrix[idx1][1] = block[1]
            self.pieceType = pieceType
            self.color = pieceType + 1
            self.gravityTicker = 0
            self.rotation = 0
    
        def __str__(self):
            return f"PosX {self.posX}, PosY {self.posY}, piecetype {self.pieceType}, gravityticker {self.gravityTicker}"
        
        def drawSelf(self,x,y):
            for block in self.matrix:
                globalPosX = block[0] * SEGMENT_WIDTH + x
                globalPosY = block[1] * SEGMENT_WIDTH + y
                blockRect = pygame.Rect(globalPosX + SEGMENT_BORDER, globalPosY + SEGMENT_BORDER, SEGMENT_WIDTH, SEGMENT_WIDTH)
                pygame.draw.rect(screen, "red", blockRect, SEGMENT_WIDTH, 4)
    
        def addToBoard(self):
            for block in self.matrix:
                board[int(self.posY + block[1])][int(self.posX + block[0])] = self.color
    
        def removeFromBoard(self):
            for block in self.matrix:
                board[int(self.posY + block[1])][int(self.posX + block[0])] = 0
    
        def addInitial(self):
            match(self.pieceType):
                case 0:
                    self.posX = 5
                    self.posY = 2
                case 1:
                    self.posX = 4.5
                    self.posY = 1.5
                case 2:
                    self.posX = 4.5
                    self.posY = 1.5
                case 3:
                    self.posX = 5
                    self.posY = 1
                case 4:
                    self.posX = 4.5
                    self.posY = 1.5
                case 5:
                    self.posX = 4.5
                    self.posY = 1.5
                case 6:
                    self.posX = 4.5
                    self.posY = 1.5
            for block in self.matrix:
                if board[int(self.posY + block[1])][int(self.posX + block[0])] != 0:
                    global running
                    running = False
                    print("Closed")
                    screen.fill("red")
                    pygame.display.update()
            self.addToBoard()
    
        def rotate(self, rotations):
            self.removeFromBoard()
            newMatrix = [[i[0],i[1]] for i in self.matrix]
            self.rotation += rotations
            self.rotation %= 4
            match rotations % 4:
                case 1:
                    for block in newMatrix:
                        temp = block[0]
                        block[0] = block[1] * -1
                        block[0] -= 1
                        block[1] = temp
                case 2:
                    for block in newMatrix:
                        block[0] *= -1
                        block[0] -= 1
                        block[1] *= -1
                        block[1] -= 1
                case 3:
                    for block in newMatrix:
                        temp = block[0]
                        block[0] = block[1]
                        block[1] = temp * -1
                        block[1] -= 1
                case _:
                    raise Exception("Invalid rotation")
            rotateString = f"{(self.rotation-rotations)%4}{self.rotation}"
            kicks = []
            if self.pieceType == 0:
                kicks = I_KICKS[rotateString]
            else:
                kicks = NON_I_KICKS[rotateString]
            for kickSet in kicks:
                if self.isMoveValid(kickSet[0],0-kickSet[1],newMatrix) == "good":
                    self.move(kickSet[0],0-kickSet[1],newMatrix)
                    return
            self.addToBoard()
            self.rotation -= rotations
            self.rotation %= 4
    
        def tickGravity(self):
            global score
            self.gravityTicker += 1
            localGrav = gravity
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                localGrav = gravity / 6
            if self.gravityTicker >= localGrav:
                self.move(0,self.gravityTicker//localGrav)
                self.gravityTicker -= localGrav
                if localGrav < gravity:
                    score += 1
    
        def isMoveValid(self,dx,dy,newMatrix = None):
            sameMatrix = False
            if newMatrix is None:
                newMatrix = self.matrix
                sameMatrix = True
            checkY = dy != 0 or not sameMatrix
            checkX = dx != 0 or not sameMatrix
            for block in newMatrix:
                newX = int(self.posX + block[0] + dx)
                newY = int(self.posY + block[1] + dy)
                if (newX < 0 or newX > 9) and checkX:
                    if not sameMatrix: return "rotate"
                    return "side"
                if newY > 21 and checkY:
                    if not sameMatrix: return "rotate"
                    return "below"
                if board[newY][newX] != 0:
                    if not sameMatrix: return "rotate"
                    if dx != 0: return "side"
                    if dy != 0: return "below"
            return "good"
        
        def move(self,dx,dy,newMatrix = None):
            self.removeFromBoard()
            if newMatrix is None:
                newMatrix = self.matrix
                isValid = self.isMoveValid(dx,dy)
            else:
                isValid = self.isMoveValid(dx,dy,newMatrix)
            newX = self.posX + dx
            newY = self.posY + dy
            if isValid == "good":
                self.posX = newX
                self.posY = newY
                self.matrix = newMatrix
            self.addToBoard()
            if isValid == "below":
                print("hard drop")
                print(self)
                checkLineClears(self)
                setPiece()
    
        def setPos(self,x,y,newMatrix = None):
            if newMatrix is None:
                newMatrix = self.matrix
    
    def buildBoard():
        topCorner = 10
        for rowIdx in range(22):
            for colIdx in range(10):
                color = ""
                borderColor = ""
                match(board[rowIdx][colIdx]):
                    case -1:
                        color = "darkgray"
                    case 0: 
                        color = "gray"
                    case 1: 
                        color = "cyan"
                    case 2: 
                        color = "blue"
                    case 3: 
                        color = "orange"
                    case 4: 
                        color = "yellow"
                    case 5: 
                        color = "lime"
                    case 6: 
                        color = "purple"
                    case 7: 
                        color = "red"
                    case _:
                        raise Exception("Invalid color detected in board")
                blockRect = pygame.Rect(colIdx * SEGMENT_WIDTH + topCorner, rowIdx * SEGMENT_WIDTH + topCorner, SEGMENT_WIDTH, SEGMENT_WIDTH)
                pygame.draw.rect(screen, color, blockRect, SEGMENT_WIDTH, 4)
    
    global mainMino
    mainMino = None
    
    def fillBag():
        tempBag = []
        for i in range(7):
            tempBag.append(i)
        random.shuffle(tempBag)
        bag.extend(tempBag)
    
    def clearBoard():
        for rowIdx in range(22):
            for colIdx in range(10):
                board[rowIdx][colIdx] = 0
    
    def hardDrop():
        global score
        curMino = mainMino
        while mainMino == curMino:
            mainMino.move(0,1)
            score += 2
    
    def setPiece():
        global mainMino
        mainMino = Mino(-1,-1,bag.pop(0))
        mainMino.addInitial()
        if len(bag) < 7:
            fillBag()
    
    def write(text,location,color=(255,255,255)):
        screen.blit(font.render(text,True,color),location)
    
    def checkLineClears(placedMino):
        global score
        global lines
        global level
        global gravity
        rows = [int(block[1] + placedMino.posY) for block in placedMino.matrix]
        rows.sort()
        tempLines = 0
        for row in rows:
            if not (0 in board[row]):
                tempLines += 1
                board[row] = [0 for _ in range(10)]
                rowsToMove = range(row-1,-1,-1)
                for rowToMove in rowsToMove:
                    for idx in range(10):
                        board[rowToMove+1][idx] = board[rowToMove][idx]
        lines += tempLines
        if lines >= (level + 1) * 10:
            level = level + 1 if level < 29 else 29
            print(gravity)
            gravity = LEVEL_GRAV[level]
            print(gravity)
        score += LINE_SCORES[tempLines] * (level + 1)
            
    
    fillBag()
    setPiece()
    
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        mainMino.move(-1,0)
                    case pygame.K_RIGHT:
                        mainMino.move(1,0)
                    case pygame.K_z:
                        mainMino.rotate(3)
                    case pygame.K_x:
                        mainMino.rotate(1)
                    case pygame.K_c:
                        mainMino.rotate(2)
                    case pygame.K_UP:
                        hardDrop()
                    case pygame.K_DOWN:
                        mainMino.gravityTicker = gravity / softDropMult
                    case _:
                        pass
    
        screen.fill("black")
    
        mainMino.tickGravity()
    
        write(f"Level: {level}",(220,10))
        write(f"Lines: {lines}",(220,60))
        write(f"Score: {score}",(220,110))
        write(f"Grvty: {gravity}",(220,160))
    
        buildBoard()
        
        pygame.display.update()
    
        clock.tick(60) 
        await asyncio.sleep(0)
        
asyncio.run(main())