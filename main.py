import pygame
import random

pygame.init()
pygame.display.set_caption("Shooter")
win = pygame.display.set_mode((853,480))
run = True
bg = pygame.image.load("Shooter/images/bg.jpg")

enemy_pic = pygame.image.load("Shooter/images/enemy.png")
enemy_pic = pygame.transform.scale(enemy_pic, (50, 50))

protagonist_pic = pygame.image.load("Shooter/images/main.png")
protagonist_pic = pygame.transform.scale(protagonist_pic, (100, 90))

bulletSound = pygame.mixer.Sound("Shooter/gun.wav")
deathSound = pygame.mixer.Sound("Shooter/death.wav")

clock = pygame.time.Clock()

class Protagonist():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.hitbox = (self.x - 32, self.y - 27, 65, 57)

    def draw(self, win):
        win.blit(protagonist_pic, (self.x, self.y))
        self.hitbox = (self.x - 7, self.y - 7, 110, 110)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.x = 370
        self.y = 350
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('You lost!', 1, (255,0,0))
        win.blit(text, (426.5 - (text.get_width()/2), 100))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Enemy():
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.angle = 0
        self.hitbox = (self.x + 11, self.y + 2, 31, 57)

    def draw(self, win):
        global enemies
        self.blitRotate()
        self.y += self.vel 
        self.hitbox = (self.x - 32, self.y - 27, 65, 57)

    def blitRotate(self):
        copy = pygame.transform.rotate(enemy_pic, self.angle)
        win.blit(copy, (self.x - int(copy.get_width() / 2), self.y - int(copy.get_height() / 2)))
        self.angle += 27

class projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self,win):
        self.move()
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    def move(self):
        self.y -= self.vel
    
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (660, 10))
    text2 = font.render("Best score: " + str(bestscore), 1, (255,255,255))
    win.blit(text2, (640, 50))
    protagonist.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    for bullet in bullets:
        if bullet.y < 10:
            bullets.remove(bullet)
        bullet.draw(win)
    pygame.display.update()

# Characters
protagonist = Protagonist(370, 350, 100, 90)
enemies = []
bullets = []

# Variables
font = pygame.font.SysFont("comicsans", 30, True)
score = 0
shootLoop = 0
start = 50
finish = 200
maxx = 3
bestscore = 0

# Main loop
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and protagonist.x + protagonist.vel + protagonist.width <= 853:
        protagonist.x += protagonist.vel
    if keys[pygame.K_LEFT] and protagonist.x - protagonist.vel >= 0:
        protagonist.x -= protagonist.vel
    if len(enemies) < maxx:
        enemies.append(Enemy(random.randint(start, finish), -30, 50, 50, random.uniform(0.5, 1.5)))
        if finish < 700 and start < 700:
            finish += 200
            start += 100
        else:
            start = 50
            finish = 200
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if score == 5:
            maxx = 6
        elif score == 15:
            maxx = 12
        elif score == 30:
            maxx = 20
        if len(bullets) < maxx:
            bulletSound.play()
            bullets.append(projectile(protagonist.x + protagonist.width//2, protagonist.y, 3, (255, 0, 0)))
        shootLoop = 1

    for bullet in bullets:
        for enemy in enemies:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]: 
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]: 
                    score += 1
                    enemies.pop(enemies.index(enemy))
                    try:
                        bullets.remove(bullet)
                    except:
                        pass
    for enemy in enemies:
        if protagonist.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and protagonist.hitbox[1] + protagonist.hitbox[3] > enemy.hitbox[1]: 
            if protagonist.hitbox[0] + protagonist.hitbox[2] > enemy.hitbox[0] and protagonist.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                deathSound.play()
                if score > bestscore:
                    bestscore = score
                enemies = []
                protagonist.hit()
                score = 0
                maxx = 3

    redrawGameWindow()
    
pygame.quit()