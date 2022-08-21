import pygame
import random
import copy
import time
import math
from pygame import mixer

size = (800, 800)
scale=15
towerscale = 15
iconscale = 10
windowsize = (1000,800)
run = True
clock = pygame.time.Clock()

# tile imgs
grassImg = pygame.transform.scale(pygame.image.load("./assets/grass.png"), (size[0]//scale, size[1]//scale))
dirtImg = pygame.transform.scale(pygame.image.load("./assets/dirt.png"), (size[0]//scale, size[1]//scale))
waterImg = pygame.transform.scale(pygame.image.load("./assets/water.png"), (size[0]//scale, size[1]//scale))

shopimg = pygame.transform.scale(pygame.image.load("./assets/shop_icon_background.png"), (size[0] // iconscale, size[1] // iconscale))
shopimg_selected = pygame.transform.scale(pygame.image.load("./assets/shop_icon_selected.png"), (size[0] // iconscale, size[1] // iconscale))

# tower images

tower1_img = pygame.transform.scale(pygame.image.load("./assets/basictower.png"), (size[0] // iconscale, size[1] // iconscale))
tower2_img = pygame.transform.scale(pygame.image.load("./assets/bigtower.png"), (size[0] // iconscale, size[1] // iconscale))
tower3_img = pygame.transform.scale(pygame.image.load("./assets/boat2.png"), (size[0] // iconscale, size[1] // iconscale))

map1 = pygame.transform.scale(pygame.image.load("./assets/map1.png"), (800, 700))
map1dirttiles = [pygame.Rect(0, 350, 150, 60), pygame.Rect(110, 150, 40, 200), pygame.Rect(108, 142, 211, 64), pygame.Rect(267, 146, 53, 343), pygame.Rect(268, 422, 264, 68), pygame.Rect(481, 281, 53, 203), pygame.Rect(481, 281, 317, 65)]
map1watertiles = []
map2 = pygame.transform.scale(pygame.image.load("./assets/map2.png"), (800, 700))
map2dirttiles = [pygame.Rect(0, 133, 178, 44), pygame.Rect(137, 138, 40, 220), pygame.Rect(138, 538,45, 324), pygame.Rect(182, 636, 579, 42), pygame.Rect(717, 322, 42, 356), pygame.Rect(434, 323, 325, 40), pygame.Rect(433, 0, 41, 363)]
map2watertiles = [pygame.Rect(203, 190, 197, 259)]
map3 = []

map = []

route1 = [(-80, 350), (105, 350), (105, 145), (270, 145), (270, 430), (480, 430), (480, 290), (800, 290)]
route2 = [(-80, 138), (137, 137), (137, 645), (737, 645), (737, 323), (438, 323), (438, 0)]
route3 = []
route = []

health = 150
money = 10000

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("arial", 30)
pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

screen = pygame.display.set_mode(windowsize)
surface = pygame.Surface(size, pygame.SRCALPHA)


oncooldown = False
cooldown = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.hp = 1
        self.speed = 1
        self.x = x
        self.y = y
        self.waypointval = 0
        self.weight = 1
        self.Img = pygame.transform.scale(pygame.image.load("./assets/duck.png"), (size[0]//scale, size[1]//scale))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.Img.get_rect()
    def damage(self, amt):
        self.hp -= amt
    def isDead(self):
        if self.hp <= 0:
            return True
        else:
            return False

class Enemy2(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.hp = 20
        self.speed = 1
        self.weight = 35
        self.Img = pygame.transform.scale(pygame.image.load("./assets/Enemy2.png"), (size[0] // scale, size[1] // scale))

class Enemy3(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.hp = 5
        self.speed = 5
        self.weight = 10
        self.Img = pygame.transform.scale(pygame.image.load("./assets/Enemy3.png"), (size[0] // scale, size[1] // scale))

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.cooldown = 60
        self.maxcooldown = 60
        self.oncooldown = True
        self.radius = 100
        self.dmg = 1
        self.x = x - size[0] / scale / 2
        self.y = y - size[0] / scale / 2
        self.Img = pygame.transform.scale(pygame.image.load("./assets/basictower.png"), (size[0] // towerscale, size[1] // towerscale))
        self.rect = self.Img.get_rect()
        pygame.sprite.Sprite.__init__(self)
        self.u = pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(850, 400, 100, 80))
        self.r = pygame.draw.circle(surface, (255, 255, 255, 100), (self.x + size[0] // towerscale // 2, self.y + size[0] // towerscale // 2), self.radius)
        self.selected = False
        self.upgradecost = 100
        self.attacktype = "basic"
        self.value = 400
        self.sell = pygame.Rect(880, 400, 180, 60)
    def drawradius(self):
        self.r = pygame.draw.circle(surface, (255,255,255, 100), (self.x + size[0] // towerscale // 2, self.y + size[0] // towerscale // 2), self.radius)
    def isoncooldown(self):
        return self.oncooldown
    def upgrademenu(self):
        self.u = pygame.Rect(810, 400, 180, 60)
        self.u_img = pygame.transform.scale(pygame.image.load("./assets/upgrade_icon.png"), (180, 60))
        screen.blit(self.u_img, (810, 400))
        screen.blit(my_font.render("£" + str(self.upgradecost), False, (255, 255, 255)), (850, 415))
    def sellmenu(self):
        self.sell = pygame.Rect(810, 470, 180, 60)
        self.s_img = pygame.draw.rect(screen, (255, 0, 0), (810, 470, 180, 60))


class Tower2(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y)
        self.dmg = 1
        self.maxcooldown = 10
        self.cooldown = 10
        self.radius = 250
        self.value = 800
        self.Img = pygame.transform.scale(pygame.image.load("./assets/bigtower.png"), (size[0] // towerscale, size[1] // towerscale))
        self.r = pygame.draw.circle(surface, (255, 255, 255, 100), (self.x + size[0] // towerscale // 2, self.y + size[0] // towerscale // 2), self.radius)
        self.attacktype = "basic"

class Tower3(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y)
        self.dmg = 5
        self.maxcooldown = 20
        self.cooldown = 20
        self.radius = 500
        self.value = 3000
        self.Img = pygame.transform.scale(pygame.image.load("./assets/boat.png"), (size[0] // towerscale, size[1] // towerscale))
        self.r = pygame.draw.circle(surface, (255, 255, 255, 100), (self.x + size[0] // towerscale // 2, self.y + size[0] // towerscale // 2), self.radius)
        self.attacktype = "explosion"
        # required for explosion tower
        self.projectilex = 0
        self.projectiley = 0
        self.projectiletime = 30
        self.targetx = 0
        self.targety = 0
        self.step_x = 1
        self.step_y = 1
        self.projectileairtime = 0
        self.attacking = False

enemies = []
towers = []

tower1buy = False
Tower1cost = 500
tower2buy = False
Tower2cost = 1000
tower3buy = False
tower3cost = 3500

enemydelay = 5
roundgo = False
roundprogressing = False
roundsdone = 0

r1 = ["1", 10]
#r1 = ["1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 5, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 10, "1", 5]
r2 = ["1", 5, "1", 5, "1", 5, "1", 5, "1", 20, "2", 30, "2", 5]
r3 = ["3", 30, "3", 5]
r4 = ["1", 30, "2", 30, "3", 30, "1", 30, "2", 30, "3", 30, "1", 30, "2", 30, "3", 30, "1", 30, "2", 30, "3", 30, "1", 30, "2", 30, "3", 30]

rounds = [r1, r2, r3, r4]

dirt_tiles = []
water_tiles = []
ondirt = False
onwater = False

titlescreen=True
while titlescreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            titlescreen = False
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()
            print(m)
            if pygame.Rect(36, 390, 375, 85).collidepoint(m): # map 1
                route=route1
                map = map1
                dirt_tiles = map1dirttiles
                titlescreen = False

            if pygame.Rect(40, 510, 375, 85).collidepoint(m):
                route=route2
                map = map2
                dirt_tiles = map2dirttiles
                water_tiles = map2watertiles
                titlescreen = False

            if pygame.Rect(40, 640, 375, 85).collidepoint(m):
                route = route3
                print("3")
                # map
                titlescreen = False

    screen.blit(pygame.transform.scale(pygame.image.load("./assets/title-bg-buttons.png"), windowsize), (0, 0))
    pygame.display.flip()
    clock.tick(60)

# play animation

def squaresequence(x1, y1, x2, y2, isx, step):
    if isx:
        for i in range(x1, y1, step):
            pygame.draw.rect(screen, (0, 0, 0), (i, y2, 100, 100))
            pygame.display.flip()
            time.sleep(0.05)
    else:
        for i in range(x1, y1, step):
            pygame.draw.rect(screen, (0, 0, 0), (x2, i, 100, 100))
            pygame.display.flip()
            time.sleep(0.05)

# if 1==2:
#     squaresequence(0, 1000, 0, 0, True, 100)
#     squaresequence(100, 800, 900, 0, False, 100)
#     squaresequence(800, -100, 0, 700, True, -100)
#     squaresequence(600, 0, 0, 0, False, -100)
#     squaresequence(100, 900, 0, 100, True, 100)

enemyspawnxy = route[0]
route.pop(0)

if map == map2:
    sound = pygame.mixer.Sound("./audio/map2.wav")
    sound.set_volume(0.03)
    sound.play(-1)

while run: # main game loop
    # events, keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()
            # all of the code dealing with a mouseclick

            for t in towers:
                if pygame.Rect(t.x, t.y, 80, 80).collidepoint(m): # manages which tower is selected
                    for s in towers:
                        if s == t:
                            s.selected = not s.selected
                        else:
                            s.selected = False

                if t.selected: # tower upgrade button logic
                    if t.u.collidepoint(m):
                        if money >= 100:
                            t.dmg += 5
                            t.radius += 2
                            money -= 100
                            t.value += 80
                    if t.sell.collidepoint(m):
                        money += t.value
                        towers.pop(towers.index(t))

            for r in dirt_tiles: # checks to see if the mouse click is on a dirt or water tile
                if r.colliderect(pygame.Rect(m[0], m[1], 10, 10)):
                    ondirt = True
                    print("on dirt")
                    break
                else:
                    ondirt = False

            for w in water_tiles:
                if w.colliderect(pygame.Rect(m[0], m[1], 10, 10)):
                    onwater = True
                    print("on water")
                    break
                else:
                    onwater = False

            # tower 1 shop button functionality
            if tower1shop_rect.collidepoint(m):
                tower1buy = not tower1buy
                tower2buy = False
                tower3buy = False
            if tower1buy == True and m[0] < 800 and money >= Tower1cost:
                if ondirt == False and onwater == False:
                    towers.append(Tower(m[0], m[1]))
                    money -= Tower1cost
                    tower1buy = False

            #tower 2 shop button
            if tower2shop_rect.collidepoint(m):
                tower2buy = not tower2buy
                tower1buy = False
                tower3buy = False
            if tower2buy == True and m[0] < 800 and money >= Tower2cost:
                if ondirt == False and onwater == False:
                    towers.append(Tower2(m[0], m[1]))
                    money -= Tower2cost
                    tower2buy = False

            # tower 3 shop button
            if tower3shop_rect.collidepoint(m):
                tower3buy = not tower3buy
                tower1buy = False
                tower2buy = False
            if tower3buy == True and m[0] < 800 and money >= tower3cost:
                if ondirt == False and onwater == True:
                    towers.append(Tower3(m[0], m[1]))
                    money -= tower3cost
                    tower3buy = False

            # controls whether enemies are spawning
            if menubutton.collidepoint(m) and enemies == []:
                if roundprogressing == False:
                    roundprogressing = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                for i in range(0, 50, 10):
                    enemies.append(Enemy(-80-i, 80))

    # logic
    if roundgo or roundprogressing:
         enemydelay -= 1
         if enemydelay <= 0:
             if rounds == []:
                 enemies.append(Enemy3(-80, 350))
                 enemydelay = 10
             elif rounds[0] == []:
                    rounds.pop(0)
                    roundprogressing = False
                    roundsdone += 1
                    money += 50 * roundsdone
         #enemies.append(Enemy(-80, 80))
             if rounds == []:
                 continue
             if rounds[0][0] == "1":
                  enemies.append(Enemy(enemyspawnxy[0], enemyspawnxy[1]))
                  rounds[0].pop(0)
                  enemydelay = rounds[0][0]
                  rounds[0].pop(0)
             elif rounds[0][0] == "2":
                  enemies.append(Enemy2(enemyspawnxy[0], enemyspawnxy[1]))
                  rounds[0].pop(0)
                  enemydelay = rounds[0][0]
                  rounds[0].pop(0)
             elif rounds[0][0] == "3":
                  enemies.append(Enemy3(enemyspawnxy[0], enemyspawnxy[1]))
                  rounds[0].pop(0)
                  enemydelay = rounds[0][0]
                  rounds[0].pop(0)

    # graphics
    screen.fill((101, 79, 33))
    surface.fill((0, 0, 0, 0))

    # map
    screen.blit(map, (0, 0))

    for e in enemies: # draws all the enemies onto the screen
        screen.blit(e.Img, (e.x, e.y))
        # controls movement of the enemies
        if e.x < route[e.waypointval][0]:
            e.x += e.speed
            if e.x > route[e.waypointval][0]:
                e.x = route[e.waypointval][0]
        elif e.x > route[e.waypointval][0]:
            e.x -= e.speed
            if e.x < route[e.waypointval][0]:
                e.x = route[e.waypointval][0]
        if e.y < route[e.waypointval][1]:
            e.y += e.speed
            if e.y > route[e.waypointval][1]:
                e.y = route[e.waypointval][1]
        elif e.y > route[e.waypointval][1]:
            e.y -= e.speed
            if e.y < route[e.waypointval][1]:
                e.y = route[e.waypointval][1]
        if e.x == route[e.waypointval][0] and e.y == route[e.waypointval][1]:
            e.waypointval += 1
            if e.waypointval > len(route) - 1:
                health -= e.weight
                print(health)
                enemies.pop(enemies.index(e))

    for t in towers:
        screen.blit(t.Img, (t.x, t.y))
        if t.selected == True:
            t.drawradius()
            t.upgrademenu()
            t.sellmenu()

    # colours button in bottom right either green or red depending on whether a new round can be triggered
    if enemies == []:
        roundgocolour = (0, 255, 0)
    elif roundprogressing:
        roundgocolour = (255, 0, 0)
    else:
        roundgocolour = (255, 0, 0)
    menubutton = pygame.draw.rect(screen, roundgocolour, pygame.Rect(850, 720, 100, 80))

    # graphics for all of the shop icons along with selected glow around them
    tower1shop_rect = pygame.Rect(810, 40, 80, 80)
    if tower1buy:
        tower1shop = screen.blit(shopimg_selected, (810, 40))
    else:
        tower1shop = screen.blit(shopimg, (810, 40))
    tower1icon = screen.blit(tower1_img, (810, 40))

    tower2shop_rect = pygame.Rect(910, 40, 80, 80)
    if tower2buy:
        tower2shop = screen.blit(shopimg_selected, (910, 40))
    else:
        tower2shop = screen.blit(shopimg, (910, 40))
    tower2icon = screen.blit(tower2_img, (910, 40))

    tower3shop_rect = pygame.Rect(810, 130, 80, 80)
    if tower3buy:
        tower3shop = screen.blit(shopimg_selected, (810, 130))
    else:
        tower3shop = screen.blit(shopimg, (810, 130))
    tower3icon = screen.blit(tower3_img, (810, 130))

    # draws the total money of the player
    moneytext = my_font.render("£" + str(money), False, (255,255,255))
    screen.blit(moneytext, (850, 0))

    for t in towers:
        # entire chunk of code to deal with if the tower has a splash projectile
        if t.attacktype == "explosion":
            if t.attacking == True:
                t.projectileairtime += 1
                if t.projectileairtime > 70:
                    t.attacking = False
                    t.oncooldown = True
                    t.cooldown = t.maxcooldown
                    continue
                e_rect = pygame.Rect(t.projectilex, t.projectiley, 40, 40)
                projectile = pygame.draw.rect(screen, (255, 0, 0, 50), (t.projectilex, t.projectiley, 40, 40))
                enemycollisions = []
                for e in enemies:
                    if e_rect.colliderect(pygame.Rect(e.x, e.y, 80, 80)):
                        print("here")
                        enemycollisions.append(enemies.index(e))
                print(enemycollisions)
                if enemycollisions != []:
                    for e in enemycollisions:
                        enemies[e].damage(t.dmg)
                        print(enemies[e].hp)
                    t.attacking = False
                    t.oncooldown = True
                    t.cooldown = t.maxcooldown
                else:
                    if t.projectilex > t.targetx:
                        t.projectilex -= t.step_x
                    elif t.projectilex < t.targetx:
                        t.projectilex += t.step_x
                    if t.projectiley > t.targety:
                        t.projectiley -= t.step_y
                    elif t.projectiley < t.targety:
                        t.projectiley += t.step_y


        for e in enemies:
            rect = pygame.Rect(e.x, e.y, int(size[0] / scale), int(size[0] / scale)) # enemy rect

            if pygame.Rect(t.r).colliderect(rect) == True: # checks if an enemy is in the towers radius

                if t.oncooldown == False:
                    if t.attacktype == "basic":
                        pygame.draw.line(screen, (255, 0, 0), (t.x + 45, t.y + 12), (e.x + 25+random.randint(0, 10), e.y+15+random.randint(1,10)), width=5) # random targeting makes the attack feel a bit more natural as oppposed to all towers hitting the enmey in the exact same spot
                        e.damage(t.dmg)
                        t.oncooldown = True
                        t.cooldown = t.maxcooldown
                    elif t.attacktype == "explosion":
                        if t.attacking == False:
                            t.targetx = e.x
                            t.targety = e.y
                            t.projectilex = t.x
                            t.projectiley = t.y
                            temp = e.x - t.x
                            temp2 = e.y - t.y
                            tt = t.projectiletime # these 5 lines gives the projectile a speed based on the distance to the target to let each projectile take the same time
                            t.step_x = abs(temp // tt)
                            t.step_y = abs(temp2 // tt)
                            t.attacking = True
                            t.projectileairtime = 0

            if e.isDead():
                money += e.weight
                enemies.pop(enemies.index(e))

        if t.isoncooldown() == True:
            t.cooldown -= 1
            if t.cooldown <= 0:
                t.oncooldown = False

    # update
    screen.blit(surface, (0,0))
    pygame.display.flip()
    # frame rate limit
    clock.tick(60)

pygame.quit()
