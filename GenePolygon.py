import Gene
from random import randint
from Vector import Vector, Vector4D
#------Classes------
#Creates a polygon gene that inherits from the Gene base class
class GenePolygon(Gene.Gene):
    #------Initialiser------
    #Creates a new Gene
    #Arguments: -The 3 coordinates of the triangle  -[Vector]
    #           -The colour of the polygon          -Vector4D
    #           -The canvasSize                     -Vector
    def __init__(self, _coords=[Vector.zero(), Vector.zero(), Vector.zero()], _colour=Vector4D.zero(), _canvasSize=Vector.zero()):
        self.coords = _coords
        self.colour = _colour
        self.canvasSize = _canvasSize

    #------Getters/Setters------
    #Arguments: -The 3 coordinates of the triangle  -[Vector]
    def setCoords(self, _coords): self.coords = _coords
    def getCoords(self): return self.coords
    def getCoordsTuple(self):
        return (self.coords[0].x, self.coords[0].y, self.coords[1].x, self.coords[1].y, self.coords[2].x, self.coords[2].y)
    #Arguments: -The colour of the polygon  -Vector4D
    def setColour(self, _colour): self.colour = _colour
    def getColour(self): return self.colour

    #------Procedures/Functions------
    #Randomises the values of the gene
    def randomise(self):
        #Randomises the base coordinate of the polygon
        self.coords[0] = Vector(randint(0, self.canvasSize.x), randint(0, self.canvasSize.y))

        #Randomises the next two points on the polygon, making sure that they are within 10 pixels (in either direction) of the base point
        self.coords[1] = self.coords[0] + Vector(randint(-10, 10), randint(-10, 10))
        self.coords[2] = self.coords[0] + Vector(randint(-10, 10), randint(-10, 10))

        #Makes sure that the points are within the canvas
        if self.coords[1].x > self.canvasSize.x: self.coords[1].x = 2 * self.canvasSize.x - self.coords[1].x
        elif self.coords[1].x < 0: self.coords[1].x *= -1
        if self.coords[1].y > self.canvasSize.y: self.coords[1].y = 2 * self.canvasSize.y - self.coords[1].y
        elif self.coords[1].y < 0: self.coords[1].y *= -1

        if self.coords[2].x > self.canvasSize.x: self.coords[2].x = 2 * self.canvasSize.x - self.coords[2].x
        elif self.coords[2].x < 0: self.coords[1].x *= -1
        if self.coords[2].y > self.canvasSize.y: self.coords[2].y = 2 * self.canvasSize.y - self.coords[2].y
        elif self.coords[2].y < 0: self.coords[1].y *= -1

        #Randomises the colour
        self.colour = Vector4D(randint(0, 255), randint(0, 255), randint(0, 255), 100)
    #Mutates the values of the gene
    def mutate(self):
        #Mutates the cooridnates by varying the coordiate's position
        self.coords[0] += Vector(randint(-3, 3), randint(-3, 3))
        self.coords[1] += Vector(randint(-3, 3), randint(-3, 3))
        self.coords[2] += Vector(randint(-3, 3), randint(-3, 3))

        #Makes sure that the points are within the canvas
        if self.coords[0].x > self.canvasSize.x: self.coords[1].x = 2 * self.canvasSize.x - self.coords[0].x
        elif self.coords[0].x < 0: self.coords[0].x *= -1
        if self.coords[0].y > self.canvasSize.y: self.coords[1].y = 2 * self.canvasSize.y - self.coords[0].y
        elif self.coords[0].y < 0: self.coords[0].y *= -1

        if self.coords[1].x > self.canvasSize.x: self.coords[1].x = 2 * self.canvasSize.x - self.coords[1].x
        elif self.coords[1].x < 0: self.coords[1].x *= -1
        if self.coords[1].y > self.canvasSize.y: self.coords[1].y = 2 * self.canvasSize.y - self.coords[1].y
        elif self.coords[1].y < 0: self.coords[1].y *= -1

        if self.coords[2].x > self.canvasSize.x: self.coords[2].x = 2 * self.canvasSize.x - self.coords[2].x
        elif self.coords[2].x < 0: self.coords[1].x *= -1
        if self.coords[2].y > self.canvasSize.y: self.coords[2].y = 2 * self.canvasSize.y - self.coords[2].y
        elif self.coords[2].y < 0: self.coords[1].y *= -1

        #Muates the colour by variating the RGB values
        self.colour += Vector4D(randint(-20, 20), randint(-20, 20), randint(-20, 20), randint(-20, 20))

        #Ensures that the colour is within the bounds
        if self.colour.x > 255: self.colour.x = 510 - self.colour.x
        elif self.colour.x < 0: self.colour.x *= -1
        if self.colour.y > 255: self.colour.y = 510 - self.colour.y
        elif self.colour.y < 0: self.colour.y *= -1
        if self.colour.z > 255: self.colour.z = 510 - self.colour.z
        elif self.colour.z < 0: self.colour.z *= -1
        if self.colour.w > 255: self.colour.w = 510 - self.colour.w
        elif self.colour.w < 0: self.colour.w *= -1
    #Returns:   -A copy of itself       -Gene
    def copy(self):
        gene = GenePolygon(_canvasSize=self.canvasSize)
        #Copies the coordinates
        geneCoords = [coord.copy() for coord in self.coords]
        gene.setCoords(geneCoords)
        #Copies the colours
        geneColours = self.colour.copy()
        gene.setColour(geneColours)
        return gene
    #Returns:   -The dump of the dna    -String
    def dump(self): 
        dump = '{"coords":%s, "colours":%s}'
        coordsDump = "["
        for i in range(len(self.coords)):
            coordsDump += self.coords[i].dump()
            if i != len(self.coords) - 1: coordsDump += ","
        coordsDump += "]"
        coloursDump = '{"r":%s, "g":%s, "b":%s, "a":%s}'%(self.colour.x, self.colour.y, self.colour.z, self.colour.w)
        dump = dump%(coordsDump, coloursDump)
        return dump