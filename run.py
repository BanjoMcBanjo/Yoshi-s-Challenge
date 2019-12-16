import sys, pygame, random, math
import time
from pygame import *
from pygame.locals import *
from pygame.sprite import *

# .SPLIT method?

# Color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 255)
BROWN = (181, 101, 29)
LIGHTGRAY = (160, 160, 160)
LIGHTYELLOW = (250, 218, 94)

# Basic board setup
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 60
HOLESWIDTH = 4
HOLESHEIGHT = 4

XMARGIN = int((WINDOWWIDTH - (BOXSIZE * HOLESWIDTH + (HOLESWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOXSIZE * HOLESHEIGHT + (HOLESHEIGHT - 1))) / 2)

# Tile Plan: Each Block/Tile will be an object constructed in a "Tile" class. Constructor can include a boolean to
# determine the type of tile. Determination of where each block is located on the board can be done through text
# parsing, and then the constructor can be called to.

# 1 BLOCK THAT CHANGES MOVEMENT

# O = Open Tile: Regular tile that can be walked on normally - DONE
# W = Wall Tile: Regular wall tile that blocks movement - DONE
# Z = Zone Tile: Outer tile to surround actual game board and prevent out of bounds errors - DONE
# E = Egg Tile: Acts like open tile, but adds egg to inventory. Eggs must be collected to reach end and win round
# A = Water Tile: Acts like wall tile without flippers; Acts like open tile with flippers - VISUAL
# F = Fire Tile: Acts like wall tile without boots; Acts like open tile with boots - VISUAL
# I = Ice Tile: Can be walked on, but without correct item causes uncontrollable movement - DONE
# y = Yellow Coin Tile: Coin that opens doors (part of inventory)
# r = Yellow Coin Tile: Coin that opens doors (part of inventory)
# f = Flower Tile: Flower that opens doors (part of inventory)
# s = Star Sprite: Star that opens doors (part of inventory)
# H = Hint Tile: Acts like open tile, but when stepped on reveals a popup hint
# M = Movable Tile: Tile that can be moved when on a "ground" tile an becomes an open tile when placed in water
# B = Bubble Tile: Bubble that allows movement on water (part of inventory)
# b = Boot Tile: Boot that allows movement on fire (part of inventory)
# T = Temp Wall Tile: Acts like a wall until sufficient eggs are collected, at which point it disappears. - SEMI-DONE
# 1 = Mario Tile: End point tile - acts like an open tile, but results in a successful game if walked on. - VISUAL
# 2 = Shy Guy Tile: Tile that has an enemy shy guy sprite and kills when the player is on it.
# 3 = Door 1: Can be opened with a yellow coin
# 4 = Door 2: Can be opened with a red coin
# 5 = Door 3: Can be opened with a flower
# 6 = Door 4: Can be opened with a star
# t = Trap Tile: Looks like a regular open tile, but kills if walked on

pygame.init()


# Yoshi sprite object
class Yoshi(pygame.sprite.Sprite):

    # "Constructor" of the Yoshi sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        yoshiImage = pygame.image.load("YoshiSprite.png")
        yoshiImageSized = pygame.transform.scale(yoshiImage, (100, 100))
        self.image = yoshiImageSized
        self.rect = self.image.get_rect(topleft=(350, 350))


class Dirt(pygame.sprite.Sprite):

    # "Constructor" of the Ground sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("DirtSprite.jpg")
        imageSized = pygame.transform.scale(image, (100, 100))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x, y))

class Wall(pygame.sprite.Sprite):

    # "Constructor" of the Ground sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("DirtSprite.jpg")
        imageSized = pygame.transform.scale(image, (100, 100))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class Egg(pygame.sprite.Sprite):

    # "Constructor" of the Egg sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        eggImage = pygame.image.load("EggSprite.png")
        eggImageSized = pygame.transform.scale(eggImage, (50, 50))
        self.image = eggImageSized
        self.rect = self.image.get_rect(topleft=(x + 25, y + 25))


class BabyMario(pygame.sprite.Sprite):

    # "Constructor" of the Baby Mario sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        babyImage = pygame.image.load("BabyMarioSprite.png")
        babyImageSized = pygame.transform.scale(babyImage, (80, 80))
        self.image = babyImageSized
        self.rect = self.image.get_rect(topleft=(x + 10, y + 10))


class Water(pygame.sprite.Sprite):

    # "Constructor" of the Water sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("WaterSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class Ice(pygame.sprite.Sprite):

    # "Constructor" of the Ice sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("IceSprite.png")
        imageSized = pygame.transform.scale(image, (100, 100))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class Fire(pygame.sprite.Sprite):

    # "Constructor" of the Fire sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("FireSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class YellowCoin(pygame.sprite.Sprite):

    # "Constructor" of the Coin sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("YellowCoinSprite.png")
        imageSized = pygame.transform.scale(image, (60, 60))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


class RedCoin(pygame.sprite.Sprite):

    # "Constructor" of the Coin sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("RedCoinSprite.png")
        imageSized = pygame.transform.scale(image, (60, 60))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


class Flower(pygame.sprite.Sprite):

    # "Constructor" of the Flower sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("FlowerSprite.png")
        imageSized = pygame.transform.scale(image, (60, 60))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


class Star(pygame.sprite.Sprite):

    # "Constructor" of the Flower sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("StarSprite.png")
        imageSized = pygame.transform.scale(image, (60, 60))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


