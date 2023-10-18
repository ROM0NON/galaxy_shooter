from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 70)
win = font1.render("YOU WIN!", True, (255, 255, 0))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = 'bullet.png'
img_steroid = 'asteroid.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, x_size, y_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x_size, y_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 3, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > win_height:
            self.kill
class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)

        
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("CS:Galaxy")
background = transform.scale(image.load(img_back), (win_width, win_height))

num_fire = 0
lost = 0
score = 0
goal = 20
life = 3
max_lost = 10

Rocket = Player('rocket.png', 6, 390, 5, 45, 105)

monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(0, win_width - 80), -40, randint(1, 3), 80, 50)
    monsters.add(monster)
for i in range(3):
    asteroid = Asteroids(img_steroid, randint(0, win_width - 80), -40, randint(1, 3), 80, 50)
    asteroids.add(asteroid)
last_time = timer()
bullets = sprite.Group()
finish = False
run = True
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    Rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))
        Rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        Rocket.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites2_list = sprite.groupcollide(bullets, asteroids, True, False)
        lifecollide = sprite.spritecollide(Rocket, asteroids, True, False)
        sprite_box = sprite.spritecollide(Rocket, monsters, True, False)
        if lifecollide or sprite_box:
            life -= 1
            if lifecollide:
                asteroid = Asteroids(img_steroid, randint(0, win_width - 80), -40, randint(1, 3), 80, 50)
                asteroids.add(asteroid)
            else:
                monster = Enemy(img_enemy, randint(0, win_width - 80), -40, randint(1, 2), 80, 50)
                monsters.add(monster)
        for c in sprites_list:
            score += 1
            monster = Enemy(img_enemy, randint(0, win_width - 80), -40, randint(1, 5), 80, 50)
            monsters.add(monster)
        if lost >= max_lost or life <= 0:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        text = font2.render("Счёт: " + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,65))
        text_life = font2.render("Жизней: " + str(life), 1, (255,255,255))
        window.blit(text_life, (10,105))
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for a in monsters:
            a.kill()
        for i in asteroids:
            i.kill()
        for i in range (1, 6):
            monster = Enemy(img_enemy, randint(0, win_width - 80), -40, randint(1, 2), 80, 50)
            monsters.add(monster)
        for i in range(3):
            asteroid = Asteroids(img_steroid, randint(0, win_width - 80), -40, randint(1, 3), 80, 50)
            asteroids.add(asteroid)
        time.delay(3000)
    time.delay(15)
