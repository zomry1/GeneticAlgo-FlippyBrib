#!/usr/bin/env python
MIN_HEIGHT = -110
MAX_HEIGHT = 831
MIN_HOR = 0
MAX_HOR = 400
SPLIT = 15

POPULATION = 52


import flappyBird as fb
import random

#height (birdY - offest) -110 to 830 split to 20 it's 47 options
#horztional (wallx) 0 to 400 spilt to 20 it's 20
#total 940

def createGene():
    options = [0,1]
    weights = [0.90,0.1]
    return [[random.choices(options, weights)[0] for x in range(MIN_HEIGHT, MAX_HEIGHT, SPLIT)] for y in range(MIN_HOR, MAX_HOR, SPLIT)]

def createGeneration():
    generation = []
    for i in range(POPULATION):
        generation.append(createGene())
    return generation

def fitnessGeneration(generation):
    fitnessGene = []
    for index,gene in enumerate(generation):
        fitnessGene.append([])
        fitnessGene[index].append(gene)
        result  = fitness(gene)
        fitnessGene[index].append(result)
    fitnessGene.sort(key=takeSecond)
    return fitnessGene

def takeSecond(elem):
    return elem[1] * -1

def orderGeneration(fitnessGene):
    return fitnessGene.sort(key=takeSecond)

def fitness(gene):
    return fb.start(gene)

def mixGene(gene1,gene2):
    options = [0,1]
    weights = [0.9,0.10]
    for i,detail in enumerate(gene1):
        if(random.choices(options,weights ) == 0):
            detail = gene2[i]
        #else its stay as it is
    return gene1

def mixGeneration(fitnessGene):
    generation = []
    for i in range(int(POPULATION/4) - 1):
        generation.append(mixGene(fitnessGene[0][0]
                                  ,fitnessGene[1][0]))
        generation.append(mixGene(fitnessGene[0][0]
                                  ,fitnessGene[1][0]))
        generation.append(mixGene(fitnessGene[0][0]
                                  ,fitnessGene[1][0]))
        generation.append(mixGene(fitnessGene[1][0]
                                  ,fitnessGene[2][0]))
    generation.append(fitnessGene[0][0])
    generation.append(fitnessGene[0][0])
    generation.append(fitnessGene[1][0])
    generation.append(fitnessGene[2][0])
    return generation
'''''''''
def mutantGeneration(generation):
    newGeneration = []
    options = [0,1]
    weight = [1,0]
    for index,gene in enumerate(generation):
        newGeneration.append([])
        if(random.choices(options,weight) == 1):
            for genom in gene:
                if (random.choices(options, weight) == 1):
                    newGeneration[i].append((genom + 1) % 2)
                else:
                    newGeneration[i].append(genom)
        else:
            newGeneration[i].append(gene)
    return newGeneration
'''''''''''
#to get row is height so curr - MIN_HEIGHT / SPLIT
#to get coulmn is horizontal so curr - MIN_HORIZONTAL / SPLIT
 #heigh change 1 by 20
#height 170
#hor 110
#gene 285
#((self.birdY - self.offset) / 20 * 20 ) + self.wallx / 20]
# 170 /20 * 20 + 110 /20 =
if __name__ == "__main__":
    generation = createGeneration()
    counter = 0
    while(True):
        print("----------------------------generation number:", counter,"---------------------------------")
        counter += 1
        fitnessGene = fitnessGeneration(generation)

        generationAVG = 0
        for i in range(POPULATION):
            if(i < 4):
                print("the",i,"th place socre is",fitnessGene[i][1])
            generationAVG += fitnessGene[i][1]
        print("generation average socre is",generationAVG/POPULATION)

        #for gene in fitnessGene:
            #print("gene fitness is:", gene[1])
        generation = mixGeneration(fitnessGene)
        newGeneration = mutantGeneration(generation)
        if(generation == newGeneration):
            print("equals")
        print("")




