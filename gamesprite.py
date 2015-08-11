# coding: utf-8

import pygame
from pygame.locals import *
from gameutil import *

class GameSprite():
    '''
    It doen't inherit pygame's Sprite class because Sprite capabilities are not necessary.
    '''
    
    def __init__(self, image):
        self._image = image
        self._width = self._image.get_width()
        #print "width %d" % self._width
        self._height = self._image.get_height()
        self._vx = -1
        self._vy = -1
        self._rect = Rect(self._vx, self._vy, self._width, self._height)
        #self._rect = None
            
    def update(self, x, y):
        #I don't know why the rect moves every time.
        #self._vx = x
        #self._vy = y
        #self._rect.move_ip(self._vx, self._vy)
        if self._vx != x and self._vy != y:
            #self._rect.move(self._vx, self._vy)
            self._rect = Rect(x, y, self._width, self._height)
            self._vx = x
            self._vy = y
        
    def draw(self, screen):
        #if self._image != None:
        #    print "here image check"
        screen.blit(self._image, self._rect)
        
    def get_locx(self):
        return self._vx
        
    def get_locy(self):
        return self._vy

class Capital(GameSprite):
    
    def __init__(self):
        image = pygame.image.load("./image/Capital.png").convert_alpha()        
        GameSprite.__init__(self, image)

class OilDerrickInSearch(GameSprite):
    
    ANIMATION_IMAGE_NUMBER = 3
    ANIMATION_CYCLE = 2
    
    def __init__(self):
        self._image = pygame.image.load("./image/OilDerrickInSearch.png").convert_alpha()
        self._width = self._image.get_width() / self.ANIMATION_IMAGE_NUMBER
        self._height = self._image.get_height()
        self._vx = -1
        self._vy = -1
        self._rect = None
        self._frame = 0
        
    def _split_image(self, image):
        imageList = []
        #from gamelauncher import *
        for i in range(self.ANIMATION_IMAGE_NUMBER):
            surface = pygame.Surface((32, 32))
            surface.blit(image, (0, 0), (0 + GameConstUtil.get_sprite_size() * i, 0, GameConstUtil.get_sprite_size(), GameConstUtil.get_sprite_size()))
            imageList.append(surface)
        return imageList        
        
    def draw(self, screen):
        img_list = self._split_image(self._image)
        self._frame = self._frame + 1
        #print "frame = %d" % self._frame
        img_num = self._frame / self.ANIMATION_CYCLE % self.ANIMATION_IMAGE_NUMBER        
        #print "img_num = %d" % img_num
        screen.blit(img_list[img_num], self._rect)
