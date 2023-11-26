import copy
from utils import evaluateBoard

class ComputerPlayer:
    def __init__(self,gridObject):
        self.grid=gridObject

    def computerHard(self,grid,depth,alpha,beta,player):
        newGrid=copy.deepcopy(grid)
        availMoves=self.grid.findAvailMoves(newGrid,player)

        if depth==0 or len(availMoves)==0:
            bestMove, Score=None, evaluateBoard(grid,player)
            return bestMove, Score
        
        if player<0:
            bestScore=-64
            bestMove=None

            for move in availMoves:
                x,y = move
                swappableTiles=self.grid.swappableTiles(x,y,newGrid,player)
                newGrid[x][y]=player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]]=player

                bMove,value=self.computerHard(newGrid,depth-1,alpha,beta,player*-1)

                if value>bestScore:
                    bestScore=value
                    bestMove=move
                alpha=max(alpha,bestScore)
                if beta<=alpha:
                    break

                newGrid=copy.deepcopy(grid)
            return bestMove, bestScore
        
        if player>0:
            bestScore=46
            bestMove=None

            for move in availMoves:
                x,y=move
                swappableTiles=self.grid.swappableTiles(x,y,newGrid,player)
                newGrid[x][y]=player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]]=player

                    bMove, value=self.computerHard(newGrid,depth-1,alpha,beta,player*-1)

                    if value<bestScore:
                        bestScore=value
                        bestMove=move
                    beta=min(beta,bestScore)
                    if beta<=alpha:
                        break

                    newGrid=copy.deepcopy(grid)
                return bestMove, bestScore