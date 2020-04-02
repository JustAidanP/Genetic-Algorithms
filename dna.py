from copy import deepcopy
from random import randint
import random, time
from Gene import Gene
#------Classes------
#Holds all of the genes and handles creating a new set of DNA based on two old ones
class DNA:
    #------Initialiser------
    #Arguments: -The desired genes  -[Gene]
    def __init__(self, desiredGenes=[]):
        self.genes = desiredGenes

    #------Getters/Setters------
    #Gets the genes
    def getGenes(self): return self.genes

    #------Procedures/Functions------
    #Fuses together two dns objects
    #Arguments: -The dna of the other object    -DNA
    #           -The mutation rate              -Float
    #Returns:   -The fused dna                  -DNA
    def fusion(self, otherDNA, mutationRate = 0):
        #Stores a new dna object
        fusedDNA = DNA.new()

        #Starts adding one of the two dna objects genes to the fusedDNA
        for i in range(max(len(self.genes), len(otherDNA.genes))):
            #Forces use of otherDNA genes
            if i > len(self.genes):
                fusedDNA.addGene(otherDNA.genes[i])
            #Forces use of self genes
            elif i > len(otherDNA.genes):
                fusedDNA.addGene(self.genes[i])
            else:
                #Randomly chooses a gene to use
                if randint(0,1) == 0:
                    fusedDNA.addGene(self.genes[i])
                else:
                    fusedDNA.addGene(otherDNA.genes[i])
            #Mutates the gene if it falls within the mutation rate
            if random.uniform(0, 1) < mutationRate: 
                fusedDNA.genes[i] = fusedDNA.genes[i].copy()
                fusedDNA.genes[i].mutate()

        #Returns the fused dna
        return fusedDNA

    #Fills the genes list with random genes
    #Arguments: -A base gene            -Gene
    #           -The number of genes    -Int
    def createGenes(self, gene=Gene(), n=1):
        for i in range(n):
            #Creates a new gene
            gene = deepcopy(gene)
            gene.randomise()
            #Adds the gene to the list
            self.genes.append(gene)
        
    #Adds a known gene, it copies the gene before adding
    #Arguments: -The gene   -Gene
    def addGene(self, gene):
        # self.genes.append(deepcopy(gene))
        # self.genes.append(gene.copy())
        self.genes.append(gene)

    #Returns:   -A new dna  -DNA
    @staticmethod
    def new():
        return DNA([])

    #Returns:   -The dump of the dna    -String
    def dump(self):
        #Dumps the genes
        dump = "["
        for gene in self.genes:
            dump += gene.dump()
            dump += ","
        dump = dump[:-1]
        return dump + "]"