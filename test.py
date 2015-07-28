# coding: utf-8

import pygame
from pygame.locals import *
import sys
import random
 
def main():  
    SCR_WIDTH,SCR_HEIGHT = 640,480
     
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
    pygame.display.set_caption(u"画像の移動と跳ね返り処理")
     
    img = pygame.image.load("./image/zam.png").convert_alpha()
    img_rect = img.get_rect()
     
    sound = pygame.mixer.Sound("./sound/beep.wav")
     
    vx = vy = 2  # 1フレームの移動ピクセル
    clock = pygame.time.Clock()
     
    while True:
        clock.tick(60)  # 60fps
        
        # 画像の移動
        img_rect.move_ip(vx, vy)
        # 跳ね返り処理
        if img_rect.left < 0 or img_rect.right > SCR_WIDTH:
            sound.play()
            vx = -vx
        if img_rect.top < 0 or img_rect.bottom > SCR_HEIGHT:
            vy = -vy
            sound.play()
        
        screen.fill((0,0,0))
        screen.blit(img, img_rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE: sys.exit()
        
if __name__ == "__main__":
    main()
       
    