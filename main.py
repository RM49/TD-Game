# code improved, tower placed with mouseclick, enemy travels accross map based on predetermined route, towers can attack enemy



import pygame
import random
import copy
import time

size = (800, 800)
scale=10
run = True
clock = pygame.time.Clock()

# tile imgs
grassImg = pygame.transform.scale(pygame.image.load("grass.png"), (size[0]//scale, size[1]//scale))
dirtImg = pygame.transform.scale(pygame.image.load("dirt.png"), (size[0]//scale, size[1]//scale))
waterImg = pygame.transform.scale(pygame.image.load("water.png"), (size[0]//scale, size[1]//scale))

map = open("map1", "r")
tiles = map.readlines()
map.close()

route1 = [(0, 80), (640, 80), (640, 640), (800, 640)]
health = 150

pygame.init()
screen = pygame.display.set_mode(size)
surface = pygame.Surface(size, pygame.SRCALPHA)

temp = (50,50)
oncooldown = False
cooldown = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.hp = 10000
        self.speed = 10
        self.x = x
        self.y = y
        self.waypointval = 0
        self.weight = 1
        self.Img = pygame.transform.scale(pygame.image.load("duck.png"), (size[0]//scale, size[1]//scale))
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
        self.cooldown = 60
        self.maxcooldown = 60
        self.oncooldown = True
        self.radius = 150
        self.dmg = 10
        self.x = x - size[0] / scale / 2
        self.y = y - size[0] / scale / 2
        self.Img = pygame.transform.scale(pygame.image.load("basictower.png"), (size[0] / scale, size[1] / scale))
        self.rect = self.Img.get_rect()
        pygame.sprite.Sprite.__init__(self)

    def drawradius(self):
        self.r = pygame.draw.circle(surface, (255,255,255, 100), (self.x + size[0] / scale / 2, self.y + size[0] / scale / 2), self.radius)
    def isoncooldown(self):
        return self.oncooldown


enemies = []
towers = []


while run: # main game loop
    # events, keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            temp = pygame.mouse.get_pos()
            towers.append(Tower(temp[0], temp[1]))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                    enemies.append(Enemy(-80, 80))

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

    for l in route1:
        pygame.draw.circle(screen, (0, 0, 0), l, 25)

    for e in enemies: # draws all the enemies onto the screen
        screen.blit(e.Img, (e.x, e.y))
        if e.x <= route1[e.waypointval][0]:
            e.x += 1
        elif e.x >= route1[e.waypointval][0]:
            e.x -= 1
        if e.y <= route1[e.waypointval][1]:
            e.y += 1
        elif e.y >= route1[e.waypointval][1]:
            e.y -= 1
        if e.x == route1[e.waypointval][0] and e.y == route1[e.waypointval][1]:
            e.waypointval += 1
            if e.waypointval > len(route1) - 1:
                health -= e.weight
                enemies.pop(enemies.index(e))
                print(health)



    for t in towers:
        screen.blit(t.Img, (t.x, t.y))
        t.drawradius()


    for t in towers:
        for e in enemies:
            rect = pygame.Rect(e.x, e.y, int(size[0] / scale), int(size[0] / scale))
            rect2 = pygame.Rect(t.x, t.y, int(size[0] / scale), int(size[0] / scale))
            if pygame.Rect(t.r).colliderect(rect) == True:
                print(e)
                print(t.isoncooldown())
                if t.isoncooldown() == False:
                    pygame.draw.line(screen, (255, 0, 0), (t.x, t.y), (e.x, e.y), width=5)
                    e.damage(t.dmg)
                    print(e.hp)
                    if e.isDead():
                        enemies.pop(enemies.index(e))
                    t.oncooldown = True
                    t.cooldown = t.maxcooldown
                    break
        if t.isoncooldown() == True:
            t.cooldown -= 10
            if t.cooldown <= 0:
                t.oncooldown = False



    # update
    screen.blit(surface, (0,0))
    pygame.display.flip()
    # frame rate limit
    clock.tick(60)

pygame.quit()



