# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 19:44:39 2018

@author: Fabian
"""

import random
import numpy as np
import tensorflow as tf
import tflearn

from bokeh.plotting import figure 
from bokeh.io import output_notebook, show

class aiLife():
    
    def __init__(self ,populationSize = 10):
        #stores player ais
        self.population = []
        self.bestFitnessOfGeneration = [0]
        
        #store properties
        self.runsOfAi = 0
        self.currentLivingAI = 0
        self.generation = 0
        self.populationSize = 50
        self.weightsSurvivors = []
        self.numberSurvivorsFromGeneration = 5
        self.numberLuckySurvivorsFromGeneration = 1
        self.highestFitness = 0
        
    def generateFirstPopulation(self):
        for i in range(self.populationSize):
            self.population.append(AI())
            print("AI: " + str(i) + " created")
        print("newGeneration: " + str(self.generation))
            
    def getNextAI(self, fitness):
        if self.runsOfAi == 1:
            
            if self.population[self.currentLivingAI].fitness < fitness:
                self.population[self.currentLivingAI].fitness = fitness
            
            self.runsOfAi += 1
            
        if self.runsOfAi == 2:
            self.currentLivingAI += 1
            self.runsOfAi = 0

            if self.currentLivingAI >= self.populationSize:
                self.createNewGeneration(self.selectFromPopulation(self.numberSurvivorsFromGeneration, self.numberLuckySurvivorsFromGeneration))
                self.generation += 1
                print("newGeneration: " + str(self.generation))
                print("--------------------------------------------")
                if self.generation % 20 == 0:
                    x = range(0,len(self.bestFitnessOfGeneration))
                    y = self.bestFitnessOfGeneration
                    
                    p = figure(width=500, height=500)
                    p.circle(x,y, size=7, color="firebrick", alpha=0.5)
                    show(p)
        
        else:
            self.population[self.currentLivingAI].fitness = fitness
            
            self.runsOfAi += 1
        
        return self.population[self.currentLivingAI]
        
    def selectFromPopulation(self, numberChoosen, numberLuckySurvivors):
        nextGeneration = []
        #sort the population by fitness
        self.population.sort(key=lambda AI: AI.fitness, reverse = True)
        self.bestFitnessOfGeneration.append(self.population[0].fitness)
        #pick the best
        
        #save best one
        if self.population[0].fitness >= self.highestFitness:
            self.highestFitness = self.population[0].fitness
            self.population[0].model.save("ai/bestLast.tfl")
        
        for i in range(numberChoosen):
            print(self.population[i].fitness)
            nextGeneration.append(self.population[i])
        
        #pick lucky ones
        for _ in range(numberLuckySurvivors):
            nextGeneration.append(random.choice(self.population))
        
        #generate the new generation
        return nextGeneration
    
    def createNewGeneration(self, parents = []):
        self.currentLivingAI = 0
        parentChromosomes = []
        
        totals = []
        running_total = 0
        
        for i in range(len(parents)):
            parentChromosomes.append((parents[i].chromosomes_h1, parents[i].chromosomes_n, parents[i].chromosomes_h1_b, parents[i].chromosomes_n_b))#, parents[i].chromosomes_h1_b, parents[i].chromosomes_h2_b, parents[i].chromosomes_h3_b, parents[i].chromosomes_n_b))
 
            running_total += parents[i].fitness
            totals.append(running_total)

        #cross over
        for i in range(self.populationSize):
            male = random.choice(parentChromosomes)
            female = random.choice(parentChromosomes)
            
            self.crossOverPoint(male, female, 0.05, i)

    def crossOverUniform(self, male_chromosomes, female_chromosomes, mutation, index):        
        
        for i in range(len(male_chromosomes)):         
            chromosomes = []
            for ii in range(len(male_chromosomes[i])):
                if random.random() <= mutation:
                    chromosomes.append(random.random()*10-5)
                else:
                    chromosomes.append(random.choice([male_chromosomes[i][ii],female_chromosomes[i][ii]]))

            if i == 0:
                self.population[index].chromosomes_h1 = chromosomes
            elif i == 1:
                self.population[index].chromosomes_n = chromosomes
            elif i == 2:
                self.population[index].chromosomes_h1_b = chromosomes
            else:
                self.population[index].chromosomes_n_b = chromosomes

            
            self.population[index].referChromosomesToModel()
                    
    def crossOverPoint(self, male_chromosomes, female_chromosomes, mutation, index):        
        
        for i in range(len(male_chromosomes)):
            chromosomes = []
            splitPoint = random.randint(0,len(male_chromosomes))
            for ii in range(len(male_chromosomes[i])):
                if random.random() <= mutation:
                    chromosomes.append(random.random()*5-2.5)
                else:
                    if i < splitPoint:
                        chromosomes.append(male_chromosomes[i][ii])
                    else:
                        chromosomes.append(female_chromosomes[i][ii])
         
            if i == 0:
                self.population[index].chromosomes_h1 = chromosomes
            elif i == 1:
                self.population[index].chromosomes_n = chromosomes
            elif i == 2:
                self.population[index].chromosomes_h1_b = chromosomes
            else:
                self.population[index].chromosomes_n_b = chromosomes

        self.population[index].referChromosomesToModel()

class AI():
    
    def __init__(self, loadAIPath = None):
        # Let's create a graph:
        self.g = tf.Graph()
        
        with self.g.as_default():
          n = tflearn.input_data(shape=[None,2])
          self.h1 = tflearn.fully_connected(n, 8)
          #self.h2 = tflearn.fully_connected(self.h1, 16)
          #self.h3 = tflearn.fully_connected(self.h2, 8)
          self.n = tflearn.fully_connected(self.h1, 2, activation='softmax')
          n = tflearn.regression(self.n)
          self.model = tflearn.DNN(n)
          
          if loadAIPath != None:
              self.model.load(loadAIPath)

          self.chromosomes_h1 = self.model.get_weights(self.h1.W).reshape(-1)
          self.chromosomes_h1_b = self.model.get_weights(self.h1.b).reshape(-1)
          #self.chromosomes_h2 = self.model.get_weights(self.h2.W).reshape(-1)
          #self.chromosomes_h3 = self.model.get_weights(self.h3.W).reshape(-1)
          self.chromosomes_n = self.model.get_weights(self.n.W).reshape(-1)
          self.chromosomes_n_b = self.model.get_weights(self.n.b).reshape(-1)

        self.fitness = 0
        
    def referChromosomesToModel(self):
        self.model.set_weights(self.h1.W, np.array(self.chromosomes_h1).reshape(2,8))
        self.model.set_weights(self.h1.b, np.array(self.chromosomes_h1_b))

        #self.model.set_weights(self.h2.W, np.array(self.chromosomes_h2).reshape(8,16))
        #self.model.set_weights(self.h3.W, np.array(self.chromosomes_h3).reshape(16,8))
        
        self.model.set_weights(self.n.W,  np.array(self.chromosomes_n).reshape(8,2))        
        self.model.set_weights(self.n.b,  np.array(self.chromosomes_n_b))
        
    def getOutput(self, input = (0,0,0,0)):
        input = np.array(input).reshape((-1,2))
        return self.model.predict(input)