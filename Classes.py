import pygame
import random
import time

#initialization
pygame.init()
random.seed(int(time.time()))
pygame.display.set_caption("Goblin Shooter")

#window parameters
windowWidth = 500 
windowHeight = 480
window = pygame.display.set_mode((windowWidth, windowHeight))

#game global variables
playerSpawnX = windowWidth/2-32
playerSpawnY = 0
jumpHeight = 9 #the number of frames spent jumping

#global images
bg = pygame.image.load("Background.png")
hills = pygame.image.load("Hills.png")
sign = pygame.image.load("Sign.png")

#create the game clock
clock = pygame.time.Clock()
frameRate = 27 #the game loop repeats 27 times per second

#sound effects
bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("hit.wav")
deathSound = pygame.mixer.Sound("death.wav")
painSound = pygame.mixer.Sound("pain.wav")
successSound = pygame.mixer.Sound("success.wav")

#background music
music = pygame.mixer.music.load("encounter.mp3")

#the character controlled by the player
class Player(object):
    #sprites for each frame of the walk cycle
    walkRight = [pygame.image.load("R1.png"), pygame.image.load("R2.png"), pygame.image.load("R3.png"), pygame.image.load("R4.png"), pygame.image.load("R5.png"),
                 pygame.image.load("R6.png"), pygame.image.load("R7.png"), pygame.image.load("R8.png"), pygame.image.load("R9.png")]
    walkLeft = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"), pygame.image.load("L4.png"), pygame.image.load("L5.png"),
                pygame.image.load("L6.png"), pygame.image.load("L7.png"), pygame.image.load("L8.png"), pygame.image.load("L9.png")]
    death = pygame.image.load("standing.png") #special sprite shown when the character dies

    def __init__(self, x, y, width, height):
        #positioning and moving
        self.x = x
        self.y = y
        self.spawnX = x #remember the spawning position
        self.spawnY = y
        self.width = width
        self.height = height
        self.vel = 5 #pixels moved per step
        self.left = False #the character is facing left
        self.right = True #the character is facing right
        self.standing = True #the character is standing still

        #gravity mechanics
        self.isJump = False
        self.walkCount = 0 #the frame counter in the walk cycle
        self.jumpCount = jumpHeight #backward counter for the jump cycle
        self.fallCount = 0 #counter for the faling cycle due to gravity
        self.land = -1 #the platform the player is standing on (-1 for the floor)
        
        #getting hit by enemies
        self.hitbox = (self.x + 20, self.y + 14, 24, 50) #an imaginary rectangle around the Player
        self.invincibility = 0 #counter for the invincible cycle
        self.invincible = False #whether the player can be damaged (set to True to start cycle)
        self.health = 100 #remaining hit points of the player

    def draw(self, window):
        self.hitbox = (self.x + 20, self.y + 14, 24, 50) #update the hitbox
        
        if self.walkCount + 1 >= 2 * len(self.walkRight): #repeat the walk cycle
            self.walkCount = 0

        if self.health <= 0: #show the death sprite when health is depleted
            window.blit(self.death, (self.x,self.y))
            self.walkCount = 0
            self.jumpCount = jumpHeight
            self.fallCount = 0
        elif not(self.standing): #Player is walking
            if self.left: #advance the left walk cycle
                window.blit(self.walkLeft[self.walkCount//2], (self.x,self.y))
                self.walkCount += 1
            elif self.right: #advance the right walk cycle
                window.blit(self.walkRight[self.walkCount//2], (self.x,self.y))
                self.walkCount += 1
        else: #when standing still, face the same direction while standing
            if self.right:
                window.blit(self.walkRight[0], (self.x, self.y))
            else:
                window.blit(self.walkLeft[0], (self.x, self.y))

        #invincibility frames
        if self.invincibility > 0: #advance the cycle
            self.invincibility += 1
        if self.invincibility >= frameRate: #end of cycle
            self.invincibility = 0
            self.invincible = False

    #emit a pain sound, deduct health and activate the invincible cycle
    def hit(self, damage):
        self.invincibility = 1
        self.invincible = True
        self.health -= damage
        if self.health < 0:
            self.health = 0
        painSound.play()

    #change all values back to initial
    def reset(self):
        self.x = self.spawnX
        self.y = self.spawnY
        self.health = 100
        self.isJump = False
        self.fallCount = 0
        self.jumpCount = jumpHeight
        self.left = False
        self.right = True
        self.land = -1
                
#represents a circular bullet launched by a character
class Projectile(object):
    def __init__(self, x, y, radius, color, facing, damage, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing #bullet movng left (-1) or right (1)
        self.vel = vel * facing
        self.damage = damage #how much health is removed from a character on impact

    def draw(self,window):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)

#autonomous moving enemies that the player needs to kill
class Enemy(object):
    #sprites for each frame of the walk cycle
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]


    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start #left x coordinate restriction
        self.end = end #right x coordinate restriction
        self.path = [self.start, self.end] #the x coordinates the Enemy will always walk within
        self.walkCount = 0 #walk cycle counter
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10

        #for gravity mechanics
        self.fallCount = 0 #falling cycle counter
        self.land = -1 #the platform the enemy is standing on
        self.jumpCount = jumpHeight #jump cycle counter
        self.isJump = False #signal that the enemy is jumping up
        
    def draw(self, window, moving):
        #update the walk cycle
        if moving:
            self.move()
            self.walkCount += 1
        self.hitbox = (self.x + 20, self.y + 5, 28, 54) #update the hitbox location

        if self.health > 0:
            if self.walkCount + 1 >= 3 * len(self.walkRight): #repeat walk cycle
                self.walkCount = 0

            #update the sprite
            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            else:
                window.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))

            #draw a health bar
            pygame.draw.rect(window, (128,128,128), (self.hitbox[0]-1, self.hitbox[1] - 20, 52, 10), 1) #health bar background
            pygame.draw.rect(window, (128,0,128), (self.hitbox[0], self.hitbox[1] - 19, 50 - (5 * (10 - self.health)), 8)) #health bar
            

    #automatically moves the Enemy each frame
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    #enemy is damaged
    def hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0 #no negative health

#a surface for characters to walk on
class Platform(object):
    #seamless sprites to draw the platform
    floorTile = pygame.image.load("FloorTile.jpg")
    floorTileStart = pygame.image.load("FloorTileStart.png")
    floorTileEnd = pygame.image.load("FloorTileEnd.png")
    platformStart = pygame.image.load("PlatformStart.png")
    platformMiddle = pygame.image.load("PlatformMiddle.png")
    platformEnd = pygame.image.load("PlatformEnd.png")
    
    def __init__(self, x, y, width, variety):
        self.x = x
        self.y = y
        self.width = width

        #a cliff (variety 0) or a floating platform (variety 1)
        self.variety = variety
        if variety == 0:
            self.middle = self.floorTile
            self.start = self.floorTileStart
            self.end = self.floorTileEnd
        else:
            self.middle = self.platformMiddle
            self.start = self.platformStart
            self.end = self.platformEnd

    def draw(self, window):
        #draw the left piece
        xPos = self.x
        window.blit(self.start, (xPos, self.y))
        xPos += self.start.get_width()

        #draw the middle pieces
        while xPos < self.width + self.x - self.end.get_width():
            window.blit(self.middle, (xPos, self.y))
            xPos += self.middle.get_width()

        #draw the end piece
        window.blit(self.end, (xPos, self.y))
        self.width = xPos - self.x + self.end.get_width() #adjust platform width to fit sprites

#buttons that are clicked with the mouse
class Button(object):
    def __init__(self, x, y, width, string):
        self.x = x
        self.y = y
        self.width = width
        self.visible = False
        self.mouseDown = False #flag for holding the mouse button down

        #create the text to show on the button
        self.string = string
        self.font = pygame.font.Font("arial.ttf", 30)
        self.text = self.font.render(self.string, 1, (0,0,0))
        if self.width < self.text.get_width()+8: #adjust button size to accomodate text
            self.width = self.text.get_width()+8
        self.height = self.text.get_height()+8
        
    def draw(self, window): 
        if self.visible:
            pygame.draw.rect(window, (200,200,200), (self.x, self.y, self.width, self.height))
            if self.mouseDown: #draw a green rectangle when the left mouse button is pushed while hovering over the button
                pygame.draw.rect(window, (0,200,0), (self.x, self.y, self.width, self.height), 2)
            window.blit(self.text, (self.x + (self.width-self.text.get_width())/2,self.y+4))

    #check if the button has been pushed, then released with the cursor hovering
    def checkClicked(self):
        if pygame.mouse.get_pos()[0] >= self.x and pygame.mouse.get_pos()[0] <= self.x+self.width and pygame.mouse.get_pos()[1] >= self.y and pygame.mouse.get_pos()[1] <= self.y+self.height:
            if pygame.mouse.get_pressed()[0]: #mouse pressed
                self.mouseDown = True
            if self.mouseDown and not(pygame.mouse.get_pressed()[0]): #mouse released
                self.mouseDown = False
                return True
        else:
            self.mouseDown = False #click cancelled
        return False

#items for the Player to collect
class Gold(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 10, 10)

    def draw(self, window):
        self.hitbox = (self.x, self.y, 10, 10)
        pygame.draw.rect(window, (255, 255, 0), (self.x, self.y, self.hitbox[2], self.hitbox[3]))

#a sprite that cannot be interacted with
class Decoration(object):
    def __init__(self, x, y, picture):
        self.x = x
        self.y = y
        self.picture = picture #a pygame image for a sprite

    def draw(self, window):
        window.blit(self.picture, (self.x, self.y-self.picture.get_height()))
