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
from itertools import permutations

def rots(group):
    return [group[i:] + group[:i] for i in range(len(group))]

piece = m21.converter.parse("C:/Users/punks/Documents/GitHub/scripts_doutorado/fuzzy-example/skeleton.musicxml")

""" measures = piece.measures(1, 8)
for i,x in enumerate(piece.parts[0][1:7]):
    print(f"COMPASSO {i+1}")
    fuzzy_rtc(x, False, [3,2])
    print("--------------------------------------") """

seq_base = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75] # sequência base de sete durações

perms = permutations(seq_base) # todas as permutações possíveis da sequência base

candidates = [] # subconjunto de perms tal que as rotações possuem três graus distintos de heterogeneidade rítmica
for p in perms:
    rotations = rots(p)
    cs = [complexity(x, 3, 1) for x in rotations]
    if len(set(cs)) == 3:
        candidates.append(p)

pcs = [60,62,71,64,69,65, 67]


group_rots = [
    [0.5, 1, 0.25, 0.75, 1.5, 1.25, 1.75], #0.627
    [0.5, 1, 0.25, 0.75, 1.25, 1.75, 1.5], #0.519
    [0.5, 1, 0.25, 1.25, 0.75, 1.75, 1.5], #0.411
    [0.5, 1, 1.25, 1.5, 1.75, 0.25, 0.75], #0.37
    [0.5, 0.25, 0.75, 1, 1.25, 1.5, 1.75], #0.195
    [0.5, 0.25, 1, 0.75, 1.5, 1.25, 1.75], #0.262
    [1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25], #0
]

stream1 = m21.stream.Stream()
ts = m21.meter.TimeSignature('7/4')
stream1.append(ts)

pitches = [72,74,83,76,81,77,79]
order_1 = [2,11,4,9,5,7]
order_2 = [0, 10, 1, 8, 3, 6]

for rot in group_rots:
    i = 0
    rotations = rots(rot)
    while i <= 12:
        r = rotations[i % len(rot)]
        if i == 0:
            for k in range(len(rot)):
                nota = m21.note.Note(pitches[k], quarterLength=r[k])
                stream1.append(nota)
            i += 1
        elif i > 0 and i < 7:
            for j,p in enumerate(pitches):
                if p % 12 == order_1[i-1]:
                    pitches[j] -= 1
            for k in range(len(rot)):
                nota = m21.note.Note(pitches[k], quarterLength=r[k])
                stream1.append(nota)
            i += 1
        elif i >= 7 and i <= 11:
            for j, p in enumerate(pitches):
                if p % 12 == order_2[i-7]:
                    pitches[j] -= 1
            for k in range(len(rot)):
                nota = m21.note.Note(pitches[k], quarterLength=r[k])
                stream1.append(nota)
            i += 1
        elif i == 12:
            for j, p in enumerate(pitches):
                if p % 12 == 6:
                    pitches[j] -= 1
            i += 1
            
piece = stream1.makeMeasures()
score = m21.stream.Score()
part = m21.stream.Part()
for el in stream1:
    part.append(el)

score = m21.stream.Score([part]).makeMeasures()
#piece.show()            

for i,x in enumerate(score.parts[0][0:85]):
    print(f"COMPASSO {i+1}")
    measure = x.getElementsByClass("GeneralNote")
    fuzzy_rtc(measure, False, [3,1])
    print("--------------------------------------")

