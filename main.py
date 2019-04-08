#!/usr/bin/env python
MIN_HEIGHT = -110
MAX_HEIGHT = 831
MIN_HOR = 0
MAX_HOR = 400
SPLIT = 20
import pygame
from pygame.locals import *  # noqa
import sys
import random
from pynput.keyboard import Key, Controller


class FlappyBird:
    def __init__(self):
        self.keyboard = Controller()
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        '''''''''
        if self.birdY > 500:
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
        '''''
        if not 0 < self.bird[1] < 720:
            self.dead = True
            #no need to restart
            '''''''''
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5
            '''''

    def run(self,gene):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead:
                self.sprite = 2
                return self.counter #end game and return the score
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            text1 = "horizontal distance " + str(self.wallx) + "  height distance " + str(self.birdY - self.offset)
            print(text1)


            # to get row is height so curr - MIN_HEIGHT / SPLIT
            # to get coulmn is horizontal so curr - MIN_HORIZONTAL / SPLIT
            #choose by gene
            if(gene[round((self.wallx-MIN_HOR)/SPLIT)-1][round(((self.birdY-self.offset) - MIN_HEIGHT)/SPLIT)-1] == 1):
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)

            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()




#!/usr/bin/env python

#from flappyBird import *
import os
import random

#height (birdY - offest) -110 to 830 split to 20 it's 47 options
#horztional (wallx) 0 to 400 spilt to 20 it's 20
#total 940

def createGene():
    '''''''''
    gene = []
    count = 0
    for height in range(-110,831,20):
        for horizontal in range(0,400,20):
            gene.append([])
            gene[count].append(height)
            gene[count].append(horizontal)
            gene[count].append(random.randint(0,1))
            count += 1
    return gene
    '''''''''
    options = [0,1]
    weights = [0.90,0.1]
    return [[random.choices(options, weights)[0] for x in range(MIN_HEIGHT, MAX_HEIGHT, SPLIT)] for y in range(MIN_HOR, MAX_HOR, SPLIT)]

#to get row is height so curr - MIN_HEIGHT / SPLIT
#to get coulmn is horizontal so curr - MIN_HORIZONTAL / SPLIT
 #heigh change 1 by 20
#height 170
#hor 110
#gene 285
#((self.birdY - self.offset) / 20 * 20 ) + self.wallx / 20]
# 170 /20 * 20 + 110 /20 =
if __name__ == "__main__":
    gene = createGene()
    result = FlappyBird().run(gene)
    print("result",result)




