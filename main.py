

import pygame
from pygame import sprite
from pygame import math
from pygame.display import update
import random
import os

FPS = 60
BACKGROUNDCOLOR = (153,0,0)
GREEN = (0,204,102)
BLUE = (0,0,102)
YELLOW = (255,255,102)
WHITE = (255,255,255)
BLACK = (0,0,0)
HEIGHT = 500
WIDTH = 500

pygame.init()
screen = pygame.display.set_mode((HEIGHT,WIDTH))
clock = pygame.time.Clock() 
pygame.display.set_caption('game')
running = True
score = 0

background_img = pygame.image.load(os.path.join("img","background.jpg")).convert()
UFO_img = pygame.image.load(os.path.join("img","UFO.jpg")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
rock_img = pygame.image.load(os.path.join("img","rock.jpg")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
enemy_bullet_img = pygame.image.load(os.path.join("img","enemy_bullet.png")).convert()

font_name = pygame.font.match_font('arial')

shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot_sound.wav"))
be_hit_sound = pygame.mixer.Sound(os.path.join("sound","be_hit.wav"))
sound_group = [
    pygame.mixer.Sound(os.path.join("sound","enemy_dead1.wav")),
    pygame.mixer.Sound(os.path.join("sound","enemy_dead2.wav"))
]

pygame.mixer.music.load(os.path.join("sound","background.wav"))
pygame.mixer.music.set_volume(0.7)


def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size) 
    text_sur = font.render(text,True,WHITE)
    text_rect = text_sur.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_sur,text_rect)
def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LEN = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LEN
    outline_rect = pygame.Rect(x,y,BAR_LEN,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)
class Player(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 18
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
        self.speedx = 8
        self.speedy = 8
        self.hp = 100
    
    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x +=self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -=self.speedx    
        if key_pressed[pygame.K_UP]:
            self.rect.y -=self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y +=self.speedy
      
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(UFO_img, (50,48))
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH-self.rect.width) 
        self.rect.y = random.randrange(0,HEIGHT/2)
        self.speedx = random.randrange(1 ,4)
        self.bullet_speed = 10
    def update(self):
            self.rect.x +=self.speedx
            if self.rect.right > WIDTH:
                self.speedx = -self.speedx 
            if self.rect.left <0:
                self.speedx = -self.speedx

            if self.bullet_speed%100 == 0:
                Enemy_bullet = Enemy_Bullet(self.rect.x+25,self.rect.bottom+25)
                all_sprites.add(Enemy_bullet)
                rocks.add(Enemy_bullet)
            self.bullet_speed+=1
            
        

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rand_size = random.randrange(20,50)
        self.image_or = pygame.transform.scale(rock_img, (rand_size,rand_size)) 
        self.image =  self.image_or.copy()
        self.image_or.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,5) 
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = 3
    def rotate(self):
        self.total_degree +=  self.rot_degree
        self.total_degree =  self.total_degree %360
        self.image = pygame.transform.rotate(self.image_or, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right<0:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,8)
            self.speedx = random.randrange(-3,3)
class Bullet(pygame.sprite.Sprite ):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(bullet_img, (20,30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() 
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill() 

class Enemy_Bullet(pygame.sprite.Sprite ):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(enemy_bullet_img, (20,60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 10

    def update(self):
        
        self.rect.y += self.speedy
        if self.rect.top >HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
rocks = pygame.sprite.Group()
      
player = Player()
all_sprites.add(player)
enemy = Enemy()  
all_sprites.add(enemy)   
enemies.add(enemy)
for i in range(20) :
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

pygame.mixer.music.play(-1)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets,True, True)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    destroy = pygame.sprite.groupcollide(enemies,bullets ,True, True)
    if destroy:
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
        random.choice(sound_group).play()
       
        score +=1
    hits = pygame.sprite.spritecollide(player,rocks,True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= 25
        be_hit_sound.play()
        if player.hp <= 0:
            running = False
    
    screen.fill(BACKGROUNDCOLOR)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.hp,5,10)
    pygame.display.update()
pygame.quit()
