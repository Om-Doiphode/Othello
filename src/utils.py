import pygame

def loadImages(path,size):
    """
    Load an image into the game, and scale the image
    """
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img,size)
    return img

def loadSpriteSheet(sheet,row,col,newSize,size):
    """
    Creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img.
    """
    image = pygame.Surface((32,32)).convert_alpha()
    image.blit(sheet,(0,0),(row*size[0],col*size[1],size[0],size[1]))
    image = pygame.transform.scale(image,newSize)
    image.set_colorkey('Black')
    return image

def directions(x,y,minX=0,minY=0,maxX=7,maxY=7):
    """
    Check to determine which directions are valid from current cell
    """
    validDirections=[]
    if x!=minX: # North
        validDirections.append((x-1,y))
    if x!=minX and y!=minY: # North West
        validDirections.append((x-1,y-1))
    if x!=minX and y!=maxY: # North East
        validDirections.append((x-1,y+1))

    if x!=maxX: #South
        validDirections.append((x+1,y))
    if x!=maxX and y!=minY: #South west
        validDirections.append((x+1,y-1))
    if x!=maxX and y!=maxY: # South east
        validDirections.append((x+1,y+1))

    if y!=minY: #West
        validDirections.append((x,y-1))
    if y!=maxY: #East
        validDirections.append((x,y+1))

    return validDirections

def evaluateBoard(grid, player):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score
