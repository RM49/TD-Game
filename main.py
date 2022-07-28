# code so far. Spawns enemies at random place and a mock tower can attack enemies within a radius on a map drawn from a text file



import pygame
import random
size = (800, 800)
scale=10
run = True
clock = pygame.time.Clock()

# tile imgs
grassImg = pygame.transform.scale(pygame.image.load("grass.png"), (size[0]/scale, size[1]/scale))
dirtImg = pygame.transform.scale(pygame.image.load("dirt.png"), (size[0]/scale, size[1]/scale))
waterImg = pygame.transform.scale(pygame.image.load("water.png"), (size[0]/scale, size[1]/scale))

map = open("map1", "r")
tiles = map.readlines()
map.close()

pygame.init()
screen = pygame.display.set_mode(size)
surface = pygame.Surface(size, pygame.SRCALPHA)

temp = (50,50)
oncooldown = False
cooldown = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.hp = 100
        self.speed = 10
        self.x = x
        self.y = y
        self.Img = pygame.transform.scale(pygame.image.load("duck.png"), (size[0]/scale, size[1]/scale))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.Img.get_rect()
    def damage(self, amt):
        self.hp -= amt
    def isDead(self):
        if self.hp <= 0:
            return True
        else:
            return False

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.cooldown = 0
        self.maxcooldown = 60
        self.oncooldown = False
        self.radius = 50
        self.x = x
        self.y = y
        self.Img = pygame.transform.scale(pygame.image.load("basictower.png"), (size[0] / scale, size[1] / scale))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.Img.get_rect()
    def drawradius(self):
        pygame.draw.circle(surface, (255,255,255, 100), (self.x, self.y), self.radius)

enemies = []

for i in range(7):
    enemies.append(Enemy(random.randint(0, 800), random.randint(0,800)))


while run: # main game loop
    # events, keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            temp = pygame.mouse.get_pos()

    # logic

    # graphics
    screen.fill((255,255,255))
    screen.blit(grassImg, (10,100))
    # maploader
    count = 0
    count2 = 0

    for i in range(0, size[0], int(size[0]/scale)):
        y = i
        for i in range(0, size[0], int(size[0]/scale)):
            x = i
            if tiles[count][count2] == "G":
                screen.blit(grassImg, (x, y))
            elif tiles[count][count2] == "W":
                screen.blit(waterImg, (x, y))
            elif tiles[count][count2] == "D":
                screen.blit(dirtImg, (x, y))
            count2 += 1
        count2=0
        count += 1

    for e in enemies: # draws all the enemies onto the screen
        screen.blit(e.Img, (e.x, e.y))

    towerRange = pygame.draw.circle(screen, (255,255,255), temp, 50) # mock tower range

    # returns collisions between enemies and the range of a tower, tower damages enemy collided with
    for e in enemies:
        rect = pygame.Rect(e.x, e.y, int(size[0]/scale), int(size[0]/scale)) # creates a rect within the borders of the enemy
        if pygame.Rect(towerRange).colliderect(rect) == True: # tests if the rect of the tower range and enemy collide, returns the enemy who was there
            if oncooldown == False:
                pygame.draw.line(screen, (255,0,0), temp, (e.x, e.y))
                e.damage(10)
                if e.isDead():
                    enemies.pop(enemies.index(e))
                oncooldown = True
                cooldown = 60
                print(e.hp)
            else:
                cooldown -= 0.5
                if cooldown <=0:
                    oncooldown = False




    # update
    pygame.display.flip()
    # frame rate limit
    clock.tick(30)

pygame.quit()

