from random import randint
import time, math
from Population import Population, Member
class GeneticAlgorithm:
    #------Initialiser-------
    #Arguments: -The population size    -Int
    #           -The gene count per DNA -Int
    #           -The gene mutation rate -Float
    #           -The gene addition rate -Float
    #           -Inverse fitness flag   -Bool
    def __init__(self, _populationSize, _geneCount, _mutationRate, _additionRate, _inverseFitness=False):
        self.populationSize = _populationSize
        self.geneCount = _geneCount
        self.mutationRate = _mutationRate
        self.additionRate= _additionRate
        #Creates the population object
        self.population = Population()
        #Stores the generation count
        self.generationNumber = 0
        #Creates the bestMember and mating pool containers
        self.bestMember = None
        self.matingPool = []

        #Determines whether the fitness is an inverse relationship (if the best fitness should be smaller than the worst)
        self.inverseFitness = _inverseFitness

    #-------Procedures/Functions------
    def generatePopulation(self): pass
    #Calculates the fitness
    #Arguments: -The member of the population   -Member
    #Returns:   -The fitness                    -Float
    def calculateFitness(self, _member): pass
    #Executes the generation
    def evaluateGeneration(self):
        #Stores the best member of the population
        self.bestMember = self.population.getMembers()[0]
        #Stores the mating pool for natural selection
        self.matingPool = []
        #Stores the baseline and zero fitness levels, defaults them to the first member fitess
        self.calculateFitness(self.population.members[0])
        blFitness = self.population.members[0].getFitness() #A member with this fitness will get the most entrances
        zFitness = self.population.members[0].getFitness()  #A member wit hthis fitness will get the least entrances
        #Loops through every member of the population and calculates the fitness for it
        for i in range(1, len(self.population.getMembers())):
            self.calculateFitness(self.population.members[i])
            fitness = self.population.members[i].getFitness()
            #Checks if it is the best or worst fitness
            if self.inverseFitness:
                if fitness < blFitness: 
                    #Stores the member with the best fitness
                    self.bestMember = self.population.members[i]
                    blFitness = fitness
                elif fitness > zFitness: zFitness = fitness
            else:
                if fitness > blFitness: 
                    #Stores the member with the best fitness
                    self.bestMember = self.population.members[i]
                    blFitness = fitness
                elif fitness < zFitness: zFitness = fitness
        #Calculates the gradient for the entrance calculation, this gradient efectively normalises the fitness between the best and worst
        gradient = 9/(blFitness - zFitness)
        #Loops through every member, adding it to the matingPool based on its fitness compared to a linear scale between best and worst fitness
        for member in self.population.getMembers():
            #Exludes the best member
            if blFitness == member.getFitness(): continue
            #Performs the entrance calculation, E = gradient * (fitness - bsFitness)
            entrance = (gradient * (member.getFitness() - blFitness) + 1) ** 2
            self.matingPool += [member for i in range(int(entrance // 1))]
            
    #Performs natural selection on the generation
    def performNaturalSelection(self):
        self.population.empty()
        #Fills the population
        for i in range(self.populationSize):
            #Creates a new member, by fusing the best member with a random member from the mating pool
            newMember = Member(self.bestMember.getDNA().fusion(otherDNA=self.matingPool[randint(0, len(self.matingPool) - 1)].getDNA(), mutationRate=self.mutationRate))
            self.population.addMember(newMember)

    #Runs the GA once
    def runOnce(self):
        self.generationNumber += 1
        #Evaluates the generation
        self.evaluateGeneration()
        #Performs natural selection
        self.performNaturalSelection()

    #Runs the GA forever, outputting the best member every so often
    #Arguments: -The output path                    -String
    #           -Generations until output           -Int
    #           -The callback method to call on gen -Void(float TimeElapsed)
    def run(self, callback):
        startTime = time.time()
        #Constantly runs the GA
        while True:
            self.runOnce()
            #Calls the callback if it exists
            #Passes in the time elapsed
            if callable(callback): callback(self, time.time() - startTime)
    
    #Stops the running of the GA
    def stop(self): pass