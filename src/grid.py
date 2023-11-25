from utils import loadImages, loadSpriteSheet, directions
import pygame
from tokens import Token
class Grid:
    def __init__(self,rows,columns,size,main):
        self.GAME=main
        self.y=rows
        self.x=columns
        self.size=size
        self.whitetoken = loadImages('assets/WhiteToken.png', size)
        self.blacktoken = loadImages('assets/BlackToken.png', size)
        self.transitionWhiteToBlack = [loadImages(f'assets/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.transitionBlackToWhite = [loadImages(f'assets/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        self.bg = self.loadBackgroundImages()

        self.player1Score = 0
        self.player2Score = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)

        self.tokens={}

        self.gridBg= self.createbgimg()

        self.gridLogic=self.regenGrid(self.y,self.x)

    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)

    def loadBackgroundImages(self):
        alpha="ABCDEFGHI"
        spriteSheet = pygame.image.load('assets/wood.png').convert_alpha()
        imageDict={}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)]=loadSpriteSheet(spriteSheet,j,i,(self.size),(32,32))

        return imageDict
    
    def createbgimg(self):
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image=pygame.Surface((960,960))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img],(i*self.size[0],j*self.size[1]))

        return image


    def regenGrid(self,rows,columns):
        """
        Generate an empty grid
        """
        grid=[]
        for _ in range(rows):
            line=[]
            for _ in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid
    
    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line=f'{i} |'.ljust(3," ")
            for item in row:
                line+=f"{item}".center(3, " ")+'|'
            print(line)
        print()

    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        window.blit(self.drawScore('White', self.player1Score), (900, 100))
        window.blit(self.drawScore('Black', self.player2Score), (900, 200))

        for token in self.tokens.values():
            token.draw(window)

        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        if self.GAME.currentPlayer == 1:
            for move in availMoves:
                pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))


    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def findValidCells(self,grid,currPlayer):
        """
        Performs a check to find all empty cells that are adjacent to opposing player
        """
        validCellToCheck=[]
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                # If the cell is not empty, don't add it to the list
                if grid[gridX][gridY]!=0:
                    continue
                DIRECTIONS=directions(gridX,gridY)

                for direction in DIRECTIONS:
                    dirX, dirY=direction
                    checkedCell=grid[dirX][dirY]

                    if checkedCell==0 or checkedCell == currPlayer:
                        continue

                    if (gridX,gridY) in validCellToCheck:
                        continue

                    validCellToCheck.append((gridX,gridY))

        return validCellToCheck
    
    def swappableTiles(self,x,y,grid,player):
        surroundCells=directions(x,y)
        if len(surroundCells)==0:
            return []
        
        swappableTiles=[]
        for checkCell in surroundCells:
            checkX, checkY=checkCell
            diffX, diffY=checkX-x, checkY-y
            currentLine=[]

            RUN=True
            while RUN:
                if grid[checkX][checkY]==player*-1:
                    currentLine.append((checkX,checkY))

                elif grid[checkX][checkY]==player:
                    RUN=False
                    break

                elif grid[checkX][checkY]==0:
                    currentLine.clear()
                    RUN=False

                checkX+=diffX
                checkY+=diffY

                if checkX<0 or checkX>7 or checkY < 0 or checkY>7:
                    currentLine.clear()
                    RUN=False

            if len(currentLine)>0:
                swappableTiles.extend(currentLine)

        return swappableTiles

    def findAvailMoves(self,grid,currentPlayer):
        """
        Takes the list of validCells and checks each to see if playable
        """
        validCells=self.findValidCells(grid,currentPlayer)
        playableCells=[]

        for cell in validCells:
            x,y = cell
            if cell in playableCells:
                continue
            swapTiles=self.swappableTiles(x,y,grid,currentPlayer)

            if len(swapTiles)>0:
                playableCells.append(cell)

        return playableCells
    
    def animateTransitions(self,cell,player):
        if player ==1:
            self.tokens[(cell[0],cell[1])].transition(self.transitionWhiteToBlack,self.whitetoken)
        else:
            self.tokens[(cell[0],cell[1])].transition(self.transitionBlackToWhite,self.blacktoken)

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        textImg = self.font.render(f'{player} : {score}', 1, 'White')
        return textImg
    
    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            endText = self.font.render(f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1, 'White')
            endScreenImg.blit(endText, (0, 0))
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')
            endScreenImg.blit(newGameText, (120, 190))
        return endScreenImg