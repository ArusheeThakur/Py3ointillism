import os
from re import X
import sys
import random
from copy import deepcopy
import multiprocessing
import numpy
from PIL import Image, ImageDraw

# Global variables or Knobs and Dials 
POPULATION=50
MUTATION_CHANCE=0.05
ADD_GENE_CHANCE=0.3
rEM_GENE_CHANCE=0.2
INITIAL_GENES=50
GENErATIONS_PEr_IMAGE=100

try:
    targetImage=Image.open("target.png")
except:
    print("Please check input file")
    exit()

class Position:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,o):
        return Position(self.x+o.x, self.y+o.y)

class Color:
    def __init__(self, r, g, b):
        self.r=r
        self.g=g
        self.b=b
    def shift(self,r , g, b):
        self.r=max(0, (min(self.r+r, 255)))
        self.g=max(0, (min(self.g+g, 255)))
        self.b=max(0, (min(self.b+b, 255)))

class Gene:
    def __init__(self, size):
        #here attributes are size and function is mutate 
        #Diameter,Position and color are all classes define above 
        self.size=size
        self.diameter=random.randint(5,15)
        self.pos=Position(random.randint(0,size[0]), random.randint(0, size[1]))
        self.color=Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.params=["diameter", "position", "color"]
    
    def mutate(self):
        #probability gauss=continous discontinuity function 
        mutationSize=max(1, int(round(random.gauss(15,4))))/100 
        mutationType=random.choice(self.params)
        #Need to genereate a new diameter which is withing the bound of previous diameter
        lowerBound = 1-mutationSize 
        upperBound = 1+mutationSize
        if mutationType=="diameter":
            smallerDiameter=int(self.diameter*(lowerBound)) 
            biggerDiameter=int(self.diameter*(upperBound))
            newDiameterValue = random.randint(smallerDiameter,biggerDiameter)
            self.diameter = max(1,newDiameterValue)
        elif mutationType=="position":
            #Again using the same logic as above we generate/mutate a new position 
            #The new position is within the bounds of the previous positions*lower/upper bound
            leftX=int(self.pos.x*(lowerBound))
            rightX=int(self.pos.x*(upperBound))
            x = max(0,random.randint(leftX ,rightX))
            leftY=int(self.pos.y*(lowerBound))
            rightY=int(self.pos.y*(upperBound))
            y = max(0,random.randint(leftY ,rightY))
            newY = min(y,self.size[1])
            newX = min(x,self.size[0])
            self.pos = Position(newX,newY)
        elif mutationType=="color": 
            #Again using the same logic as above we generate/mutate a new rgb values  
            #The new values are within the bounds of the previous values*lower/upper bound
            #Also here self.color.r/b/g means that we are using class color in class gene 
            less_red=int(self.color.r*(lowerBound))
            more_red=int(self.color.r*(upperBound))
            less_green=int(self.color.g*(lowerBound))
            more_green=int(self.color.g*(upperBound))
            less_blue=int(self.color.b*(lowerBound))
            more_blue=int(self.color.b*(upperBound))
            r = min(max(0,random.randint(less_red,more_red,255)))
            g = min(max(0,random.randint(less_green,more_green,255)))
            b = min(max(0,random.randint(less_blue,more_blue,255)))
            self.color = Color(r,g,b)

class Organism:

    def __init__(self,size,num):
        self.size = size
        self.genes=[] #Here we are creating an array 
        for _ in range(num):
            g=Gene(size) #Okay here is a slight dout that I have, is the size here gene size??
            #appending/adding genes
            self.genes.append(g) 
      
    def mutate(self):
        #here we see if the length of the array self gene is less than 200 then we genereate 
        #a random floast value between 0 and 1 this is what random.random function does 
        #if its lesser than mutation chance then the genes will mutate 
        if len(self.genes) < 200:
            for g in self.genes:
                if MUTATION_CHANCE > random.random():
                    g.mutate()

        else:
            #mh v
            no_of_genes =int(len(self.genes)*MUTATION_CHANCE)
            for g in random.sample(self.genes,no_of_genes):
                g.mutate()

        if ADD_GENE_CHANCE > random.random():
            self.genes.append(Gene(self.size))
            
        if len(self.genes)>0 and rEM_GENE_CHANCE < random.random():
            self.genes.remove(random.choice(self.genes))

    def drawImage(self):
        image = Image.new("rGB",self.size,(255,255,255))
        canvas= ImageDraw.Draw(image)

        for gene in self.genes:
            colour = (gene.color.r, gene.color.g, gene.color.b)

        for g in self.genes:
            color = (g.color.r,g.color.g,g.color.b)
            left_x=g.pos.x-g.diameter
            left_y=g.pos.y-g.diameter
            right_x=g.pos.x+g.diameter
            right_y=g.pos.y+g.diameter
            canvas.ellipse([left_x,left_y,right_x,right_y],outline=color,fill=color)

            return image