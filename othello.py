import random
import pygame
import copy
from utils import loadImages,loadSpriteSheet,directions
from grid import Grid
from tokens import Token
from computer import ComputerPlayer

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100,800))
        pygame.display.set_caption("Othello")

        self.player1=1
        self.player2=-1

        self.currentPlayer=1

        self.time=0

        self.rows=8
        self.columns=8

        self.gameOver=False

        self.grid=Grid(self.rows, self.columns,(80,80),self)
        self.computerPlayer=ComputerPlayer(self.grid)

        self.RUN=True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button==1:
                    if self.currentPlayer==1 and not self.gameOver:
                        x,y=pygame.mouse.get_pos()
                        x,y=(x-80)//80, (y-80)//80
                        validCells=self.grid.findAvailMoves(self.grid.gridLogic,self.currentPlayer)
                        if not validCells:
                            pass
                        else:
                            if (y,x) in validCells:
                                self.grid.insertToken(self.grid.gridLogic,self.currentPlayer,y,x)
                                swappableTiles=self.grid.swappableTiles(y,x,self.grid.gridLogic,self.currentPlayer)
                                for tile in swappableTiles:
                                    self.grid.animateTransitions(tile,self.currentPlayer)
                                    self.grid.gridLogic[tile[0]][tile[1]]*=-1
                                self.currentPlayer*=-1
                                self.time=pygame.time.get_ticks()

                    if self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            self.gameOver = False

    def update(self):
        if self.currentPlayer == -1:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 1000:
                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.gameOver = True
                    return
                cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, 5, -64, 64, -1)
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                swappableTiles = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)
                for tile in swappableTiles:
                    self.grid.animateTransitions(tile, self.currentPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                self.currentPlayer *= -1

        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)
        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            self.gameOver = True
            return

    def draw(self):
        self.screen.fill((0,0,0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()
