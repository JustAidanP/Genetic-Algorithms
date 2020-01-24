#------Classes------
#Defines a member object
class Member:
    #------Initialiser------
    #Arguments: -The DNA of the member      -DNA
    #           -The fitness of the member  -Float  -Default None
    def __init__(self, _dna, _fitness=None):
        self.dna = _dna
        self.fitness = _fitness
    
    #------Getters/Setters------
    #Arguments: -The DNA of the member  -DNA
    def setDNA(self, _dna): self.dna = _dna
    def getDNA(self): return self.dna
    #Arguments: -The fitness of the member  -Float
    def setFitness(self, _fitness): self.fitness = _fitness
    def getFitness(self): return self.fitness

    #------Procedures/Functions------
    #Returns:   -The dump of the dna    -String
    def dump(self):
        dump = '{"dna":%s, "fitness":%s}'%(self.dna.dump(), self.fitness)
        return dump


#Defines a population object
class Population:
    #------Initialiser------
    #Arguments: -The member list    -[Member]
    def __init__(self ,_members=[]):
        self.members = _members
    
    #------Getters/Setters------
    #Arguments: -The member list    -[Member]
    def setMembers(self, _members): self.members = _members
    def getMembers(self): return self.members

    #------Procedures/Functions------
    #Adds a member to the member list
    #Arguments: -A member   -Member
    def addMember(self, _member): self.members.append(_member)
    #Empties the member list
    def empty(self): self.members = []