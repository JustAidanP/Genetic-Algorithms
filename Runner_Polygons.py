#------Generic Imports------
from PIL import Image, ImageDraw, ImageChops
import sys, math, time

#------Specific Imports------
from Vector import Vector
from GAPolygons import GAPolygons

#Defines the callback function
#Arguments: -The ga             -GeneticAlgorithm
#           -The elapsedTime    -Float
def generationCallback(ga, timeElapsed):
    print("------Generation %s, Time %s, Avg %s------"%(ga.generationNumber, round(timeElapsed, 3), round(timeElapsed / ga.generationNumber, 3)))
    #Checks to see if the best member should be output
    if ga.generationNumber % step == 0:
        print("Best Member Saved")
        file = open(outputFile + ".json", 'w')
        #Creates the json file output
        jsonOut = "{\"member\":%s, \"time\":%s, \"generation\":%s, \"avgTime\":%s}"%(ga.bestMember.dump(), timeElapsed, ga.generationNumber, round(timeElapsed / ga.generationNumber, 3))
        file.write(jsonOut)
        file.close()

    #Writes a history of the best member when the generation is a power of two
    if math.log2(ga.generationNumber).is_integer():
        file = open(outputFile + "_Gen%s"%ga.generationNumber + ".json", "w")
        #Creates the json output file
        jsonOut = "{\"member\":%s, \"time\":%s, \"generation\":%s, \"avgTime\":%s}"%(ga.bestMember.dump(), timeElapsed, ga.generationNumber, round(timeElapsed / ga.generationNumber, 3))
        file.write(jsonOut)
        file.close()


if __name__=="__main__":
    global inputFile, outputFile, step
    inputFile = ""
    outputFile = ""
    step = 10
    try:
        if sys.argv[1] == "-i": inputFile = sys.argv[2]
        if sys.argv[3] == "-o": outputFile = sys.argv[4]
        if sys.argv[5] == "-s": step = int(sys.argv[6])
    except: sys.exit(0)

    #Creates the genetic algorithm
    ga = GAPolygons(25, 512, 0.025, 0, True)
    #Sets the polygon ga specific data
    ga.setCanvasSize(Vector(256, 256))
    ga.setFitnessThreshold(256 * 256 * 4 * 75)

    #Opens the target image
    targetImage = Image.open(inputFile)
    #Converts the image to RGBA
    targetImage = targetImage.convert("RGB")
    targetImage = targetImage.resize((256, 256))
    ga.setTargetImage(targetImage)

    #Runs the ga
    ga.generatePopulation()
    ga.run(generationCallback)