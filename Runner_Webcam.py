#------Generic Imports------
from PIL import Image, ImageDraw, ImageChops, ImageTk
from cv2 import cv2
import sys, math, threading
import tkinter
#------Specific Imports------
from Vector import Vector
from GAPolygons import GAPolygons

class Runner_Webcam:
    #------Initialiser------
    def __init__(self):
        #Sets up storage for the images that are used
        self.webcamImg = None
        self.gaImg = None
        self.diffImg = None

        #Sets up video capture
        self.camCapture = cv2.VideoCapture(0)
        #Gets the first frame
        ret, frame = self.camCapture.read() 
        print(frame.shape)
        #Converts to pil
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.webcamImg = Image.fromarray(img)
        self.gaImg = self.webcamImg

        #--Genetic Algorithm
        #Creates the genetic algorithm
        self.ga = GAPolygons(24, 768, 0.025, 0, True)
        #Sets the polygon ga specific data
        self.ga.setCanvasSize(Vector(256, 256))
        #Sets the target image of the genetic algorithm to the first frame
        self.ga.setTargetImage(self.webcamImg.resize(size=(256, 256)))
        self.ga.generatePopulation()

        #Creates the gaThread
        self.gaThread = threading.Thread(target=self.ga.run, args=(self.callback,))
        self.gaThread.start()

        #Creates the webcam thread
        self.wcThread = threading.Thread(target=self.getWebcam)
        self.wcThread.start()

        #--Tkinter
        #Creates the root interface
        self.tkRoot = tkinter.Tk()
        self.tkRoot.geometry("1536x720")
        #Creates the generation number
        self.tkGen = tkinter.Label(self.tkRoot, text="Generation: 0")
        self.tkGen.place(x=0, y=0, height= 10)
        #Creates a canvas for the image
        self.tkImage = tkinter.Label(self.tkRoot, text="Hello")
        self.tkImage.place(x=0, y=10, width=1280, height = 720)
        #Creates a canvas for the reference image
        self.tkReference = tkinter.Label(self.tkRoot, text="Hello")
        self.tkReference.place(x=1280, y=10, width=128, height=72)
        #Creates a canvas for the difference image
        self.tkDiff = tkinter.Label(self.tkRoot, text="Hello")
        self.tkDiff.place(x=1280, y=82, width=128, height=72)
    #Sets up the function for the with command, i.e. with Runner_Webcam as runner:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.camCapture.release()

    #------Procedures/Functions------
    #Defines the callback procedure for the ga
    def callback(self, ga, timeElapsed):
        self.tkGen["text"] = "Generation: %s"%ga.generationNumber
        self.gaImg = Image.new("RGB", (1280, 720), (255, 255, 255))
        #Creates a canvas for the image
        drawingCanvas = ImageDraw.Draw(self.gaImg, "RGBA")
        #Draws polygons on the image based on the DNA of the member
        for gene in ga.bestMember.getDNA().getGenes():
            #Draws on the image
            xy = []
            for i in range(3):
                xy.append(gene.getCoords()[i].x * 1280 / 256)
                xy.append(gene.getCoords()[i].y * 720 / 256)
            drawingCanvas.polygon(xy=tuple(xy), fill=(gene.getColour().x, gene.getColour().y, gene.getColour().z, gene.getColour().w))
        del drawingCanvas

        self.diffImg = ImageChops.difference(ga.targetImage, self.gaImg)

        self.ga.setTargetImage(self.webcamImg.resize(size=(256, 256)))

    #Gets a feed from the webcam
    def getWebcam(self):
        while True:
            #Gets the next webcam image
            ret, frame = self.camCapture.read() 
            #Converts to pil
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.webcamImg = Image.fromarray(img)

    #Provides the update function
    def update(self):
        #Renders the display
        self.display()
        #Sets up the next screen call
        self.tkRoot.after(10, self.update)
    #Displays the GA image
    def display(self):
        #Shows the image
        image = ImageTk.PhotoImage(self.gaImg.resize(size=(1280, 720)))
        self.tkImage.configure(image=image)
        self.tkImage.image = image
        #Shows the webcam reference image
        image = ImageTk.PhotoImage(self.webcamImg.resize(size=(128, 72)))
        self.tkReference.configure(image=image)
        self.tkReference.image = image
        #Shows the difference image
        if self.diffImg:
            image = ImageTk.PhotoImage(self.diffImg.resize(size=(128, 72)))
            self.tkDiff.configure(image=image)
            self.tkDiff.image = image


if __name__=="__main__":
    with Runner_Webcam() as runner:
        #Sets up the mainloop
        runner.tkRoot.after(10, runner.update)
        runner.tkRoot.mainloop()