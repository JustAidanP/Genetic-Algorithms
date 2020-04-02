from PIL import Image, ImageDraw, ImageChops
import numpy, sys

from copy import deepcopy
from GenePolygon import GenePolygon
from dna import DNA
from Population import Member, Population
from GeneticAlgorithm import GeneticAlgorithm
from Vector import Vector

#------Classes------
class GAPolygons(GeneticAlgorithm):
    #------Getters/Setters------
    #Sets the canvas size
    #Arguments: -The canvas size    -Vector
    def setCanvasSize(self, _canvasSize): self.canvasSize = _canvasSize
    #Sets the target image
    #Arguments: -The target image   -Image
    def setTargetImage(self, _targetImage): self.targetImage = _targetImage
    #Sets the fitness threshold
    #Arguments: -The threshold      -Float
    def setFitnessThreshold(self, _fitnessThreshold): self.fitnessThreshold = _fitnessThreshold

    #-------Procedures/Functions------
    #Generates the population
    def generatePopulation(self):
        for i in range(self.populationSize):
            #Creates a new dna object
            dna = deepcopy(DNA())
            gene = GenePolygon(_canvasSize=self.canvasSize)
            dna.createGenes(gene=gene, n=self.geneCount)
            #Creates a new member with the dna
            member = Member(_dna=dna)
            #Adds the member to the population
            self.population.addMember(member)


    #Creates an image for a member of the population
    #Arguments: -The member -Member
    def createImage(self, _member):
        #Creates the image
        memberImage = Image.new("RGB", (self.canvasSize.x, self.canvasSize.y), (255, 255, 255))
        #Creates a canvas for the image
        drawingCanvas = ImageDraw.Draw(memberImage, "RGBA")
        #Draws polygons on the image based on the DNA of the member
        for gene in _member.getDNA().getGenes():
            #Draws on the image
            drawingCanvas.polygon(xy=gene.getCoordsTuple(), fill=(gene.getColour().x, gene.getColour().y, gene.getColour().z, gene.getColour().w))
        del drawingCanvas
        #Returns the created image
        return memberImage

    #Calculates the fitness for the member of the population
    #Arguments: -The member of the population   -Member
    def calculateFitness(self, _member):
        memberImage = self.createImage(_member)
        #Calculates the difference of the target image and the memberImage
        imageDifference = ImageChops.difference(self.targetImage, memberImage)
        #Calculates the totalDifference between the two images
        totalDifference = abs(numpy.array(imageDifference).sum())
        #Assigns the fitness to the population member
        _member.fitness = float(totalDifference)