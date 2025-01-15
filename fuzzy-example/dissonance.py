from all_classes import *

def interval_vector(chord):
    chord_mod_12 = [el % 12 for el in chord]
    chord_mod_12 = list(set(chord_mod_12))

    vector = [0] * 6
    for i, el in enumerate(chord_mod_12):
        for j in chord_mod_12[i+1:]:
            interval = (j - el) % 12
            if interval > 6:
                interval = 12 - interval
            vector[interval-1] += 1
    return vector
            
def dissonance(chord):
    vector = interval_vector(chord)
    multipliers = [-1.428, -0.582, 0.594, 0.386, 1.240, -0.453]
    result = 0
    for pair in zip(vector, multipliers):
        result += (pair[0] * pair[1])
    return result