class Hint(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("HintSprite.png")
        imageSized = pygame.transform.scale(image, (100, 100))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class ShyGuy(pygame.sprite.Sprite):

    # "Constructor" of the Shy Guy (ENEMY) sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        shyGuyImage = pygame.image.load("ShyGuySprite.png")
        shyGuySized = pygame.transform.scale(shyGuyImage, (80, 80))
        self.image = shyGuySized
        self.rect = self.image.get_rect(topleft=(x + 10, y + 10))


class DoorY(pygame.sprite.Sprite):

    # "Constructor" of the Yellow Coin Door
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("DoorSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class DoorR(pygame.sprite.Sprite):

    # "Constructor" of the Red Coin Door
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("DoorSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class DoorF(pygame.sprite.Sprite):

    # "Constructor" of the Flower Door
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("DoorSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class DoorS(pygame.sprite.Sprite):

    # "Constructor" of the Star Door
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        waterImage = pygame.image.load("DoorSprite.png")
        waterImageSized = pygame.transform.scale(waterImage, (100, 100))
        self.image = waterImageSized
        self.rect = self.image.get_rect(topleft=(x, y))


class Bubble(pygame.sprite.Sprite):

    # "Constructor" of the Bubble sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        eggImage = pygame.image.load("BubbleSprite.png")
        eggImageSized = pygame.transform.scale(eggImage, (60, 60))
        self.image = eggImageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


class Boot(pygame.sprite.Sprite):

    # "Constructor" of the Boot sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        eggImage = pygame.image.load("BootSprite.png")
        eggImageSized = pygame.transform.scale(eggImage, (60, 60))
        self.image = eggImageSized
        self.rect = self.image.get_rect(topleft=(x + 20, y + 20))


def drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF):
    for a in range(0, 7):
        for b in range(0, 7):
            if currentMatrix[a + startTempX][b + startTempY] == 'O':  # Open Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
            elif currentMatrix[a + startTempX][b + startTempY] == 'W':  # Wall Tile
                pygame.draw.rect(DISPLAYSURF, WHITE, (50 + (b * 100), 50 + (a * 100), 100, 100))
                wall_sprite = Wall(50 + (b * 100), 50 + (a * 100))
                wallSpriteGroup = Group(wall_sprite)
                wallSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'Z':  # Zone Wall Tile
                pygame.draw.rect(DISPLAYSURF, GREEN, (50 + (b * 100), 50 + (a * 100), 100, 100))
            elif currentMatrix[a + startTempX][b + startTempY] == 'E':  # Egg Sprite/Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                egg_sprite = Egg(50 + (b * 100), 50 + (a * 100))
                eggSpriteGroup = Group(egg_sprite)
                eggSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '1':  # Baby Mario Sprite/Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                mario_sprite = BabyMario(50 + (b * 100), 50 + (a * 100))
                marioSpriteGroup = Group(mario_sprite)
                marioSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '2':  # Shy Guy Tile - NEEDS BETTER FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                shy_guy_sprite = ShyGuy(50 + (b * 100), 50 + (a * 100))
                shyGuyGroup = Group(shy_guy_sprite)
                shyGuyGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'T':  # Destination Wall Tile
                pygame.draw.rect(DISPLAYSURF, RED, (50 + (b * 100), 50 + (a * 100), 100, 100))
            elif currentMatrix[a + startTempX][b + startTempY] == 'A':  # Water Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                water_sprite = Water(50 + (b * 100), 50 + (a * 100))
                waterSpriteGroup = Group(water_sprite)
                waterSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'F':  # Fire Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                fire_sprite = Fire(50 + (b * 100), 50 + (a * 100))
                fireSpriteGroup = Group(fire_sprite)
                fireSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'F':  # Fire Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                fire_sprite = Fire(50 + (b * 100), 50 + (a * 100))
                fireSpriteGroup = Group(fire_sprite)
                fireSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'I':  # Ice Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                ice_sprite = Ice(50 + (b * 100), 50 + (a * 100))
                iceSpriteGroup = Group(ice_sprite)
                iceSpriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'y':  # Yellow Coin Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = YellowCoin(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'f':  # Flower Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = Flower(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'r':  # Red Coin Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = RedCoin(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 's':  # Star Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = Star(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'B':  # Bubble Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = Bubble(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'b':  # Boot Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = Boot(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 'H':  # Hint Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = Hint(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '3':  # Door (Y) Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = DoorY(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '4':  # Door (R) Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = DoorR(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '5':  # Door (F) Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = DoorF(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == '6':  # Door (S) Tile - NEEDS FUNCTIONALITY
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))
                sprite = DoorS(50 + (b * 100), 50 + (a * 100))
                spriteGroup = Group(sprite)
                spriteGroup.draw(DISPLAYSURF)
            elif currentMatrix[a + startTempX][b + startTempY] == 't':  # Trap Tile
                pygame.draw.rect(DISPLAYSURF, BROWN, (50 + (b * 100), 50 + (a * 100), 100, 100))


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def main():
    global scoreNum, eggsRemNum

    # Initial SPRITE setup
    yoshi_sprite = Yoshi()
    playerSpriteGroup = Group(yoshi_sprite)

    # Initial DISPLAY setup
    DISPLAYSURF = pygame.display.set_mode((1000, 800))
    DISPLAYSURF.fill(LIGHTGRAY)
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, 800, 800))
    pygame.display.set_caption("Yoshi's Challenge")

    # Tile board setup for level 1
    level1 = open("level1.txt")
    matrix1 = []
    for line in level1:
        matrix1.append(line.rstrip().split())

    # Tile board setup for level 2
    level2 = open("level2.txt")
    matrix2 = []
    for line in level2:
        matrix2.append(line.rstrip().split())

    # Tile board setup for level 3 (WALL OVERLAY FOR LEVEL 2)
    level3 = open("level3.txt")
    matrix3 = []
    for line in level3:
        matrix3.append(line.rstrip().split())

    startTempX = 9
    startTempY = 9

    # Timer initial setup
    clock = pygame.time.Clock()

    # Font setup
    BASICFONT = pygame.font.Font('freesansbold.ttf', 15)

    # START setup (including button)
    pressedStart = False
    startButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 20, 65, 30))
    timeText = "START!"
    theTimeText = BASICFONT.render(timeText, True, WHITE)
    DISPLAYSURF.blit(theTimeText, (820, 30))

    # PAUSE setup (including button)
    pressedPause = False
    pauseButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 60, 60, 30))
    pauseText = "PAUSE"
    theTimeText = BASICFONT.render(pauseText, True, WHITE)
    DISPLAYSURF.blit(theTimeText, (820, 70))

    # Timer display setup
    timeText = "Time Remaining:"
    theTimeText = BASICFONT.render(timeText, True, WHITE)
    DISPLAYSURF.blit(theTimeText, (820, 100))

    # Eggs Remaining setup
    eggsText = "Eggs Remaining:"
    theEggsText = BASICFONT.render(eggsText, True, WHITE)
    DISPLAYSURF.blit(theEggsText, (820, 160))

    # Inventory Setup
    inventoryText = "Inventory:"
    theInventoryText = BASICFONT.render(inventoryText, True, WHITE)
    DISPLAYSURF.blit(theInventoryText, (820, 220))

    xLocation = 820
    yLocation = 250
    for a in range(3):
        for b in range(2):
            pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))

    # Level Select Setup
    levelText = "Level Select:"
    theLevelText = BASICFONT.render(levelText, True, WHITE)
    DISPLAYSURF.blit(theLevelText, (820, 680))

    # Buttons for Level Select Setup
    for a in range(3):
        level1Button = pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (0 * 60)), 700, 50, 50))
        level2Button = pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (1 * 60)), 700, 50, 50))
        levelNum1 = str(1)
        levelNum2 = str(2)
        theLevelNum1 = BASICFONT.render(levelNum1, True, BLACK)
        theLevelNum2 = BASICFONT.render(levelNum2, True, BLACK)
        DISPLAYSURF.blit(theLevelNum1, (840 + (0 * 60), 720))
        DISPLAYSURF.blit(theLevelNum2, (840 + (1 * 60), 720))

    # Level time indicates the starting time for each level
    levelTime1 = 60  # levelTime will have to be changed between levels
    levelTime2 = 50
    levelTimeUsed = levelTime1

    timeStep = levelTime1  # Designates starting time step; To be changed with multiple levels

    frame = 0

    # Initiates enemy sprite array (customized for each level)
    enemyArr1S1 = [1, 2, 3, 4] # Left
    enemyArr1S2 = [1, 2, 3, 4] # Top
    enemyArr1S3 = [1, 2, 3, 4] # Right

    # Initiates the player location
    playerX = startTempX + 3
    playerY = startTempY + 3

    # Initializes number of eggs remaining (varies per level)
    level1EggsRem = 4
    level2EggsRem = 8
    levelEggsRemArr = [level1EggsRem, level2EggsRem]

    # Initializes value used to indicate how many eggs there are
    eggArrayUsed = 0

    # Initializes inventory possessions
    hasYellowCoin = False
    hasRedCoin = False
    hasFlower = False
    hasStar = False
    hasBubble = False  # For Water
    hasBoots = False  # For Fire

    # Determines if the player has landed on a "killing" tile, and if the player has won
    youDied = False
    youWin = False

    # Copy of the level array currently in use
    currentMatrix = []

    # Initializes level select booleans
    level1Active = True
    level2Active = False

    level1Hint = False
    level2Hint = False

    # runThrough determines if current board represents correct level; drawCurrentBoard determines if it's been drawn
    # once. These two should go together for level changes and restarts
    runThrough = False
    drawCurrentBoard = True

    while True:

        playerSpriteGroup.draw(DISPLAYSURF)

        # Level boards must be squares
        if level1Active is True and runThrough is False:
            levelTimeUsed = levelTime1
            runThrough = True
            eggArrayUsed = 0
            level1 = open("level1.txt")
            for line in level1:
                currentMatrix.append(line.rstrip().split())
            print("This One")
            # FIX SHY GUY
        elif level2Active is True and runThrough is False:
            levelTimeUsed = levelTime2
            runThrough = True
            eggArrayUsed = 1
            level2 = open("level2.txt")
            for line in level2:
                currentMatrix.append(line.rstrip().split())
            print("This Two")

        # print(currentMatrix)

        # Draws part of the board that's visible
        if drawCurrentBoard is True:
            drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
            drawCurrentBoard = False

        if level2Active is True:
            drawBoard(matrix3, startTempX, startTempY, DISPLAYSURF)
            playerSpriteGroup.draw(DISPLAYSURF)

        # print(matrix1[3][3])

        # print(truncate(frame))
        # Time number setup (constantly updating)
        if pressedStart is True:
            frame += (1 / 12)
            timeStep = truncate(levelTimeUsed - frame)
            # startingValue = levelTime1 - truncate(timeTicksTemp / 1000)
            # timeStep = (startingValue + 1) - truncate((pygame.time.get_ticks() - start_ticks) / 1000)
            # print(startingValue)
            if level1Active is True:
                if abs(enemyArr1S1[0] - frame) <= 0.0000001:
                    enemyArr1S1[0] += 4
                    currentMatrix[12][8] = '2'
                    currentMatrix[11][8] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S1[1] - frame) <= 0.0000001:
                    enemyArr1S1[1] += 4
                    currentMatrix[13][8] = '2'
                    currentMatrix[12][8] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S1[2] - frame) <= 0.0000001:
                    enemyArr1S1[2] += 4
                    currentMatrix[12][8] = '2'
                    currentMatrix[13][8] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S1[3] - frame) <= 0.0000001:
                    enemyArr1S1[3] += 4
                    currentMatrix[11][8] = '2'
                    currentMatrix[12][8] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)

                if abs(enemyArr1S2[0] - frame) <= 0.0000001:
                    enemyArr1S2[0] += 4
                    currentMatrix[8][12] = '2'
                    currentMatrix[8][11] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S2[1] - frame) <= 0.0000001:
                    enemyArr1S2[1] += 4
                    currentMatrix[8][13] = '2'
                    currentMatrix[8][12] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S2[2] - frame) <= 0.0000001:
                    enemyArr1S2[2] += 4
                    currentMatrix[8][12] = '2'
                    currentMatrix[8][13] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S2[3] - frame) <= 0.0000001:
                    enemyArr1S2[3] += 4
                    currentMatrix[8][11] = '2'
                    currentMatrix[8][12] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)

                if abs(enemyArr1S3[0] - frame) <= 0.0000001:
                    enemyArr1S3[0] += 4
                    currentMatrix[12][16] = '2'
                    currentMatrix[11][16] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S3[1] - frame) <= 0.0000001:
                    enemyArr1S3[1] += 4
                    currentMatrix[13][16] = '2'
                    currentMatrix[12][16] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S3[2] - frame) <= 0.0000001:
                    enemyArr1S3[2] += 4
                    currentMatrix[12][16] = '2'
                    currentMatrix[13][16] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                elif abs(enemyArr1S3[3] - frame) <= 0.0000001:
                    enemyArr1S3[3] += 4
                    currentMatrix[11][16] = '2'
                    currentMatrix[12][16] = 'O'
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)

        timeNumberText = str(timeStep)
        theTimeNumberText = BASICFONT.render(timeNumberText, True, WHITE)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (820, 125, 220, 30))
        DISPLAYSURF.blit(theTimeNumberText, (820, 125))

        # Eggs remaining counter setup
        eggRemText = str(levelEggsRemArr[eggArrayUsed])
        theEggRemText = BASICFONT.render(eggRemText, True, WHITE)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (820, 185, 220, 30))
        DISPLAYSURF.blit(theEggRemText, (820, 185))

        # If all/enough eggs are created, wall blocking destination disappears
        if levelEggsRemArr[eggArrayUsed] == 0:  # FIX EGGS FOR CURRENTMATRIX
            for a in range(len(currentMatrix)):
                for b in range(len(currentMatrix[0])):
                    if currentMatrix[a][b] == "T":
                        currentMatrix[a][b] = "O"

        # Exits the program if time runs out
        if timeStep <= -1:
            timeUpText = "TIME'S UP"
            gameOverText = "GAME OVER"
            theTimeUpText = BASICFONT.render(timeUpText, True, WHITE)
            theGameOverText = BASICFONT.render(gameOverText, True, WHITE)
            pygame.draw.rect(DISPLAYSURF, BLACK, (330, 180, 200, 120))
            DISPLAYSURF.blit(theTimeUpText, (370, 200))
            DISPLAYSURF.blit(theGameOverText, (370, 250))
            pressedStart = False

        # If a killing tile is landed on, this runs
        if youDied is True:
            BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
            youDiedText = "YOU DIED"
            gameOverText = "GAME OVER"
            theYouDiedText = BASICFONT.render(youDiedText, True, WHITE)
            theGameOverText = BASICFONT.render(gameOverText, True, WHITE)
            pygame.draw.rect(DISPLAYSURF, BLACK, (330, 180, 200, 120))
            DISPLAYSURF.blit(theYouDiedText, (370, 200))
            DISPLAYSURF.blit(theGameOverText, (370, 250))
            pressedStart = False

        # If you make contact with an enemy sprite, game over
        if currentMatrix[playerX][playerY] == '2':
            youDied = True

        # If you make contact with Baby Mario, you win and this runs
        if youWin is True:
            BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
            youDiedText = "YOU WIN!!!!"
            pointsText = "Final Score: " + str(timeStep * 1000)
            theYouDiedText = BASICFONT.render(youDiedText, True, WHITE)
            thePointsText = BASICFONT.render(pointsText, True, WHITE)
            pygame.draw.rect(DISPLAYSURF, BLACK, (330, 180, 220, 120))
            DISPLAYSURF.blit(theYouDiedText, (370, 200))
            DISPLAYSURF.blit(thePointsText, (370, 250))
            pressedStart = False

        if level1Hint is True:
            BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
            text1 = "Here we have one key, but there are many doors."
            text2 = "I wonder which one this key will open..."
            theYouDiedText = BASICFONT.render(text1, True, WHITE)
            theGameOverText = BASICFONT.render(text2, True, WHITE)
            pygame.draw.rect(DISPLAYSURF, BLACK, (330, 180, 400, 120))
            DISPLAYSURF.blit(theYouDiedText, (370, 200))
            DISPLAYSURF.blit(theGameOverText, (370, 250))

        if level2Hint is True:
            BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
            text1 = "There is a way to succeed"
            text2 = "You just need to find the right path..."
            theYouDiedText = BASICFONT.render(text1, True, WHITE)
            theGameOverText = BASICFONT.render(text2, True, WHITE)
            pygame.draw.rect(DISPLAYSURF, BLACK, (330, 180, 400, 120))
            DISPLAYSURF.blit(theYouDiedText, (370, 200))
            DISPLAYSURF.blit(theGameOverText, (370, 250))

        for event in pygame.event.get():

            if pygame.mouse.get_pressed()[0] and startButton.collidepoint(pygame.mouse.get_pos()):
                pressedStart = True  # Checks if START button was clicked - causes START button to become a CONTINUE and
                # creates a RESTART BUTTON
                continueButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 20, 90, 30))
                continueText = "CONTINUE"
                theContinueText = BASICFONT.render(continueText, True, WHITE)
                DISPLAYSURF.blit(theContinueText, (820, 30))

                restartButton = pygame.draw.rect(DISPLAYSURF, BLUE, (915, 20, 80, 30))
                restartText = "RESTART"
                theRestartText = BASICFONT.render(restartText, True, WHITE)
                DISPLAYSURF.blit(theRestartText, (920, 30))

            if pygame.mouse.get_pressed()[0] and pauseButton.collidepoint(pygame.mouse.get_pos()):
                if pressedStart is True:  # Checks if PAUSE button was clicked - Makes timer stagnant and prevents most
                    # other player actions
                    pressedStart = False

            if pygame.mouse.get_pressed()[0] and continueButton.collidepoint(pygame.mouse.get_pos()):
                if pressedStart is False:
                    pressedStart = True

            if pygame.mouse.get_pressed()[0] and restartButton.collidepoint(pygame.mouse.get_pos()):
                # CHECKS IF THE RESTART BUTTON WAS CLICKED - DOES A LOT
                frame = 0
                timeStep = levelTimeUsed
                pressedStart = False
                youDied = False
                youWin = False
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (915, 20, 80, 30))
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (815, 20, 90, 30))
                startButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 20, 65, 30))
                timeText = "START!"
                theTimeText = BASICFONT.render(timeText, True, WHITE)
                DISPLAYSURF.blit(theTimeText, (820, 30))
                xLocation = 820
                yLocation = 250
                for a in range(3):
                    for b in range(2):
                        pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))
                hasYellowCoin = False
                hasRedCoin = False
                hasFlower = False
                hasStar = False
                hasBubble = False  # For Water
                hasBoots = False  # For Fire
                level1Hint = False
                level2Hint = False
                enemyArr1S1 = [1, 2, 3, 4]
                enemyArr1S2 = [1, 2, 3, 4]
                enemyArr1S3 = [1, 2, 3, 4]

                if level1Active is True:
                    levelEggsRemArr[eggArrayUsed] = 4
                    for a in range(len(matrix1)):
                        for b in range(len(matrix1[0])):
                            currentMatrix[a][b] = matrix1[a][b]
                    startTempX = 9
                    startTempY = 9
                    playerX = startTempX + 3
                    playerY = startTempY + 3
                elif level2Active is True:
                    levelEggsRemArr[eggArrayUsed] = 8
                    for a in range(len(matrix2)):
                        for b in range(len(matrix2[0])):
                            currentMatrix[a][b] = matrix2[a][b]
                    startTempX = 1
                    startTempY = 1
                    playerX = startTempX + 3
                    playerY = startTempY + 3

                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                playerSpriteGroup.draw(DISPLAYSURF)

            # Can only select different levels during pause
            if pygame.mouse.get_pressed()[0] and level1Button.collidepoint(
                    pygame.mouse.get_pos()) and pressedStart is False:
                for a in range(5):
                    for b in range(2):
                        pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))

                newCurrentMatrix = []

                levelTimeUsed = levelTime1

                level1Active = True
                level2Active = False
                level3Active = False

                frame = 0
                timeStep = levelTime1
                pressedStart = False
                youDied = False
                youWin = False
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (915, 20, 80, 30))
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (815, 20, 90, 30))
                startButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 20, 65, 30))
                timeText = "START!"
                theTimeText = BASICFONT.render(timeText, True, WHITE)
                DISPLAYSURF.blit(theTimeText, (820, 30))
                xLocation = 820
                yLocation = 250
                for a in range(3):
                    for b in range(2):
                        pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))
                hasYellowCoin = False
                hasRedCoin = False
                hasFlower = False
                hasStar = False
                hasBubble = False  # For Water
                hasBoots = False  # For Fire
                level1Hint = False
                level2Hint = False
                enemyArr1S1 = [1, 2, 3, 4]
                enemyArr1S2 = [1, 2, 3, 4]
                enemyArr1S3 = [1, 2, 3, 4]

                startTempX = 9
                startTempY = 9
                playerX = startTempX + 3
                playerY = startTempY + 3

                youDied = False

                eggArrayUsed = 0
                level1 = open("level1.txt")
                for line in level1:
                    newCurrentMatrix.append(line.rstrip().split())

                for a in range(len(matrix1)):
                    for b in range(len(matrix1[0])):
                        currentMatrix[a][b] = newCurrentMatrix[a][b]

                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)

            if pygame.mouse.get_pressed()[0] and level2Button.collidepoint(
                    pygame.mouse.get_pos()) and pressedStart is False:
                for a in range(5):
                    for b in range(2):
                        pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))

                newCurrentMatrix = []

                level1Active = False
                level2Active = True

                frame = 0
                levelTimeUsed = levelTime2
                timeStep = levelTime2
                pressedStart = False
                youDied = False
                youWin = False
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (915, 20, 80, 30))
                pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (815, 20, 90, 30))
                startButton = pygame.draw.rect(DISPLAYSURF, BLUE, (815, 20, 65, 30))
                timeText = "START!"
                theTimeText = BASICFONT.render(timeText, True, WHITE)
                DISPLAYSURF.blit(theTimeText, (820, 30))
                xLocation = 820
                yLocation = 250
                for a in range(3):
                    for b in range(2):
                        pygame.draw.rect(DISPLAYSURF, WHITE, ((xLocation + (b * 80)), (yLocation + (a * 80)), 70, 70))
                hasYellowCoin = False
                hasRedCoin = False
                hasFlower = False
                hasStar = False
                hasBubble = False  # For Water
                hasBoots = False  # For Fire
                level1Hint = False
                level2Hint = False
                # enemyArr1S1 = [1, 2, 3, 4]
                # enemyArr1S2 = [1, 2, 3, 4]
                # enemyArr1S3 = [1, 2, 3, 4]

                startTempX = 1
                startTempY = 1
                playerX = startTempX + 3
                playerY = startTempY + 3

                eggArrayUsed = 1
                level2 = open("level2.txt")
                for line in level2:
                    newCurrentMatrix.append(line.rstrip().split())

                for a in range(len(matrix2)):
                    for b in range(len(matrix2[0])):
                        currentMatrix[a][b] = newCurrentMatrix[a][b]

                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)

            if event.type == KEYUP:

                # Check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a):

                    # Functionality for wall and destination wall
                    if currentMatrix[playerX][playerY - 1] != 'W' and currentMatrix[playerX][playerY - 1] != 'T' and \
                            currentMatrix[playerX][playerY - 1] != 'I' and currentMatrix[playerX][
                        playerY - 1] != '3' and \
                            currentMatrix[playerX][playerY - 1] != '4' and currentMatrix[playerX][
                        playerY - 1] != '5' and \
                            currentMatrix[playerX][playerY - 1] != '6' and pressedStart is True:
                        playerY -= 1
                        startTempY -= 1
                        print("Going left")

                        # Functionality for eggs
                        if currentMatrix[playerX][playerY] == 'E':
                            levelEggsRemArr[eggArrayUsed] -= 1
                            currentMatrix[playerX][playerY] = 'O'

                        # If yellow coin is found
                        if currentMatrix[playerX][playerY] == 'y':
                            currentMatrix[playerX][playerY] = 'O'
                            hasYellowCoin = True
                            sprite = YellowCoin(805, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'r':
                            currentMatrix[playerX][playerY] = 'O'
                            hasRedCoin = True
                            sprite = RedCoin(880, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'f':
                            currentMatrix[playerX][playerY] = 'O'
                            hasFlower = True
                            sprite = Flower(805, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 's':
                            currentMatrix[playerX][playerY] = 'O'
                            hasStar = True
                            sprite = Star(885, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'B':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBubble = True
                            sprite = Bubble(805, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'b':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBoots = True
                            sprite = Boot(885, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'H':
                            if level1Active is True:
                                level1Hint = True
                            elif level2Active is True:
                                level2Hint = True

                        if currentMatrix[playerX][playerY] == 'A' and hasBubble is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == 'F' and hasBoots is False:
                            youDied = True

                        # Hit Shy Guy
                        if currentMatrix[playerX][playerY] == '2':
                            youDied = True

                        # Hit trap tile
                        if currentMatrix[playerX][playerY] == 't':
                            youDied = True

                        if currentMatrix[playerX][playerY] == '1':
                            youWin = True

                    elif currentMatrix[playerX][playerY - 1] == '3':
                        if hasYellowCoin is True:
                            currentMatrix[playerX][playerY - 1] = 'O'
                            playerY -= 1
                            startTempY -= 1
                    elif currentMatrix[playerX][playerY - 1] == '4':
                        if hasRedCoin is True:
                            currentMatrix[playerX][playerY - 1] = 'O'
                            playerY -= 1
                            startTempY -= 1
                    elif currentMatrix[playerX][playerY - 1] == '5':
                        if hasFlower is True:
                            currentMatrix[playerX][playerY - 1] = 'O'
                            playerY -= 1
                            startTempY -= 1
                    elif currentMatrix[playerX][playerY - 1] == '6':
                        if hasStar is True:
                            currentMatrix[playerX][playerY - 1] = 'O'
                            playerY -= 1
                            startTempY -= 1

                    elif currentMatrix[playerX][playerY - 1] == 'I':

                        iceAdvance = True
                        # i = 0
                        while iceAdvance is True:
                            if currentMatrix[playerX][playerY - 1] == 'I':
                                playerY -= 1
                                startTempY -= 1
                                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                                playerSpriteGroup.draw(DISPLAYSURF)
                                pygame.display.update()
                                pygame.time.wait(5)
                            elif currentMatrix[playerX][playerY - 1] == 'O':
                                playerY -= 1
                                startTempY -= 1
                                iceAdvance = False
                            elif currentMatrix[playerX][playerY - 1] == '2':
                                playerY -= 1
                                startTempY -= 1
                                iceAdvance = False
                                youDied = True
                            elif currentMatrix[playerX][playerY - 1] == 'E':
                                levelEggsRemArr[eggArrayUsed] -= 1
                                currentMatrix[playerX][playerY - 1] = 'O'
                                playerY -= 1
                                startTempY -= 1
                                iceAdvance = False
                            elif currentMatrix[playerX][playerY - 1] == 'F' and hasBoots is False:
                                playerY -= 1
                                startTempY -= 1
                                youDied = True
                            elif currentMatrix[playerX][playerY - 1] == 'W':
                                iceAdvance = False

                    if currentMatrix[playerX][playerY] != 'H':
                        level1Hint = False
                        level2Hint = False
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                    playerSpriteGroup.draw(DISPLAYSURF)

                elif event.key in (K_RIGHT, K_d):

                    if currentMatrix[playerX][playerY + 1] != 'W' and currentMatrix[playerX][playerY + 1] != 'T' and \
                            currentMatrix[playerX][playerY + 1] != 'I' and currentMatrix[playerX][
                        playerY + 1] != '3' and \
                            currentMatrix[playerX][playerY + 1] != '4' and currentMatrix[playerX][
                        playerY + 1] != '5' and \
                            currentMatrix[playerX][playerY + 1] != '6' and pressedStart is True:
                        playerY += 1
                        startTempY += 1
                        print("Going right")

                        if currentMatrix[playerX][playerY] == 'E':
                            levelEggsRemArr[eggArrayUsed] -= 1
                            currentMatrix[playerX][playerY] = 'O'

                        if currentMatrix[playerX][playerY] == 'y':
                            currentMatrix[playerX][playerY] = 'O'
                            hasYellowCoin = True
                            sprite = YellowCoin(805, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'r':
                            currentMatrix[playerX][playerY] = 'O'
                            hasRedCoin = True
                            sprite = RedCoin(880, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'f':
                            currentMatrix[playerX][playerY] = 'O'
                            hasFlower = True
                            sprite = Flower(805, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 's':
                            currentMatrix[playerX][playerY] = 'O'
                            hasStar = True
                            sprite = Star(885, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'B':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBubble = True
                            sprite = Bubble(805, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'b':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBoots = True
                            sprite = Boot(885, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'H':
                            if level1Active is True:
                                level1Hint = True
                            elif level2Active is True:
                                level2Hint = True

                        if currentMatrix[playerX][playerY] == 'A' and hasBubble is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == 'F' and hasBoots is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == '2':
                            youDied = True

                        if currentMatrix[playerX][playerY] == 't':
                            youDied = True

                        if currentMatrix[playerX][playerY] == '1':
                            youWin = True

                    elif currentMatrix[playerX][playerY + 1] == '3':
                        if hasYellowCoin is True:
                            currentMatrix[playerX][playerY + 1] = 'O'
                            playerY += 1
                            startTempY += 1
                    elif currentMatrix[playerX][playerY + 1] == '4':
                        if hasRedCoin is True:
                            currentMatrix[playerX][playerY + 1] = 'O'
                            playerY += 1
                            startTempY += 1
                    elif currentMatrix[playerX][playerY + 1] == '5':
                        if hasFlower is True:
                            currentMatrix[playerX][playerY + 1] = 'O'
                            playerY += 1
                            startTempY += 1
                    elif currentMatrix[playerX][playerY + 1] == '6':
                        if hasStar is True:
                            currentMatrix[playerX][playerY - 1] = 'O'
                            playerY += 1
                            startTempY += 1

                    elif currentMatrix[playerX][playerY + 1] == 'I':

                        iceAdvance = True
                        # i = 0
                        while iceAdvance is True:
                            if currentMatrix[playerX][playerY + 1] == 'I':
                                playerY += 1
                                startTempY += 1
                                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                                playerSpriteGroup.draw(DISPLAYSURF)
                                pygame.display.update()
                                pygame.time.wait(5)
                            elif currentMatrix[playerX][playerY + 1] == 'O':
                                playerY += 1
                                startTempY += 1
                                iceAdvance = False
                            elif currentMatrix[playerX][playerY + 1] == '2':
                                playerY += 1
                                startTempY += 1
                                iceAdvance = False
                                youDied = True
                            elif currentMatrix[playerX][playerY + 1] == 'E':
                                levelEggsRemArr[eggArrayUsed] -= 1
                                currentMatrix[playerX][playerY + 1] = 'O'
                                playerY += 1
                                startTempY += 1
                                iceAdvance = False
                            elif currentMatrix[playerX][playerY + 1] == 'F' and hasBoots is False:
                                playerY += 1
                                startTempY += 1
                                youDied = True
                            elif currentMatrix[playerX][playerY + 1] == 'W':
                                iceAdvance = False

                    if currentMatrix[playerX][playerY] != 'H':
                        level1Hint = False
                        level2Hint = False
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                    playerSpriteGroup.draw(DISPLAYSURF)


                elif event.key in (K_UP, K_w):

                    if currentMatrix[playerX - 1][playerY] != 'W' and currentMatrix[playerX - 1][playerY] != 'T' and \
                            currentMatrix[playerX - 1][playerY] != 'I' and currentMatrix[playerX - 1][
                        playerY] != '3' and \
                            currentMatrix[playerX - 1][playerY] != '4' and currentMatrix[playerX - 1][
                        playerY] != '5' and \
                            currentMatrix[playerX - 1][playerY] != '6' and pressedStart is True:
                        playerX -= 1
                        startTempX -= 1
                        print("Going up")

                        if currentMatrix[playerX][playerY] == 'E':
                            levelEggsRemArr[eggArrayUsed] -= 1
                            currentMatrix[playerX][playerY] = 'O'

                        if currentMatrix[playerX][playerY] == 'y':
                            currentMatrix[playerX][playerY] = 'O'
                            hasYellowCoin = True
                            sprite = YellowCoin(805, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'r':
                            currentMatrix[playerX][playerY] = 'O'
                            hasRedCoin = True
                            sprite = RedCoin(880, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'f':
                            currentMatrix[playerX][playerY] = 'O'
                            hasFlower = True
                            sprite = Flower(805, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 's':
                            currentMatrix[playerX][playerY] = 'O'
                            hasStar = True
                            sprite = Star(885, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'B':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBubble = True
                            sprite = Bubble(805, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'b':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBoots = True
                            sprite = Boot(885, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'H':
                            if level1Active is True:
                                level1Hint = True
                            elif level2Active is True:
                                level2Hint = True

                        if currentMatrix[playerX][playerY] == 'A' and hasBubble is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == 'F' and hasBoots is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == '2':
                            youDied = True

                        if currentMatrix[playerX][playerY] == 't':
                            youDied = True

                        if currentMatrix[playerX][playerY] == '1':
                            youWin = True

                    elif currentMatrix[playerX - 1][playerY] == '3':
                        if hasYellowCoin is True:
                            currentMatrix[playerX - 1][playerY] = 'O'
                            playerX -= 1
                            startTempX -= 1
                    elif currentMatrix[playerX - 1][playerY] == '4':
                        if hasRedCoin is True:
                            currentMatrix[playerX - 1][playerY] = 'O'
                            playerX -= 1
                            startTempX -= 1
                    elif currentMatrix[playerX - 1][playerY] == '5':
                        if hasFlower is True:
                            currentMatrix[playerX - 1][playerY] = 'O'
                            playerX -= 1
                            startTempX -= 1
                    elif currentMatrix[playerX - 1][playerY] == '6':
                        if hasStar is True:
                            currentMatrix[playerX - 1][playerY] = 'O'
                            playerX -= 1
                            startTempX -= 1

                    elif currentMatrix[playerX - 1][playerY] == 'I':

                        iceAdvance = True
                        # i = 0
                        while iceAdvance is True:
                            if currentMatrix[playerX - 1][playerY] == 'I':
                                playerX -= 1
                                startTempX -= 1
                                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                                playerSpriteGroup.draw(DISPLAYSURF)
                                pygame.display.update()
                                pygame.time.wait(5)
                            elif currentMatrix[playerX - 1][playerY] == 'O':
                                playerX -= 1
                                startTempX -= 1
                                iceAdvance = False
                            elif currentMatrix[playerX - 1][playerY] == '2':
                                playerX -= 1
                                startTempX -= 1
                                iceAdvance = False
                                youDied = True
                            elif currentMatrix[playerX - 1][playerY] == 'E':
                                levelEggsRemArr[eggArrayUsed] -= 1
                                currentMatrix[playerX - 1][playerY] = 'O'
                                playerX -= 1
                                startTempX -= 1
                                iceAdvance = False
                            elif currentMatrix[playerX - 1][playerY] == 'F' and hasBoots is False:
                                playerX -= 1
                                startTempX -= 1
                                youDied = True
                            elif currentMatrix[playerX - 1][playerY] == 'W':
                                iceAdvance = False

                    if currentMatrix[playerX][playerY] != 'H':
                        level1Hint = False
                        level2Hint = False
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                    playerSpriteGroup.draw(DISPLAYSURF)

                elif event.key in (K_DOWN, K_s):

                    if currentMatrix[playerX + 1][playerY] != 'W' and currentMatrix[playerX + 1][playerY] != 'T' and \
                            currentMatrix[playerX + 1][playerY] != 'I' and currentMatrix[playerX + 1][
                        playerY] != '3' and \
                            currentMatrix[playerX + 1][playerY] != '4' and currentMatrix[playerX + 1][
                        playerY] != '5' and \
                            currentMatrix[playerX + 1][playerY] != '6' and pressedStart is True:
                        playerX += 1
                        startTempX += 1
                        print("Going down")

                        if currentMatrix[playerX][playerY] == 'E':
                            levelEggsRemArr[eggArrayUsed] -= 1
                            currentMatrix[playerX][playerY] = 'O'

                        if currentMatrix[playerX][playerY] == 'y':
                            currentMatrix[playerX][playerY] = 'O'
                            hasYellowCoin = True
                            sprite = YellowCoin(805, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'r':
                            currentMatrix[playerX][playerY] = 'O'
                            hasRedCoin = True
                            sprite = RedCoin(880, 235)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'f':
                            currentMatrix[playerX][playerY] = 'O'
                            hasFlower = True
                            sprite = Flower(805, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 's':
                            currentMatrix[playerX][playerY] = 'O'
                            hasStar = True
                            sprite = Star(885, 315)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'B':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBubble = True
                            sprite = Bubble(805, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'b':
                            currentMatrix[playerX][playerY] = 'O'
                            hasBoots = True
                            sprite = Boot(885, 395)
                            spriteGroup = Group(sprite)
                            spriteGroup.draw(DISPLAYSURF)

                        if currentMatrix[playerX][playerY] == 'H':
                            if level1Active is True:
                                level1Hint = True
                            elif level2Active is True:
                                level2Hint = True

                        if currentMatrix[playerX][playerY] == 'A' and hasBubble is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == 'F' and hasBoots is False:
                            youDied = True

                        if currentMatrix[playerX][playerY] == '2':
                            youDied = True

                        if currentMatrix[playerX][playerY] == 't':
                            youDied = True

                        if currentMatrix[playerX][playerY] == '1':
                            youWin = True

                    elif currentMatrix[playerX + 1][playerY] == '3':
                        if hasYellowCoin is True:
                            currentMatrix[playerX + 1][playerY] = 'O'
                            playerX += 1
                            startTempX += 1
                    elif currentMatrix[playerX + 1][playerY] == '4':
                        if hasRedCoin is True:
                            currentMatrix[playerX + 1][playerY] = 'O'
                            playerX += 1
                            startTempX += 1
                    elif currentMatrix[playerX + 1][playerY] == '5':
                        if hasFlower is True:
                            currentMatrix[playerX + 1][playerY] = 'O'
                            playerX += 1
                            startTempX += 1
                    elif currentMatrix[playerX + 1][playerY] == '6':
                        if hasStar is True:
                            currentMatrix[playerX + 1][playerY] = 'O'
                            playerX += 1
                            startTempX += 1

                    elif currentMatrix[playerX + 1][playerY] == 'I':

                        iceAdvance = True
                        # i = 0
                        while iceAdvance is True:
                            if currentMatrix[playerX + 1][playerY] == 'I':
                                playerX += 1
                                startTempX += 1
                                drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                                playerSpriteGroup.draw(DISPLAYSURF)
                                pygame.display.update()
                                pygame.time.wait(5)
                            elif currentMatrix[playerX + 1][playerY] == 'O':
                                playerX += 1
                                startTempX += 1
                                iceAdvance = False
                            elif currentMatrix[playerX + 1][playerY] == '2':
                                playerX += 1
                                startTempX += 1
                                iceAdvance = False
                                youDied = True
                            elif currentMatrix[playerX + 1][playerY] == 'E':
                                levelEggsRemArr[eggArrayUsed] -= 1
                                currentMatrix[playerX + 1][playerY] = 'O'
                                playerX += 1
                                startTempX += 1
                                iceAdvance = False
                            elif currentMatrix[playerX + 1][playerY] == 'F' and hasBoots is False:
                                playerX += 1
                                startTempX += 1
                                youDied = True
                            elif currentMatrix[playerX + 1][playerY] == 'W':
                                iceAdvance = False

                    if currentMatrix[playerX][playerY] != 'H':
                        level1Hint = False
                        level2Hint = False
                    drawBoard(currentMatrix, startTempX, startTempY, DISPLAYSURF)
                    playerSpriteGroup.draw(DISPLAYSURF)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
