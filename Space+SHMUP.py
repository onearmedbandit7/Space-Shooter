
# coding: utf-8

# In[1]:

import pygame
import random
vec = pygame.math.Vector2


WIDTH = 1400
HEIGHT = 800
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
score = 0
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)* BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 32
        self.rect.centerx = 100
        self.rect.bottom = HEIGHT/2
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        
    def update(self):
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (100,HEIGHT/2)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        if keystate[pygame.K_UP]:
            self.speedy = -7
        if keystate[pygame.K_DOWN]:
            self.speedy = 7
        if keystate[pygame.K_a]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #### GLOBAL POSITIONS FOR TARGETTING##################
        global playerpos
        playerpos = vec(self.rect.x,self.rect.y)
        global powship1
        powship1 = vec(self.rect.x+5,self.rect.y-50)
        global powship2
        powship2 = vec(self.rect.x+5,self.rect.y+70)
        #################################
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.hidden is False:
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0
        
           
    def powerup(self):
        self.power += 1
        if self.power ==4:
            powship1 = Powship1(self.rect.centerx,self.rect.top)
            all_sprites.add(powship1)
            powships.add(powship1)
        if self.power ==5:
            powship2 = Powship2(self.rect.centerx,self.rect.top)
            all_sprites.add(powship2)
            powships.add(powship2)
            
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.right,self.rect.top+25)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            
            if self.power == 2:
                bullet1 = Bullet(self.rect.right,self.rect.top)
                bullet2 = Bullet(self.rect.right,self.rect.bottom +5)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()  
                
            if self.power == 3:
                bullet1 = Bullet(self.rect.right,self.rect.top)
                bullet2 = Bullet(self.rect.right,self.rect.bottom +5)
                bullet3 = Bullet2(self.rect.centerx,self.rect.top+5)
                bullet4 = Bullet3(self.rect.centerx,self.rect.bottom-5)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                shoot_sound.play()  
             
            
    def hide(self):
        #hide player ship temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT +400

SEEK_FORCE = 1.5
MAX_SPEED = 9

class Powship1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = powship_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.vel = vec(MAX_SPEED,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos

        
        #complete seek function - do not need to edit
    def seek(self,target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer
    
    
    def update(self):
        self.acc = self.seek(powship1)
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y <0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

class Powship2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = powship_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.vel = vec(MAX_SPEED,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos

        
        #complete seek function - do not need to edit
    def seek(self,target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer
        
    
    def update(self):
        self.acc = self.seek(powship2)
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y <0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos        
        
        
    
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = basicenemy_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 13
        self.rect.y = random.randrange(HEIGHT - self.rect.width)
        self.rect.x = random.randrange(WIDTH+40,WIDTH+100)
        self.speedx = -5
        self.speedy = random.randrange(-5,5)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < -10 or self.rect.bottom < -25 or self.rect.top > HEIGHT + 25:
            self.rect.y = random.randrange(HEIGHT - self.rect.width)
            self.rect.x = random.randrange(WIDTH+40,WIDTH+100)
            self.speedx = -10
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20
        
    def update(self):
        self.rect.x += self.speedx    
    #erase it if it moves off right side of screen
        if self.rect.right > WIDTH+2:
            self.kill()
            
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20
        self.speedy = 10
        
    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy
    #erase it if it moves off right side of screen
        if self.rect.right > WIDTH+2:
            self.kill()
            
            
class Bullet3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20
        self.speedy = -10
        
    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy
    #erase it if it moves off right side of screen
        if self.rect.right > WIDTH+2:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = powerup_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -2
        
    def update(self):
        self.rect.x += self.speedx    
    #erase it if it moves off right side of screen
        if self.rect.right > WIDTH+20:
            self.kill()
            
        
    def update(self):
        self.rect.x += self.speedx    
    #erase it if it moves off right side of screen
        if self.rect.right > WIDTH+20:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
            
        
#Load each graphic
background = pygame.image.load('spaceback.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load('tm3stock.png').convert()
player_mini_img = pygame.transform.scale(player_img,(34,15))
player_mini_img.set_colorkey(BLACK)
basicenemy_img = pygame.image.load('tm5.png').convert()
bullet_img = pygame.image.load('laserBlue07.png').convert()
powship_img = pygame.image.load('powship.png').convert()


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    
powerup_img = pygame.image.load('frame0.png').convert()
powerup_img.set_colorkey(BLACK)
    
#Load each game sound
player_die_sound = pygame.mixer.Sound('rumble1.ogg')
shoot_sound = pygame.mixer.Sound('Laser_Shoot.wav')
expl_sound = pygame.mixer.Sound('explosion.wav')
pow_sound = pygame.mixer.Sound('Powerup.wav')
#shield_sound = pygame.mixer.Sound('shield.wav')
pygame.mixer.music.load('cyclo.mp3')
pygame.mixer.music.set_volume(.2)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
powships = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites.add(player)
for i in range(4):
    newmob()

pygame.mixer.music.play(loops=-1)
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
    # Update
    all_sprites.update()
    # check to see if a bullet hit the mob, true means that both groups get deleted then adds new mobs for dead ones
    
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        score += 50 
        expl_sound.play()
        newmob()
        if random.random() > 0.1:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        #shield_sound.play()
        player.shield -= 50
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            
    #check to see if player obtained powerup
    hits = pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        player.powerup()
        pow_sound.play()
        
    #if player dead and explosion finished
    if player.lives == 0 and not death_explosion.alive():
        running = False
    
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, 50, 10)
    draw_shield_bar(screen, 15,45, player.shield)
    draw_lives(screen, 5, HEIGHT - 20, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



