import pygame as pg
from pygame.locals import *
import random
import math
#from denemefonksiyonlar import mousecollide
vec = pg.math.Vector2

pg.init()
clock = pg.time.Clock()
fps = 90
run = True
#screen
WIDTH = 1300
HEIGHT = 700
time_now = pg.time.get_ticks()
time_now2 = pg.time.get_ticks()
screen = pg.display.set_mode((WIDTH,HEIGHT))
#color
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
CYAN = (122,122,122)
BLACK = (0,0,0)

pg.display.set_caption('Feza')
#Load images
lasers = {'lasergreen':'Feza/graphs/resimler/PNG/Lasers/laserGreen11.png',
          'laserblue':['Feza/graphs/resimler/PNG/Lasers/laserBlue{}.png'.format(random.randint(12,16))]}
bg = pg.image.load('Feza/graphs/resimler/Backgrounds/bg5.jpg').convert()
bg = pg.transform.scale(bg,(WIDTH,HEIGHT))
#   Player lives
livepic = pg.image.load('Feza/graphs/resimler/PNG/UI/playerLife2_green.png')
#power ups
powerkamus = {'bold':['Feza/graphs/resimler/PNG/Power-ups/bold_silver.png'],'shield':['Feza/graphs/resimler/PNG/Power-ups/shield_silver.png']}
ptime = pg.time.get_ticks()
#shield power up image
shieldimage = pg.image.load('Feza/graphs/resimler/PNG/Effects/shield2.png').convert_alpha()

#Planets
planetdic = {'planets':[]}
imagestoload = ['Feza/graphs/resimler/saturne.png','Feza/graphs/resimler/jupiter.png','Feza/graphs/resimler/venus.png','Feza/graphs/resimler/uranus.png','Feza/graphs/resimler/neptune.png']
for i in imagestoload:
    img = pg.image.load(i).convert_alpha()
    planetdic['planets'].append(img)

explosion_anim = {}
explosion_anim['expl'] = []
for i in range(3):
    filename = 'Feza/graphs/resimler/explosion{}.png'.format(i)
    img = pg.image.load(filename).convert()
    img.set_colorkey(BLACK)
    explosion_anim['expl'].append(img)

#definate_time
last_time = pg.time.get_ticks()

#functions
font = pg.font.SysFont('Bauhaus',60)
def draw_text(text,font,textc,x,y):
    img = font.render(text,True,textc)
    screen.blit(img,(x,y))
def draw_percantagebar(x,y,percantage):

    if percantage > 100:
        percantage = 100
    bar_length = 100
    bar_height = 10
    pct = (percantage/100) * bar_length
    outer_bar = pg.Rect(x,y,bar_length,bar_height)
    inner_bar =  pg.Rect(x, y, pct, bar_height)
    pg.draw.rect(screen,RED,outer_bar)
    pg.draw.rect(screen,GREEN,inner_bar)

#Draw player lifes

playerimg = pg.image.load('Feza/graphs/resimler/png/playerShip2_green.png').convert()
mini = pg.transform.scale(playerimg,(25,19))
playerimg.set_colorkey(BLACK)
def player_live_function(life,x,y,pic):
    for i in range(life):
        img = pic   
        rec = img.get_rect()
        rec.x = x + 30 * i
        rec.y = y
        screen.blit(img,rec)
player_live_function(3,WIDTH-100,20,mini)

