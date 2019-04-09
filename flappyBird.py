#!/usr/bin/env python
MIN_HEIGHT = -110
MAX_HEIGHT = 831
MIN_HOR = 0
MAX_HOR = 400
SPLIT = 15

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
        self.timeLive = 0
        self.offset = random.randint(-110, 110)

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            print('*****************************************************************************************')
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
        #360 + 130 - X + 10 - 65
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
            clock.tick(500000000)
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
                # 360 + 130 - X + 10 - 65
                #360+130-x, 600-380
                distanceFromPass = abs(self.birdY - (360+130 -self.offset + 10 - 65))
                #print("close to pass", self.birdY - (360+130 -self.offset + 10 - 65))
                #        print("gene fitness is:",self.timeLive - (1 / 20 *    distanceFromPass  )+ 1000 *self.counter) #time - distnace from open pipe + big bomus on points
                return (self.timeLive - (1/20 * distanceFromPass  )+ 1000 *self.counter) #end game and return the score
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            #text1 = "horizontal distance " + str(self.wallx) + "  height distance " + str(self.birdY - self.offset)
            #print(text1)


            # to get row is height so curr - MIN_HEIGHT / SPLIT
            # to get coulmn is horizontal so curr - MIN_HORIZONTAL / SPLIT
            #choose by gene
            try:
                if (gene[round((self.wallx - MIN_HOR) / SPLIT) - 1][round(((self.birdY - self.offset) - MIN_HEIGHT) / SPLIT) - 1] == 1):
                    self.keyboard.press(Key.space)
                    self.keyboard.release(Key.space)
            except:
                print("horizontal index:",round((self.wallx - MIN_HOR) / SPLIT) - 1,"height index",round(((self.birdY - self.offset) - MIN_HEIGHT) / SPLIT) - 1)

            self.updateWalls()
            self.birdUpdate()
            self.timeLive += 1
            pygame.display.update()


def start(gene):
    return FlappyBird().run(gene)