 import random, copy, time, math, numpy
from PIL import Image, ImageDraw, ImageChops
class GeneticAlgorithm:
    #The chance of a mutation to happen on a weight(gene)
    mutationRate = 0.01
    #The chance that a new gene will be added to DNA
    geneAdditionRate = 0
    #Determines the initial size of the DNA
    DNAGeneCount = 512
    #The number of members per generation
    populationSize = 30
    #A container for each generation of members
    #Two Dimensional, The DNA and its Fitness
    population = []
    curGeneration = 1
    #Each value references a member from the population
    #The number of references depends on the fitness the member scored
    matingPoolReference = [[]]
    #Holds the best reference to DNA of the generation
    bestIndexOfGen = 0
    #Holds the second best reference to DNA of the generation
    secondBestIndexOfGen = 0
    totalFitnessOfGen = 0
    bestOverallFitness = 0
    #Updated constantly to allow movement of the most effecient DNA
    bestDNA = []

    def __init__(self):
        print("Start")
        timeForCheck = time.time()
        timeElapsed = time.time()
        self.initialRun()
        while True:
            self.run()
            self.curGeneration += 1

            print("Generation: ", self.curGeneration)
            print("Time Elapsed: ", str(time.time() - timeElapsed))
            print("------New Generation------")
            #Checks if 10 minutes have passed, if so it shows the image
            #600 is 10 minutes
            if (time.time() - timeForCheck) / 600 > 1:
                timeForCheck = time.time()

                #Creates the image
                memberImage = Image.new("RGBA", (3840, 2160))
                #Creates a canvas for the drawing in which the memberImage is drawn over
                drawingCanvas = ImageDraw.Draw(im=memberImage)
                #Draws rectangles on the image based on the DNA of the member
                for gene in self.population[self.bestIndexOfGen][0].genes:
                    xyCoords = []
                    for axis in range(len(gene.getXYCoords())):
                        xyCoords.append(gene.getXYCoords()[axis] * ( (3840 / canvasSize[0]) if axis % 2 == 0 else (2160 / canvasSize[1]) ))
                    # xyCoords = (xyCoords[0] * 3840 / canvasSize[0], xyCoords[1] * 2160 / canvasSize[1])
                    #Draws on the image
                    drawingCanvas.polygon(xy=xyCoords, fill=gene.getColour())
                
                memberImage.save("/Users/aidanprice/Desktop/Machine Learning/GeneticAlgorithms/Cam_PortraitRun/" + str(self.curGeneration) + ".png")
                # self.createImage(self.population[self.bestIndexOfGen][0]).save("/Users/aidanprice/Desktop/Machine Learning/GeneticAlgorithms/BeachIrelandRun/" + str(self.curGeneration) + "_smaller.png")

    #Sets up the initial DNA items and then initiates a run
    def initialRun(self):
        #Generates the inital population
        #First item is the DNA, second is the initial fitness
        for i in range(self.populationSize):
            self.population.append([DNA(), 0])

    def naturalSelection(self):
        #Updates the best overall fitness
        if self.population[self.bestIndexOfGen][1] > self.bestOverallFitness:
            self.bestOverallFitness = self.population[self.bestIndexOfGen][1]
        #Creates a new population of size populationSize
        newPopulation = [self.population[self.bestIndexOfGen]]
        #The gene pool will ensure that there is variation in the next generation
        genePool = []
        print("Best Overall Fitness: ", self.bestOverallFitness / 2)
        print("Best Fitness: ", self.population[self.bestIndexOfGen][1] / 2)
        print("Total Fitness: ", len(self.matingPoolReference[0]))
        #Fills the new population with new members, including the best of the last population
        for populationIter in range(self.populationSize - 1):
            #Backups up matingPoolReference
            matingPoolReferenceBackup = copy.copy(self.matingPoolReference[0])
            #Creates a new population
            #Gets the DNA of the best DNA
            parent1 = self.population[self.bestIndexOfGen][0]
            #Removes all references to parent1 from the backup mating pool
            matingPoolReferenceBackup = [reference for reference in matingPoolReferenceBackup if reference != self.bestIndexOfGen]
            #Randomly selects a reference to a 2nd DNA item
            parent2Ref = matingPoolReferenceBackup[random.randint(0, len(matingPoolReferenceBackup) - 1)]
            #Gets the DNA of the parent2Ref
            parent2 = self.population[parent2Ref][0]
            #Creates a new DNA item
            newDNA = DNA(parent1.fusion(parent2.genes))
            #First element is the neural network, the second is the fitness
            newPopulation.append([newDNA, 0])

        #Inserts the best DNA of the last population into the new population
        newPopulation.append(self.population[self.bestIndexOfGen])
        #Assigns the newPopulation
        self.population = newPopulation
        #Resets the bestIndexOfGen and secondBestIndexOfGen
        self.bestIndexOfGen = 0
        # #Adds a new gene to every DNA randomly
        # if random.uniform(0, 1) < self.geneAdditionRate:
        #     self.DNAGeneCount += 1
        #     self.addGene()
    #Runs a generation
    def run(self):
        #Resets the matingPoolReference
        self.matingPoolReference = [[]]
        #Runs through every member of the population and calculates the fitness
        for populationMember in range(len(self.population)):
            #Recieves the population item containing the DNA and the fitness
            populationItem = self.population[populationMember]

            fitness = 0
            #Calculates the fitness of the DNA
            fitness = self.calculateFitness(populationItem[0])
            roundedFitness = 0
            #Makes sure that only the DNA that meets the threshold are used
            if fitness >= 0:
                #Rounds the fitness value
                roundedFitness = int(round(fitness, 0))
                #Increases the chance of a better fitness being picked in naturalSelection
                roundedFitness = roundedFitness ** 2
                #Adds 1 to the roundedFitness to ensure that there is always a mating pool
                roundedFitness += 1
            #Adds references to the DNA to matingPoolReferences, the number of references depends on the fitness
            self.matingPoolReference[0] += ([populationMember] * roundedFitness)
            #Detects the best DNA of the run
            if fitness > self.population[self.bestIndexOfGen][1]:
                self.bestIndexOfGen = populationMember
            #Updates the fitness of the population member
            populationItem[1] = fitness

        #Makes sure that there are at least two unique members in matingPoolReference
        if len(self.matingPoolReference[0]) < 2:
            #Empties the matingPoolReference
            self.matingPoolReference[0] = []
            #Adds the best member into the matingPoolReference
            self.matingPoolReference[0].append(self.bestIndexOfGen)
            #A container for the reference to be added to the matingPoolReference
            chosenReference = self.bestIndexOfGen
            #Randomly chosses a second reference for the matingPoolReference, making sure that it isn't the same as the bestIndexOfGen
            while chosenReference == self.bestIndexOfGen: chosenReference = random.randint(0, len(self.population)-1)
            self.matingPoolReference[0].append(chosenReference)
        self.naturalSelection()

    #Creates a new Image
    def createImage(self, member):
        #Creates the image
        memberImage = Image.new("RGBA", canvasSize)
        #Creates a canvas for the drawing in which the memberImage is drawn over
        drawingCanvas = ImageDraw.Draw(im=memberImage)
        #Draws rectangles on the image based on the DNA of the member
        for gene in member.genes:
            #Draws on the image
            drawingCanvas.polygon(xy=gene.getXYCoords(), fill=gene.getColour())
        #Returns the created image
        return memberImage

    #Calculates the fitness of the member
    def calculateFitness(self, member):
        memberImage = self.createImage(member)
        #Calculates the difference of the target image and the memberImage
        imageDifference = ImageChops.difference(targetImage, memberImage)
        #Calculates the totalDifference
        totalDifference = numpy.array(imageDifference).sum()
        #Calculates the fitness based off of a linear function
        fitness = (10 / -fitnessThreshold) * totalDifference + 10
        #Returns the fitness
        return fitness

    #Adds a new gene to every member
    def addGene(self):
        #Iterates through every member
        for member in self.population:
            #Creates a new gene in the DNA
            member[0].addGene()

#Holds the target image
global targetImage
# targetImage = Image.open("/Users/aidanprice/Desktop/Other/ReservoirResized.JPG")
targetImage = Image.open("/Users/aidanprice/Desktop/Machine Learning/GeneticAlgorithms/Cam_Portrait.JPG")
#Converts the image to RGBA
targetImage = targetImage.convert("RGBA")
#Holds the canvas size for use with gene randomisation
global canvasSize
canvasSize = targetImage.size
#Holds the threshold for the difference between the images before the fitness is considered
#The last value defines how far each pixel can be away from the original image
#The '4' accounts for the RGBA channels
global fitnessThreshold
fitnessThreshold = (canvasSize[0] * canvasSize[1]) * 4 * 75

GeneticAlgorithm()
