#------Generic Imports------
from PIL import Image, ImageDraw, ImageChops
import sys, math
#------Specific Imports------
from Vector import Vector
from GAPolygons import GAPolygons

#Defines the callback function
#Arguments: -The ga             -GeneticAlgorithm
#           -The elapsedTime    -Float
def generationCallback(ga, timeElapsed):
    print("------Generation %s, Time %s, Avg %s------"%(ga.generationNumber, round(timeElapsed, 3), round(timeElapsed / ga.generationNumber, 3)))
    #Goes onto the next frame every 1024 generations
    if ga.generationNumber % 2048 != 0: return
    print("Switching Frame")
    #Saves the best member
    if ga.generationNumber > 3000:
        file = open("/Users/aidanprice/Desktop/Coding/GeneticAlgorithms/PolygonImages/MidSceneChange/Json/bmWalesDam.json", 'w')
    else:
        file = open("/Users/aidanprice/Desktop/Coding/GeneticAlgorithms/PolygonImages/MidSceneChange/Json/bmSun.json", 'w')
    #Creates the json file output
    jsonOut = "{\"member\":%s, \"time\":%s, \"generation\":%s}"%(ga.bestMeber.dump(), timeElapsed, ga.generationNumber)
    file.write(jsonOut)
    file.close()

    #Sets the new frame
    targetImage = Image.open("/Users/aidanprice/Desktop/Coding/GeneticAlgorithms/PolygonImages/MidSceneChange/WalesDam.jpeg")
    #Converts the image to RGBA
    targetImage = targetImage.convert("RGB")
    targetImage = targetImage.resize((256, 256))
    #Sets the target to the new frame
    ga.setTargetImage(targetImage)


if __name__=="__main__":
    #Creates the genetic algorithm
    ga = GAPolygons(24, 512, 0.025, 0, True)
    #Sets the polygon ga specific data
    ga.setCanvasSize(Vector(256, 256))
    ga.setFitnessThreshold(256 * 256 * 4 * 75)

    #Opens the first image
    targetImage = Image.open("/Users/aidanprice/Desktop/Coding/GeneticAlgorithms/PolygonImages/MidSceneChange/Sun.jpg")
    #Converts the image to RGBA
    targetImage = targetImage.convert("RGB")
    targetImage = targetImage.resize((256, 256))

    ga.setTargetImage(targetImage)

    ga.generatePopulation()
    ga.run(generationCallback)