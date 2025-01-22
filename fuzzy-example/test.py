from dissonance import *
from contours import *
from complexity import *
from all_classes import allClasses
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import music21 as m21
from fuzzy_system import fuzzy_rtc
#from allsix import all_six
import pickle
from collections import defaultdict


trecho_filename = "C:/Users/punks/Documents/GitHub/scripts_doutorado/fuzzy-example/trecho2.musicxml"
#fuzzy_rtc(trecho_filename)

# trecho diatonico
#Heterogeneidade rítmicas:  -0.0
#Índice de consonância:  4.754999999999999
#Índice na tabela de partições:  4.284249995979899
n = 6
#all_six = all_contours(n)

with open("fuzzy-example/allseven.pkl", "rb") as f:
    all_seven = pickle.load(f)

d = defaultdict(list)

for x in all_seven:
    d[complexity(x,2,1)].append(x)

for k in d.keys():
    print(k, len(d[k]))


a = [5,3,1,2,4,0,6]

def rotx(x, n):
    return x[n:] + x[:n]

for i in range(7):
    print(complexity(rotx(a,i), 4, 2))


'''
c = [x for x in all_six if len(set(x)) == n]
for x in all_six:
    print(x, complexity(x))
    print("-------------------------")'''