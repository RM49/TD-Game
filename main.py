# code still messy. can now select or deselect towers, then purchase an upgrade on it. increasing price needed. more enemy types and others needed for balanced game



import pygame
import random
import copy
import time

size = (800, 800)
scale=10
windowsize = (1000,800)
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
money = 2000

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("arial", 30)

screen = pygame.display.set_mode(windowsize)
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
        self.u = pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(850, 400, 100, 80))
        self.r = pygame.draw.circle(surface, (255, 255, 255, 100), (self.x + size[0] / scale / 2, self.y + size[0] / scale / 2), self.radius)
        self.selected = False
    def drawradius(self):
        self.r = pygame.draw.circle(surface, (255,255,255, 100), (self.x + size[0] / scale / 2, self.y + size[0] / scale / 2), self.radius)
    def isoncooldown(self):
        return self.oncooldown
    def upgrademenu(self):
        self.u = pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(850, 400, 100, 80))

class Tower2(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y)
        self.dmg = 50
        self.maxcooldown = 20
        self.cooldown = 20
        self.radius = 250
        self.Img = pygame.transform.scale(pygame.image.load("bigtower.png"), (size[0] / scale, size[1] / scale))



enemies = []
towers = []

tower1buy = False
Tower1cost = 500
tower2buy = False
Tower2cost = 1500
roundgo = False


enemydelay = 5

while run: # main game loop
    # events, keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()

            for t in towers:
                print("here")
                if pygame.Rect(t.x, t.y, 80, 80).collidepoint(m):
                    for s in towers:
                        if s == t:
                            s.selected = not s.selected
                        else:
                            s.selected = False

                if t.selected:
                    if t.u.collidepoint(m):
                        if money >= 100:
                            t.dmg += 5
                            t.radius += 2
                            money -= 100



            # tower 1 stuff
            if basetowermenu.collidepoint(m):
                tower1buy = not tower1buy
                tower2buy = False
            if tower1buy == True and m[0] < 800 and money >= Tower1cost:
                towers.append(Tower(m[0], m[1]))
                money -= Tower1cost

            #tower 2 stuff

            if bigtowermenu.collidepoint(m):
                tower2buy = not tower2buy
                tower1buy = False
            if tower2buy == True and m[0] < 800 and money >= Tower2cost:
                towers.append(Tower2(m[0], m[1]))
                money -= Tower2cost

            # controls whether enemies are spawning
            if menubutton.collidepoint(m):
                roundgo = not roundgo

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                for i in range(0, 50, 10):
                    enemies.append(Enemy(-80-i, 80))


    # logic
    if roundgo:
        enemydelay -= 1
        if enemydelay <= 0:
            enemies.append(Enemy(-80, 80))
            enemydelay = 5


    # graphics
    screen.fill((101, 79, 33))
    surface.fill((0, 0, 0, 0))
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
        if t.selected == True:
            t.drawradius()
            t.upgrademenu()


    roundgocolour = (0, 255, 0)
    if roundgo:
        roundgocolour = (255, 0, 0)
    menubutton = pygame.draw.rect(screen, roundgocolour, pygame.Rect(850, 720, 100, 80))

    tower1buttoncolour = (0, 0, 255)
    if tower1buy:
        tower1buttoncolour = (0, 100, 100)

    basetowermenu = pygame.draw.rect(screen, tower1buttoncolour, pygame.Rect(850, 40, 100, 80))

    tower2buttoncolour = (0, 0, 255)
    if tower2buy:
        tower2buttoncolour = (0, 200, 200)

    bigtowermenu = pygame.draw.rect(screen, tower2buttoncolour, pygame.Rect(850, 200, 100, 80))

    moneytext = my_font.render("£" + str(money), False, (255,255,255))
    screen.blit(moneytext, (850, 0))

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
                        money += 50
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
