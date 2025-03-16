#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    def collidepoint(self, x,y):
       return self.rect.collidepoint(x,y)


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700-10- self.rect.width:
            self.rect.x+=self.speed

    def fire(self):
        bullet = Bullet('pirog.png', self.rect.centerx, self.rect.y,20, 40, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,3)
            lost += 1     

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <=0:
            self.kill()

window = display.set_mode((700,500))
display.set_caption('Шутер')

#!задай фон сцены
background = transform.scale(image.load('fon2.jpg'), (700,500))

mixer.init()
mixer.music.load('pesnya.mp3')
mixer.music.play()

font.init()
#font1 = font.Font(None, 36)
font1 = font.SysFont('Arial', 36)

player = Player('timoha.png', 316,400,68, 100, 5)

bullets = sprite.Group()

enemy_count = 4
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('dryg.png', randint(10, 700-10-90), -40, 50, 90, randint(2,3))
    enemyes.add(enemy)

button = GameSprite('play.png', 300, 200, 100, 50, 0)

game = True 
finish = True
menu = True
lost = 0
score = 0
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if menu:
        window.blit(background,(0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0],pos[1]):
                menu = False
                finish = False

    if not finish:
        window.blit(background, (0,0))

        player.update()
        player.reset()
        enemyes.update()
        enemyes.draw(window)
        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено: '+str(lost), 1, (255,255,255))
        window.blit(lost_enemy, (10,10))
        score_enemy = font1.render('Убито: '+str(score), 1, (255,255,255))
        window.blit(score_enemy, (10,50))

        spite_list = sprite.groupcollide(
            enemyes, bullets, True, True
        )
        for i in range(len(spite_list)):
            score += 1
            enemy = Enemy('dryg.png', randint(10, 700-10-90), -40, 50, 90, randint(2,3))
            enemyes.add(enemy)
        if score>=21:
            finish = True
            txt_win = font1.render('Ты победил! Возьми пирожок.', 1, (255,0,0))
            window.blit(txt_win, (170,250))
        spite_list = sprite.spritecollide(player, enemyes, True)
        if lost>=5 or len(spite_list)>0:
            finish = True
            txt_lose = font1.render('Ты проиграл! Ты не получишь пирожок.', 1, (255,0,0))
            window.blit(txt_lose, (120,250))

    clock.tick(FPS)
    display.update()