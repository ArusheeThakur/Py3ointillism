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
        