import pygame
import sys
from pygame.locals import * # pygame 的所有常亮名导入进来WWWW

import random


pygame.init()
size = width, height = 640, 600  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
pygame.display.set_caption('lalalalala')

WBLUE = 25,155,155
GREEN = 25, 255, 15
YELLOW = 255,255,15
GRAY = 100, 100 ,100
RED = 255,0,0
BLACK = 0,0,0
WHITE = 255,255,255

v = 0 #速度
a = 0 #加速度
a_flag = 0 #加速度变化标志
cx_flag = 0 #车左右移动变化标志
pause_flag = 0
score = 0

fps = 100

potato_y = -1 #障碍物y坐标
potato_x = 0 #障碍物x坐标
stop_y = -150000 #停止点y坐标
car_x = 120 #车横坐标

ROLL = 0  #行道树坐标滚动偏移
#游戏中信息显示的字体
font = pygame.font.SysFont("宋体",30)

# 字体对象.render(文字内容,True,文字颜色,背景颜色=None)
#text = font.render('hello pygame', True, (0, 0, 255), (0, 255, 0))

# 3.显示文字
#window.blit(text, (0, 0))

def collide():
    if potato_y > 0 and abs(car_x - potato_x) < 25 and abs(potato_y - 505) < 25:
        return True

def alarm():
    if potato_y > 0 and abs(car_x - potato_x) < 25 and potato_y > stop_y:
        return True

def render():

    global stop_y
    pygame.draw.rect(screen,WBLUE,((90,0),(200,600)),0)
    
    for i in range(6):
        pygame.draw.rect(screen,GREEN,((40,i*100 + ROLL),(10,10)),8 )
        pygame.draw.rect(screen,GREEN,((350,i*100 + ROLL) ,(10,10)),8)
        pygame.draw.rect(screen,WHITE,((180,i*100 + ROLL) ,(10,30)),0)
    if potato_y > 0:
        pygame.draw.rect(screen,GRAY,((potato_x,potato_y),(20,20)),8 )
    pygame.draw.rect(screen,YELLOW,((car_x,500) ,(20,20)),10)
    pygame.draw.rect(screen,RED,((car_x + 5,stop_y),(10,10)),7)
    pygame.draw.line(screen,RED,(car_x + 10,stop_y),(car_x + 10,500),2)
    
    text_v = "speed: " + str(('%.2f' % v)) + " km/h"
    text_a = "a = " + str(a) + "  m / s^2"
    if stop_y <= -150000 :
        text_stop = "stop_dis = inf" 
    else:
        text_stop = "stop_dis = " + str(('%.2f' % (505 - stop_y)))
    text_score = "score: " + str(('%.2f' % score))
    str_v = font.render(text_v, True, (255, 255, 255), (0,0,0))
    str_a = font.render(text_a, True, (255, 255, 255), (0,0,0))
    str_s = font.render(text_stop, True, (255, 255, 255), (0,0,0))
    str_score = font.render(text_score, True, (255, 255, 255), (0,0,0))
    screen.blit(str_v, (400, 200))
    screen.blit(str_a, (400, 250))
    screen.blit(str_s, (400, 300))
    screen.blit(str_score, (400, 100))
    


def update_state():

    global v , ROLL,stop_y , a,a_flag , cx_flag,car_x ,potato_y,potato_x,score
    v = v + (a * 3.6)/fps 
    if v < 0:
        v = 0
    elif v > 400:
        v = 400
    
    if v > 700:
        pygame.draw.rect(screen,YELLOW,((600,200) ,(12,25)),0)

    ROLL = (ROLL + 1.5*v / fps) % 100


    if a_flag == 1:
        a = 40
    elif a_flag == -1:
        a = -40
    else:
        a = 0

    if cx_flag == 1:
        car_x = car_x - 5
        if car_x < 100:
            car_x = 100
    elif cx_flag == -1:
        car_x = car_x + 5
        if car_x > 260:
            car_x = 260

    if a >= 0:
        stop_y = -150000 
    else:
        pygame.draw.rect(screen,RED,((600,300) ,(12,25)),0)
        stop_y = 505 - v*v/ (2*(-a) * fps / 43)

    if potato_y < 0 and random.randint(0,10000) < 600:
        potato_y = 1
        potato_x = random.randint(100,260)
    
    if potato_y > 0:
        potato_y = potato_y + 1.5*v / fps
    
    if potato_y > height:
        potato_y = -1
        score = score + v*14.8/30

    if collide():
        score = score - 5.8 * v 
        a = 0
        v = 0
        screen.blit(font.render("Collide!", True, (0, 0, 0), (255, 0, 0)), (400, 350))
        pause_flag = 1
        
    
    if alarm():
        screen.blit(font.render("Alarm!", True, (0, 0, 0), (0,100, 200)), (400, 400))
    
    score = score + v * 0.205/152
        
    
    


while True:  # 死循环确保窗口一直显示

    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
             sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                a_flag = 1            
            elif event.key == K_s:
                a_flag = -1
            elif event.key == K_a:
                cx_flag = 1
            elif event.key == K_d:
                cx_flag = -1
        if event.type == pygame.KEYUP:
            a_flag = 0
            cx_flag = 0
            pause_flag = 0
    
    if not pause_flag:
        update_state()
        pygame.display.update()
        pygame.time.wait(int(1000 / fps))
        
        pygame.draw.rect(screen,BLACK,((0,0) ,(width,height)),0)
        render()

pygame.quit()  # 退出pygame