class Planets(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
             

    def update(self):
        #self.acc = vec(0,0)
        self.pos.x += -(self.vel.x)*(0.0033)
        self.pos.y += -(self.vel.y)*(0.0033)
        self.rect.center = self.pos
        #print(self.center,'cos',self.movex*math.cos(math.radians(self.direction)),'direction',self.direction,'cosaçı',math.cos(math.radians(self.direction)))
        #print(self.rect.center,'movex',self.movex*math.cos(math.radians(self.direction-90)),'cos',math.cos(math.radians(self.direction-90)))
#[[650.0, 175.0], [650.0, 233.33333333333334], [650.0, 350.0]]


class Player(pg.sprite.Sprite): 
    def __init__(self,x,y,image):
        self.copyimg = pg.image.load(image).convert_alpha()
        pg.sprite.Sprite.__init__(self)
        self.image = self.copyimg.copy()
        #self.copyimg.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        #pg.draw.circle(self.copyimg,RED,self.rect.center,self.radius)
        self.rect.center = (x,y)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed =  0.3
        self.friction = -0.02
        self.rot = 45
        self.random_move = ['İleri','Geri']
        self.chasex = True
        self.chasey = True
        self.directing = 1
        self.times = pg.time.get_ticks()
        self.mainmenu = True
        self.now = pg.time.get_ticks()
    def rotate(self):
        self.rot = self.rot % 360
        newimage = pg.transform.rotate(self.copyimg,int(self.rot%360))
        
        #pg.draw.rect(screen,WHITE,self.rect,5)
        #old_center = self.rect.center
        self.image = newimage
        self.rect = self.image.get_rect()
        #self.rect.center = old_center   

    def shoot(self):
        bullet = BulletPlayer(self.pos.x,self.pos.y,self.rot,lasers['laserblue'][random.randint(0,len(lasers['laserblue'])-1)])
        bulletgroupenemy.add(bullet)
    
    def update(self):
        
        if pg.time.get_ticks() - self.now > 900 and self.mainmenu == False:
            self.shoot()
            self.now = pg.time.get_ticks()
        rasthareket = random.randint(0,100)
        keys = pg.key.get_pressed()
        if self.mainmenu:
            self.mainmenuscreen()
        if not self.mainmenu:
            self.acc = vec(0,0)
            self.rotate()

            if self.chasex:
                self.acc.x = self.speed*math.cos(math.radians(self.rot+90))
            if not self.chasex:
                self.acc.x = self.acc.x* (-1)
                
            if self.chasey:
                self.acc.y = self.speed*math.sin(math.radians(self.rot-90))

            if not self.chasey:
                self.acc.y =  self.acc.y*(-1)

            if self.pos.x > WIDTH:
                self.pos.x = 0
            elif self.pos.x < 0:
                self.pos.x = WIDTH
            if self.pos.y > HEIGHT:
                self.pos.y = 0
            elif self.pos.y < 0:
                self.pos.y = HEIGHT
            
            self.acc += self.vel * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.center = self.pos        
    def mainmenuscreen(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.mainmenu = False
        if self.mainmenu:
            self.rotate()
            
            if self.mainmenu:
                self.acc.x = self.speed*math.cos(math.radians(self.rot+90))
            if not self.mainmenu:
                self.acc.x = self.acc.x* (-1)
                
            if self.mainmenu:
                self.acc.y = self.speed*math.sin(math.radians(self.rot-90))

            if not self.mainmenu:
                self.acc.y =  self.acc.y*(-1)

            if self.pos.x > WIDTH:
                self.pos.x = 0
            elif self.pos.x < 0:
                self.pos.y = random.randint(HEIGHT,HEIGHT + 100)
                self.rot = random.randint(0,70)
                self.pos.x = random.randint(300,WIDTH)
            if self.pos.y > HEIGHT+300:
                self.pos.y = 0
            elif self.pos.y < 0:
                self.pos.y = random.randint(HEIGHT,HEIGHT + 100)
                self.rot = random.randint(0,70)
                self.pos.x = random.randint(300,WIDTH)
            self.acc += self.vel * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.center = self.pos        
        
class Player2(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        self.mainmenu = True
        self.copyimg = pg.image.load(image).convert_alpha()
        pg.sprite.Sprite.__init__(self)
        self.image = self.copyimg.copy()
        #self.copyimg.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        #pg.draw.circle(self.copyimg,RED,self.rect.center,self.radius)
        self.rect.center = (x,y)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed =  0.3
        self.friction = -0.02
        self.rot = 90
        #self.mainmenuscreen = True
        self.live = 3
        self.hidetimer = pg.time.get_ticks()
        self.hitted = False
        self.bolt = 2000
        self.bolt_time = pg.time.get_ticks()
        self.shield_time = pg.time.get_ticks()
        
    def rotate(self):
        self.rot = self.rot % 360
        #self.oldrot = self.rot 
        newimage = pg.transform.rotate(self.copyimg,self.rot)
       
        self.image = newimage
        self.rect = self.image.get_rect()
    def shoot(self):
        bullet = BulletPlayer(self.rect.centerx,self.rect.centery,self.rot,lasers['lasergreen'])
        bulletgroup.add(bullet)
    
    def hit(self):
        self.hidetimer = pg.time.get_ticks()
        self.hitted = True


    def update(self):
        self.acc = vec(0,0)
        self.rotate()
        
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.acc.y,self.acc.x = self.speed*math.sin(math.radians(self.rot-90)),self.speed*math.cos(math.radians(self.rot+90))
        elif keys[pg.K_DOWN]:
            self.acc.y,self.acc.x = -0.5*self.speed*math.sin(math.radians(self.rot-90)),-0.5*self.speed*math.cos(math.radians(self.rot+90))
         
        if keys[pg.K_RIGHT]:
            self.rot -= self.speed + 1
        if keys[pg.K_LEFT]:
            self.rot += self.speed + 1

        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT  
       
        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

class BulletPlayer(pg.sprite.Sprite):
    def __init__(self,x,y,rotation,image):
        pg.sprite.Sprite.__init__(self)
        self.cop = pg.image.load(image).convert_alpha()
        self.image = self.cop.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.shootspeed = 10
        self.rotation = rotation

    def update(self):
        self.rotation = self.rotation % 360
        newimage = pg.transform.rotate(self.cop,int(self.rotation))
        oldcenter = self.rect.center
        self.image = newimage
        self.rect = self.image.get_rect()   
        self.rect.center = oldcenter
        
        keys = pg.key.get_pressed()
        self.rect.x += self.shootspeed*math.cos(math.radians(self.rotation+90))
        self.rect.y += self.shootspeed*math.sin(math.radians(self.rotation-90))
        if self.rect.x < 0 or self.rect.x >WIDTH or self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()
        
class Explosion(pg.sprite.Sprite):
    def __init__(self,center):
        pg.sprite.Sprite.__init__(self)
        self.image = explosion_anim['expl'][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim['expl']):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim['expl'][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerups(pg.sprite.Sprite):
    def __init__(self,attribute):
        pg.sprite.Sprite.__init__(self)
        self.attribute = attribute
        self.image = pg.image.load(powerkamus[self.attribute][0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    

class Shield(pg.sprite.Sprite):
    def __init__(self,x,y,rot):
        pg.sprite.Sprite.__init__(self)
        self.copyimg = shieldimage
        self.image = self.copyimg.copy()
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.pos = vec(0,0)
        self.rot = rot

    def update(self,pos,rot):  
        image = pg.transform.rotate(self.copyimg,rot)
        oldcenter = self.rect.center
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        self.rect.center = pos
        

powerups_group = pg.sprite.Group()
allsprites = pg.sprite.Group()
playergroup = pg.sprite.Group()
bulletgroup = pg.sprite.Group()
playerkeste = pg.sprite.Group()
bulletgroupenemy = pg.sprite.Group()
planetgroup = pg.sprite.Group()
shieldgroup = pg.sprite.Group()
planetlist =  [Planets(random.randint(100,1500),random.randint(100,600),planetdic['planets'][0]),Planets(random.randint(100,1500),random.randint(100,600),planetdic['planets'][2]),
               Planets(random.randint(100,1500),random.randint(100,600),planetdic['planets'][1])]
for i in planetlist:
    planetgroup.add(i)

#[Player(300,200,'Feza/graphs/resimler/png/playerShip2_blue.png'),Player(800,500,'Feza/graphs/resimler/png/playerShip2_blue.png')]
playerlist1 = [(400,600,'Feza/graphs/resimler/png/playerShip3_blue.png')]
playerlist = []
for players in range(0,len(playerlist1)):
    p = Player(*playerlist1[players])
    playerlist.append(p)
    playergroup.add(p)
    #allsprites.add(p)
angle = 270
mainplayer = Player2(1000,600,'Feza/graphs/resimler/png/playerShip2_green.png')
levellist = [(800,500,'Feza/graphs/resimler/png/playerShip2_blue.png'),(600,900,'Feza/graphs/resimler/png/playerShip2_blue.png'),(1300,520,'Feza/graphs/resimler/png/playerShip2_blue.png'),
            (13,96,'Feza/graphs/resimler/png/playerShip2_blue.png'),(789,32,'Feza/graphs/resimler/png/playerShip2_blue.png'),(325,10,'Feza/graphs/resimler/png/playerShip2_blue.png')]
playerkeste.add(mainplayer)
#allsprites.add(mainplayer.planet)

b = 0
a = 0
c=0
oyun = ''
level = 0
true = False
while run:    
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if pg.time.get_ticks() - time_now2 > mainplayer.bolt:
                    mainplayer.shoot()
                    time_now2 = pg.time.get_ticks()
            
    # rotate each player to each other    
    
    if playerlist[0].mainmenu:
        bulletgroup.empty()
        bulletgroupenemy.empty()
        #print(playerlist[0].mainmenu,playerlist[0])
        #print(b)
        screen.fill(BLACK)
        draw_text('Galactic Fighters',font,RED,WIDTH/4 + 180,HEIGHT/6)
        draw_text('    Press "E" to start',font,WHITE,WIDTH/4 + 150,HEIGHT/4.5)
        draw_text('    Level:'+str(level+1),font,WHITE,WIDTH/4 + 150,HEIGHT/3.8)
        draw_text(oyun,font,WHITE,WIDTH/4+350,HEIGHT/3)
        mainplayer.hitted = False            

        if b >= 1:
            if oyun == 'Kazandın':
                level += 1
                for i in range(level-1,level):
                    #print(level-1,level)
                    playerlist1.append(levellist[i])
            elif oyun == 'Kaybettin':
                print('kaeeee')
                playerlist1 = [(400,600,'Feza/graphs/resimler/png/playerShip3_blue.png')]
                #playerlist1.add(Player(800,500,'Feza/graphs/resimler/png/playerShip2_blue.png'))
            mainplayer.pos.x = WIDTH/2
            mainplayer.pos.y = HEIGHT/2   
            #playerlist1 = [(300,200,'Feza/graphs/resimler/png/playerShip1_blue.png')]
            playerlist = []
            playergroup = pg.sprite.Group()
            for players in range(0,len(playerlist1)):
                p = Player(*playerlist1[players])
                playerlist.append(p)
                playergroup.add(p)
                
        b = 0
        playergroup.update()
        playergroup.draw(screen)


    else:
        screen.fill(BLACK)
        screen.blit(bg, (0, 0))
        setr = pg.time.get_ticks()
        #playerlist[i].shoot()
        # Bot Controls!!!
        for i in range(0,len(playerlist)):
            x = (playerlist[i].pos.x - mainplayer.pos.x)
            y = (playerlist[i].pos.y - mainplayer.pos.y)
            tancant = math.degrees(math.atan(y/x))

            if x < 0 and y < 0:
                angle = 270
                dönüş = -1
            if x > 0 and y > 0:
                angle = 90
                dönüş = 1
            if x < 0 and y > 0:
                angle = 270
                dönüş = 1
            if x > 0 and y < 0:
                angle = 90
                dönüş = -1
            toplam = angle - int(tancant)


            if playerlist[i].rot !=  (angle - int(tancant)):    
                if (angle - int(tancant) + 360 - playerlist[i].rot)%360 > 180:
                    playerlist[i].rot += -1
                    if pg.time.get_ticks() - playerlist[i].times > 500:
                        playerlist[i].times = pg.time.get_ticks()
                if (angle - int(tancant) + 360 - playerlist[i].rot)%360 < 180:
                    playerlist[i].rot += 1
                    if pg.time.get_ticks() - playerlist[i].times > 500:
                        playerlist[i].times = pg.time.get_ticks()
            else:
                if pg.time.get_ticks() - playerlist[i].times > 500:
                    playerlist[i].times = pg.time.get_ticks()
            
            
            if playerlist[i].pos.x  < mainplayer.pos.x :
                playerlist[i].chasex = True
                playerlist[i].directing = 1
            if playerlist[i].pos.x  > mainplayer.pos.x :
                playerlist[i].chasex = True
                playerlist[i].directing = -1

            if playerlist[i].pos.y < mainplayer.pos.y :
                playerlist[i].chasey = True
                playerlist[i].directing = 1

            if playerlist[i].pos.y > mainplayer.pos.y:
                playerlist[i].chasey = True
                playerlist[i].directing = -1

            if abs(playerlist[i].pos.x - mainplayer.pos.x) < 400 :
                playerlist[i].chasex = False
                
            if abs(playerlist[i].pos.y - mainplayer.pos.y) < 400:
                playerlist[i].chasey = False
            
            if len(playerlist) != 1:

                if abs(playerlist[i].pos.x - playerlist[i-1].pos.x) < 100 :
                    playerlist[i].chasex = True
                    
                if abs(playerlist[i].pos.y - playerlist[i-1].pos.y) < 100:
                    playerlist[i].chasey = True
            

            botx = (playerlist[i].pos.x - playerlist[i-1].pos.x)
            boty = (playerlist[i].pos.y - playerlist[i-1].pos.y)
            bottancant = math.degrees(math.atan(y/x))

            hitsenemy = pg.sprite.groupcollide(playergroup,bulletgroup,True,True)
            for hit in hitsenemy:
                expl = Explosion(hit.rect.center)
                allsprites.add(expl)
                mainplayer.hit()
                mainplayer.hitted = False

            if len(playergroup) == 0 and pg.time.get_ticks() - mainplayer.hidetimer > 100:
                playerlist[0].mainmenu = True
                b+=1
                oyun = 'Kazandın'
                
                
            hitsmainplayer = pg.sprite.spritecollide(mainplayer,bulletgroupenemy,True)

            if hitsmainplayer :
                expl = Explosion(mainplayer.rect.center)
                allsprites.add(expl)
                if not true:
                    mainplayer.hit()
                
            if mainplayer.hitted and pg.time.get_ticks() - mainplayer.hidetimer > 100:
                playerlist[0].mainmenu = True
                b+=1
                mainplayer.hitted = False
                oyun = 'Kaybettin'
                level = 0
            
        
            if random.random() > 0.95 and len(powerups_group) < 1:
                powerup = Powerups(random.choice(['bold','shield']))
                powerups_group.add(powerup)
            #print(pg.time.get_ticks() - ptime)

            """
            if len(powerups_group) != 0 and pg.time.get_ticks() - ptime > 2000:
                powerups_group.sprites()[0].kill()
                ptime = pg.time.get_ticks()
            """
            hitspowerup = pg.sprite.spritecollide(mainplayer,powerups_group,True)

            if hitspowerup:
                ptime = pg.time.get_ticks()
                print(powerup.attribute)
                if powerup.attribute == 'bold':
                    mainplayer.bolt = 500
                    mainplayer.bolt_time = pg.time.get_ticks()
                if powerup.attribute == 'shield':
                    true = True
                    mainplayer.shield_time = pg.time.get_ticks()
                    shield = Shield(mainplayer.pos.x,mainplayer.pos.y,mainplayer.rot)
                    shieldgroup.add(shield)
                    
                    #player_live_function(3,WIDTH-100,20,mini)
            if pg.time.get_ticks() - mainplayer.bolt_time > 5000:
                mainplayer.bolt = 2000                    

        #print(playergroup.sprites())

        planetlist[c%len(planetlist)].vel.x = mainplayer.vel.x
        planetlist[c%len(planetlist)].vel.y = mainplayer.vel.y
        c+=1
            
        #screen.fill(BLACK)
        #screen.blit(bg, (0, 0))
        planetgroup.update()
        planetgroup.draw(screen)
        allsprites.update()
        allsprites.draw(screen)
        playergroup.update()
        playergroup.draw(screen)
        playerkeste.update()
        playerkeste.draw(screen)
        bulletgroup.update()
        bulletgroup.draw(screen)
        bulletgroupenemy.update()
        bulletgroupenemy.draw(screen)
        powerups_group.update()
        powerups_group.draw(screen)
        
        if true and pg.time.get_ticks() - mainplayer.shield_time < 10000:
            
            shieldgroup.update(mainplayer.rect.center,mainplayer.rot)
            shieldgroup.draw(screen)
        
        if pg.time.get_ticks() - mainplayer.shield_time > 10000:
            true = False
        
        if len(shieldgroup) > 1:
            shield.kill() 
            
            
            
        player_live_function(3,WIDTH-100,20,mini)
        #mousecollide(100,100)
    pg.display.update()
pg.quit()


"""
arkadaşlar konu ile alakasız ama kafama çok takıldı da ondan sormam gerekliydi, şimdi maliyet hocası ödevi anlatırken şu attığım tabloyu çizdi ve tabloda
1. dağıtım 2. dağıtım yaparken sabit ve değişken maliyetlerini çizdi biz dağıtım yaparken sabit ve değişkenli yapmadık hiç

"""
