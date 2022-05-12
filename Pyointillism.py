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