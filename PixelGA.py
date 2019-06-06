import numpy as np
import random
import copy
import math
from sys import exit
import time
from tkinter import *


random.seed(20)


def print_pop(population):
    for i in population:
        print(i)


def create_starting_population(popsize):
    population = []
    for index in range(popsize):
        myrgbvalues = []
        for rgb in range(3):
            myrgbvalues.append(random.randint(0, 255))
        population.append(myrgbvalues)
    return population


def fitness_population(population, targetchromosome):
    fitnesslist = []
    for i in range(0, len(population)):
        fitnesslist += [fitness(population[i], targetchromosome)]
    return fitnesslist


def fitness(chromosome, targetchromosome):
    fitness = 0
    for i in range(len(chromosome)):
         fitness += (255 - (abs(targetchromosome[i] - chromosome[i])))

    return fitness


def get_partner_index(population, auxpopulation, targetchromosome):
    auxbest, auxbestfitness = best_fitness_pop(auxpopulation, targetchromosome)
    while True:
        indexpop = random.randint(0, auxpopulation.__len__()-1)
        fitnessp = fitness(auxpopulation[indexpop], targetchromosome)
        rfitness = random.randint(0, auxbestfitness)
        if rfitness <= fitnessp:
            indexpartner = population.index(auxpopulation[indexpop])
            del auxpopulation[indexpop]

            return indexpartner, auxpopulation


def crossover(a, b):
    new_1 = []
    new_2 = []
    for i in range(a.__len__()):
        randomprof = random.random()
        if randomprof <= 0.5:
            new_1.append(a[i])
            new_2.append(b[i])
        else:
            new_1.append(b[i])
            new_2.append(a[i])

    return new_1, new_2


def mutate(population, mutationrate):
    for chromosome in population:
        if random.random() <= mutationrate:
            foundgene = 1
            while foundgene == 1:
                random_gene = random.randint(0, 2)
                mutateaddnumber = random.randint(-2, 2)
                while mutateaddnumber == 0:
                    mutateaddnumber = random.randint(-2, 2)
                if chromosome[random_gene] + mutateaddnumber <= 255:
                    chromosome[random_gene] += mutateaddnumber
                    foundgene = 0
    return population


def best_fitness_pop(population, targetchromosome):
    fitnesslist = fitness_population(population, targetchromosome)
    #print(fitnesslist)
    best = population[np.argmax(fitnesslist)]
    bestfitness = fitness(best, targetchromosome)
    #print(bestfitness)

    return best, bestfitness


def get_best_chromosomes(population, newpopulation, numberbest, targetchromosome):

    auxpopulation = population.copy()
    for i in range(numberbest):
        fitnesslist = fitness_population(auxpopulation, targetchromosome)
        newpopulation.append(auxpopulation[np.argmax(fitnesslist)])
        del auxpopulation[np.argmax(fitnesslist)]

    return newpopulation


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


def mouseclick(event, mypixel):
    global gennumber
    global population
    global targetchromosome
    global lastbestfitness
    global numberofcouples
    global populationsize
    global mutationrate

    newpopulation = []
    best, bestfitness = best_fitness_pop(population, targetchromosome)

    if gennumber >= 0:
        print()
        print("Generation # " + str(gennumber))
        print("Best Fitness Value --> " + str(bestfitness))
        print("Best Chromosome    --> " + str(best))

    auxpopulation = copy.deepcopy(population)
    for j in range(numberofcouples):
        partnerindex1, auxpopulation = get_partner_index(population, auxpopulation, targetchromosome)
        partnerindex2, auxpopulation = get_partner_index(population, auxpopulation, targetchromosome)
        new_1, new_2 = crossover(population[partnerindex1], population[partnerindex2])
        newpopulation.append(new_1)
        newpopulation.append(new_2)

    newpopulation = get_best_chromosomes(population, newpopulation, populationsize - numberofcouples * 2, targetchromosome)

    population = mutate(newpopulation, mutationrate)

    lastbestfitness = bestfitness
    gennumber += 1
    counter = 0

    for i in range(len(mypixel)):
        canvas.itemconfig(mypixel[i], fill=_from_rgb((population[i][0], population[i][1], population[i][2])))
        counter = counter + 1
    if bestfitness == 765:
        targetchromosome = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        population = create_starting_population(populationsize)
        gennumber = 0
        print('FINISH!!!!!')
        #exit()

def main():
    global population
    global targetchromosome
    global lastbestfitness
    global gennumber
    global numberofcouples
    global populationsize
    global mutationrate

    # PARAMETERS
    gennumber = 0
    numberofgen = 1000
    selectionsizerate = 0.5
    mutationrate = 0.5

    #SIZE
    sizenumber = 10
    populationsize = sizenumber * sizenumber
    numberofcouples = int(populationsize*selectionsizerate/2)

    # TARGET
    targetchromosome = [120, 12, 120]

    # ----- START -----
    population = create_starting_population(populationsize)
    #print(population)
    fitnesslist = fitness_population(population, targetchromosome)
    #print(fitnesslist)

    lastbestfitness = -1

    root = Tk()
    global canvas
    canvas = Canvas(root, width=400, height=400)

    mypixel = []
    counter = 0
    for cl in range(sizenumber):
        for rw in range(sizenumber):
            mypixel.append(canvas.create_rectangle(rw * 400 / sizenumber, cl * 400 / sizenumber, (rw + 1) * 400 / sizenumber, (cl + 1) * 400 / sizenumber, outline=_from_rgb((255, 255, 255)), fill=_from_rgb((population[counter][0], population[counter][1], population[counter][2]))))
            counter = counter + 1
    canvas.pack(fill=BOTH, expand=1)
    canvas.bind("<Button-1>", lambda eff: mouseclick(eff, mypixel))

    canvas.pack()
    root.mainloop()


    '''for i in range(numberofgen):
        newpopulation = []
        best, bestfitness = best_fitness_pop(population, targetchromosome)

        if bestfitness > lastbestfitness:
            print()
            print("Generation # " + str(i))
            print("Best Fitness Value --> " + str(bestfitness))
            print("Best Chromosome    --> " + str(best))
            if bestfitness == 765:
                return 0

        auxpopulation = copy.deepcopy(population)
        for j in range(numberofcouples):
            partnerindex1 , auxpopulation = get_partner_index(population, auxpopulation, targetchromosome)
            partnerindex2 , auxpopulation = get_partner_index(population, auxpopulation, targetchromosome)
            new_1, new_2 = crossover(population[partnerindex1], population[partnerindex2])
            newpopulation.append(new_1)
            newpopulation.append(new_2)

        newpopulation = get_best_chromosomes(population, newpopulation, populationsize-numberofcouples*2, targetchromosome)

        population = mutate(newpopulation, mutationrate)

        lastbestfitness = bestfitness'''

main()
