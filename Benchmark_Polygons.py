#------Generic Imports------
from PIL import Image, ImageDraw, ImageChops
import sys, math, time

#------Specific Imports------
from Vector import Vector
from GAPolygons import GAPolygons


if __name__=="__main__":
    #Creates the genetic algorithm
    ga = GAPolygons(25, 512, 0.025, 0, True)
    #Sets the polygon ga specific data
    ga.setCanvasSize(Vector(256, 256))
    ga.setFitnessThreshold(256 * 256 * 4 * 75)

    #Opens the target image
    targetImage = Image.open("PolygonImages/Benchmark.jpeg")
    #Converts the image to RGBA
    targetImage = targetImage.convert("RGB")
    targetImage = targetImage.resize((256, 256))
    ga.setTargetImage(targetImage)

    #Genereates the population
    ga.generatePopulation()
    #Benchmarks the run routine
    startTime = time.time()
    avg = 0
    for i in range(400):
        startTime = time.time()
        ga.runOnce()
        avg += time.time() - startTime
    print(avg / 400)