from random import *
from math import *
import pygame
from utilities import *
from der_mann import *
pygame.init()
win=pygame.display.set_mode((1200,600))
run=True
class Automobile:
    def __init__(self):
        #Vectorial movement setup
        self.x=0
        self.y=0
        self.xspeed=0
        self.yspeed=0
        self.vectors=[]
        self.movement_angle=0

        self.acceleration=4
        self.max_speed=40
        self.angle=pi/2
        self.speed=0
        self.total_speed=0
        self.aspeed=0
        self.drift_conversion=False

        self.sprite=pygame.image.load("assets/cars/coupe_red.png")
        #self.sprite=pygame.transform.scale(self.sprite,(31,3000))
        
        self.length=self.sprite.get_height()/2 #fuck it i'm making the sprite like this
        self.width=self.sprite.get_width()/2
        self.wheel_rotation=0

        self.drifting=False
        self.drift_marks=[]
        self.last_drift_mark=0

        self.player=Player()
        self.player.driving_disability=1
        self.wheel_acceleration=0 #actual physics term, trust me
        self.wheel_jerk=0
        self.temporal_perception=1
        self.temporal_acceleration=0
    def control(self):  
        self.keys=pygame.key.get_pressed() 
        is_key_down=False
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            self.wheel_rotation-=0.001*dt
            is_key_down=True
        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            self.wheel_rotation+=0.001*dt
            is_key_down=True
        if not is_key_down:
            if random()<0.02*dt:
                self.wheel_jerk=min(0.005*self.player.driving_disability,max(-0.005*self.player.driving_disability,self.wheel_jerk+(random()*self.player.driving_disability/40000)*(randint(0,1)*2-1)))
            self.wheel_acceleration+=self.wheel_jerk
            if abs(self.wheel_acceleration)>=0.015:
                self.wheel_jerk=-self.wheel_jerk
            if abs(self.wheel_rotation)<=0.001:
                self.wheel_rotation=0
            elif abs(self.wheel_acceleration)<0.00005:
                if self.wheel_rotation>0:
                    self.wheel_rotation-=0.001*dt
                else:
                    self.wheel_rotation+=0.001*dt
        else:
            pass
            self.wheel_acceleration=0
            self.wheel_jerk=0
            self.xspeed*=1-0.04*dt
            self.yspeed*=1-0.04*dt
        self.wheel_rotation=max(-0.05,min(0.05,self.wheel_rotation+self.wheel_acceleration*dt))
        self.angle+=(self.wheel_rotation)*dt*self.speed/self.max_speed
        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]: # We simulate real fun
            self.speed+=self.acceleration
            self.speed=min(self.max_speed,self.speed)
        elif self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
            self.speed*=0.97
            self.xspeed*=1-0.2*dt
            self.yspeed*=1-0.2*dt
        if self.keys[pygame.K_SPACE] or self.drifting:
            self.drifting=(abs(self.angle%tau-self.movement_angle%tau)>(pi/5)) and (self.total_speed>(self.max_speed/8))
        else:
            self.drifting=False
        if self.drifting or self.keys[pygame.K_SPACE]:
            self.vectors.append((cos(self.angle)*self.speed/1000,sin(self.angle)*self.speed/1000))
            self.drift_conversion=False
        else:
            if not self.drift_conversion:
                self.drift_conversion=True
                deadzone=2
                self.aspeed=max(0,deadzone-abs(self.angle%tau-self.movement_angle%tau))/deadzone*self.speed
            self.aspeed+=(self.speed-self.aspeed)/40*dt
            self.xspeed=cos(self.angle)*self.aspeed/3
            self.yspeed=sin(self.angle)*self.aspeed/3
        #print(self.total_speed,(self.max_speed/10))
        if random()<0.02*dt or self.temporal_perception in (0.5,2):
            self.temporal_acceleration+=(randint(0,1)*2-1)*random()*self.player.temporal_perception/10000
            self.temporal_acceleration=max(-0.001,min(0.001,self.temporal_acceleration))
        self.temporal_perception+=self.temporal_acceleration
        self.temporal_perception=max(1/(1+self.player.temporal_perception),min((1+self.player.temporal_perception),self.temporal_perception))
    def move(self):
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.x+=self.xspeed*dt
        self.xspeed*=1-0.01*dt
        self.y+=self.yspeed*dt
        self.yspeed*=1-0.01*dt
        self.total_speed=sqrt(self.xspeed**2+self.yspeed**2)
        if self.total_speed>0:
            self.movement_angle=atan2(self.yspeed,self.xspeed)
        self.outer_points=[
            (cos(self.angle)*self.length+cos(self.angle+pi/2)*self.width,sin(self.angle)*self.length+sin(self.angle+pi/2)*self.width),
            (cos(self.angle)*self.length-cos(self.angle+pi/2)*self.width,sin(self.angle)*self.length-sin(self.angle+pi/2)*self.width),
            (-cos(self.angle)*self.length-cos(self.angle+pi/2)*self.width,-sin(self.angle)*self.length-sin(self.angle+pi/2)*self.width),
            (-cos(self.angle)*self.length+cos(self.angle+pi/2)*self.width,-sin(self.angle)*self.length+sin(self.angle+pi/2)*self.width),
        ]
        self.wheels=[(i[0]/1.1,i[1]/1.1) for i in self.outer_points]
        self.front_hits=[
            (cos(self.angle)*self.length+cos(self.angle+pi/2)*self.width*(1-2*i/10),sin(self.angle)*self.length+sin(self.angle+pi/2)*self.width*(1-2*i/10)) for i in range(11)            
        ]
    def draw(self,surface):
        for i in self.drift_marks:
            pygame.draw.rect(surface,(15,15,15),[i[0]+camera_x_offset-self.x-2,i[1]+camera_y_offset-self.y-2,4,4])
        center(pygame.transform.rotate(self.sprite,-self.angle/tau*360-90),surface,camera_x_offset,camera_y_offset)
        #pygame.draw.polygon(surface,(255,234,23),[(i[0]+camera_x_offset,i[1]+camera_y_offset) for i in self.outer_points])
        for i in range(3):
            i-=0.25
            pygame.draw.polygon(surface,(138/1.2,255/1.2,207/1.2),(
                (
                    1100+cos(self.wheel_rotation*tau/0.05+i/3*tau)*18+cos(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*4,
                    500+sin(self.wheel_rotation*tau/0.05+i/3*tau)*18+sin(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*4
                    ),
                (
                    1100+cos(self.wheel_rotation*tau/0.05+i/3*tau)*70+cos(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*9,
                    500+sin(self.wheel_rotation*tau/0.05+i/3*tau)*70+sin(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*9
                    ),
                (
                    1100+cos(self.wheel_rotation*tau/0.05+i/3*tau)*70-cos(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*9,
                    500+sin(self.wheel_rotation*tau/0.05+i/3*tau)*70-sin(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*9
                    ),
                (
                    1100+cos(self.wheel_rotation*tau/0.05+i/3*tau)*18-cos(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*4,
                    500+sin(self.wheel_rotation*tau/0.05+i/3*tau)*18-sin(self.wheel_rotation*tau/0.05+i/3*tau+pi/2)*4
                    ),
                
            ))
        pygame.draw.circle(surface,(138,255,207),(1100,500),80,15)
        pygame.draw.circle(surface,(138,255,207),(1100,500),20)
        if self.drifting:
            self.last_drift_mark+=self.total_speed*dt
            if self.last_drift_mark>5:
                if len(self.drift_marks)>200:
                    self.drift_marks.pop(0)
                    self.drift_marks.pop(0)
                    self.drift_marks.pop(0)
                    self.drift_marks.pop(0)
                self.drift_marks.append((self.x+self.wheels[2][0],self.y+self.wheels[2][1],self.angle))
                self.drift_marks.append((self.x+self.wheels[3][0],self.y+self.wheels[3][1],self.angle))
                self.drift_marks.append((self.x+self.wheels[1][0],self.y+self.wheels[1][1],self.angle))
                self.drift_marks.append((self.x+self.wheels[0][0],self.y+self.wheels[0][1],self.angle))
                
                self.last_drift_mark=0
        pygame.draw.line(surface,(255,0,125),(5,300),(5,300+self.wheel_acceleration*30000),5)
        pygame.draw.line(surface,(125,0,255),(10,200),(10,self.temporal_perception*200),5)
        
camera_x_offset=600
camera_y_offset=300
car=Automobile()
clock=pygame.time.Clock()
while run:
    clock.tick()
    FPS=clock.get_fps()
    dt=60/(FPS+1)
    dt*=(car.temporal_perception)
    if dt>5:
        dt=5
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((55,55,55))
    for i in range(13):
        y_offset=-car.y%50
        for ii in range(10):
            ii-=4.5
            pygame.draw.rect(win,(255,255,255),(600-car.x-3+ii*60,y_offset-10+i*50,6,20))
    pygame.draw.rect(win,(255,255,255),(600-3-330-car.x,0,6,600))
    pygame.draw.rect(win,(255,255,255),(600-3+330-car.x,0,6,600))
    
    car.control()
    car.move()
    car.draw(win)
    pygame.display.update()
pygame.quit()