from pygame import *
mixer.pre_init(44100, 16, 2, 4096)
init()

w_width = 700
w_height = 600
back = (10, 55, 150)
window = display.set_mode((w_width, w_height))
display.set_caption('Лабіринт')

mixer.music.load('nyancat.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

bullet_sound = mixer.Sound("bulletsound.wav")

class GameSprite(sprite.Sprite):
    def __init__(self, pic, width, height, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pic), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, pic, width, height, x, y, speed_x, speed_y):
        GameSprite.__init__(self, pic, width, height, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def update(self):
        if hero.rect.x <= w_width - 80 and hero.speed_x > 0 or hero.rect.x >= 0 and hero.speed_x < 0:
            self.rect.x += self.speed_x
        platforms_touched = sprite.spritecollide(self, barriers, False)
        #рух вправо
        if self.speed_x > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
                
        #рух вліво
        elif self.speed_x < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                
        
        if hero.rect.y <= w_height - 80 and hero.speed_y > 0 or hero.rect.y >= 0 and hero.speed_y < 0:
            self.rect.y += self.speed_y
        platforms_touched = sprite.spritecollide(self, barriers, False)
        #рух вниз
        if self.speed_y > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
            
        #рух вгору
        elif self.speed_y < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire_1(self):
        bullet = Bullet_1('bullet_thunder.png', 25, 20, self.rect.right - 25, self.rect.centery - 16, 30)
        bullets.add(bullet)
    
    def fire_2(self):
        bullet = Bullet_2('bullet_thunder.png', 25, 20, self.rect.left - 25, self.rect.centery - 16, 30)
        bullets.add(bullet)
          


class Enemy(GameSprite):
    direction = 'left'
    def __init__(self, pic, width, height, x, y, speed):
        GameSprite.__init__(self, pic, width, height, x, y)
        self.speed = speed
    
    def update(self):
        if self.rect.x <= 370:
            self.direction = 'right'
        if self.rect.x >= w_width - 120:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    

class Enemy_1(GameSprite):
    def __init__(self, pic, width, height, x, y):
        GameSprite.__init__(self, pic, width, height, x, y)

class Enemy_2(GameSprite):
    direction = 'bottom'
    def __init__(self, pic, width, height, x, y, speed):
        GameSprite.__init__(self, pic, width, height, x, y)
        self.speed = speed

    def update(self):
        if self.rect.y >= w_height - 70:
            self.direction = 'up'
        if self.rect.y <= 400:
            self.direction = 'bottom'
        if self.direction == 'up':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Bullet_1(GameSprite):
    def __init__(self, pic, width, height, x, y, speed):
        GameSprite.__init__(self, pic, width, height, x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > w_width + 10:
            self.kill()
    
class Bullet_2(GameSprite):
    def __init__(self, pic, width, height, x, y, speed):
        GameSprite.__init__(self, pic, width, height, x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < w_width - 690:
            self.kill()


wall_1 = GameSprite('wall_g.png', 350, 20, 150, 230)
wall_2 = GameSprite('wall_v.png', 20, 400, 150, 230)
wall_3 = GameSprite('wall_g.png', 700, 20, 0, 30)
wall_4 = GameSprite('wall_v.png', 20, 250, 500, 230)
wall_5 = GameSprite('wall_g.png', 200, 20, 300, 370)
wall_6 = GameSprite('wall_g.png', 200, 20, 170, 510)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
barriers.add(wall_4)
barriers.add(wall_5)
barriers.add(wall_6)

hero = Player('nyan_cat.png', 110, 60, 5, w_height - 80, 0, 0)
final = GameSprite('portal.png', 60, 80, 430, 270)

enemy = Enemy('enemy.png', 120, 70, 600, 100, 4)
enemy_1 = Enemy_1('enemy.png', 100, 60, 320, 280)
enemy_2 = Enemy_2('enemy.png', 90, 50, 390, 400, 2)
enemies = sprite.Group()
enemies.add(enemy)
enemies.add(enemy_1)
enemies.add(enemy_2)

bullets = sprite.Group()

run = True
finish = False
while run:
    
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        
        elif ev.type == KEYDOWN:
            if ev.key == K_w:
                hero.speed_y = -5
            elif ev.key == K_a:
                hero.speed_x = -5
            elif ev.key == K_d:
                hero.speed_x = 5
            elif ev.key == K_s:
                hero.speed_y = 5
            elif ev.key == K_RIGHT:
                hero.fire_1()
                mixer.Sound.play(bullet_sound)
            elif ev.key == K_LEFT:
                hero.fire_2()
                mixer.Sound.play(bullet_sound)
        
        elif ev.type == KEYUP:
            if ev.key == K_w:
                hero.speed_y = 0
            elif ev.key == K_a:
                hero.speed_x = 0
            elif ev.key == K_d:
                hero.speed_x = 0
            elif ev.key == K_s:
                hero.speed_y = 0
        
        
    if not finish:
        
        window.fill(back)
        bullets.draw(window)
        final.draw()
        hero.draw()
        hero.update()
        
        bullets.update()
        barriers.draw(window)
        
        sprite.groupcollide(enemies, bullets, True, True)
        enemies.draw(window)
        enemies.update()
        sprite.groupcollide(bullets, barriers, True, False)
    
        if sprite.collide_rect(hero, final):
            finish = True
            mixer.music.stop()
            mixer.music.load('winsound.mp3')
            mixer.music.play(1)
            win = image.load('win.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(win, (700, 600)), (0, 0))
        if sprite.spritecollide(hero, enemies, False):
            finish = True
            mixer.music.stop()
            mixer.music.load('gameover.mp3')
            mixer.music.play(1)
            defeat = image.load('endgame.jpg')
            window.blit(transform.scale(defeat, (700, 600)), (0, 0))

       

    time.delay(35)
    display.update()
