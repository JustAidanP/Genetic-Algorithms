from random import randint
import time, math
from Population import Population, Member
class GeneticAlgorithm:
    #------Initialiser-------
    #Arguments: -The population size    -Int
    #           -The gene count per DNA -Int
    #           -The gene mutation rate -Float
    #           -The gene addition rate -Float
    def __init__(self, _populationSize, _geneCount, _mutationRate, _additionRate):
        self.populationSize = _populationSize
        self.geneCount = _geneCount
        self.mutationRate = _mutationRate
        self.additionRate= _additionRate
        #Creates the population object
        self.population = Population()
        #Stores the generation count
        self.generationNumber = 0
        #Creates the bestMember and mating pool containers
        self.bestMeber = None
        self.matingPool = []

    #-------Procedures/Functions------
    def generatePopulation(self): pass
    #Calculates the fitness
    #Arguments: -The member of the population   -Member
    #Returns:   -The fitness                    -Float
    def calculateFitness(self, _member): pass
    #Executes the generation
    def evaluateGeneration(self):
        #Stores the best member of the population
        self.bestMeber = self.population.getMembers()[0]
        #Stores the mating pool for natural selection
        self.matingPool = []
        #Loops through every member of the population and calculates the fitness for it
        for member in self.population.getMembers():
            self.calculateFitness(member)
            #Adds a member to the mating list, ensuring that the final best member isn't contained, ensures that every member has at least one entry
            if member.getFitness() > self.bestMeber.getFitness(): 
                #Adds the last best member to the mating pool 
                self.matingPool += [self.bestMeber for i in range(int(self.bestMeber.getFitness() // 1) ** 2 + 2 if self.bestMeber.getFitness() > 0 else 1)]
                self.bestMeber = member
            else:
                #Adds the member to the mating pool
                self.matingPool += [member for i in range(int(member.getFitness() // 1) ** 2 + 2 if member.getFitness() > 0 else 1)]
            
    #Performs natural selection on the generation
    def performNaturalSelection(self):
        self.population.empty()
        #Fills the population
        for i in range(self.populationSize):
            #Creates a new member, by fusing the best member with a random member from the mating pool
            newMember = Member(self.bestMeber.getDNA().fusion(otherDNA=self.matingPool[randint(0, len(self.matingPool) - 1)].getDNA(), mutationRate=self.mutationRate))
            self.population.addMember(newMember)

    #Runs the GA once
    def runOnce(self):
        self.generationNumber += 1
        #Evaluates the generation
        self.evaluateGeneration()
        #Performs natural selection
        self.performNaturalSelection()

    #Runs the GA until either the defined number of generations have ran or until the time limit has ran out
    #Arguments: The number of generations to run    -Int    -Default None
    #           The time to run for                 -Float  -Default None
    def runUntil(self): pass
    #Runs the GA forever, outputting the best member every so often
    #Arguments: -The output path            -String
    #           -Generations until output   -Int
    def run(self, bmOutputPath, gensUntilOutput):
        startTime = time.time()
        #Constantly runs the GA
        while True:
            print("------Generation %s------"%self.generationNumber)
            self.runOnce()
            #Checks to see if the best member should be output
            if self.generationNumber % gensUntilOutput == 0:
                print("Best Member Saved")
                file = open(bmOutputPath + ".json", 'w')
                #Creates the json file output
                jsonOut = "{\"member\":%s, \"time\":%s, \"generation\":%s}"%(self.bestMeber.dump(), time.time() - startTime, self.generationNumber)
                file.write(jsonOut)
                file.close()

            #Writes a history of the best member when the generation is a power of two
            if math.log2(self.generationNumber).is_integer():
                file = open(bmOutputPath + "_Gen%s"%self.generationNumber + ".json", "w")
                #Creates the json output file
                jsonOut = "{\"member\":%s, \"time\":%s, \"generation\":%s}"%(self.bestMeber.dump(), time.time() - startTime, self.generationNumber)
                file.write(jsonOut)
                file.close()
    
    #Stops the running of the GA
    def stop(self): pass