from dissonance import *
from contours import *
from complexity import *
from all_classes import allClasses
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import music21 as m21


def fuzzy_rtc(filename, xmlfile=True, params=[3,2]):

    if xmlfile:
        trecho = m21.converter.parse(filename).flatten().stripTies()
    else:
        trecho = filename
    pitches = [x.pitch.midi for x in trecho.notes]
    rit = [x.quarterLength for x in trecho.notes]
    print(rit)
    comp = complexity(rit, size=params[0], next_group=params[1])
    diss = dissonance(pitches)

    # Step 1: Define the fuzzy sets for input variables (complexity and dissonance)
    comp_universe = np.arange(0, 1001, 1)
    diss_universe = np.arange(0, 10916, 1)
    complexity_mf = ctrl.Antecedent(comp_universe, 'complexity')
    dissonance_mf = ctrl.Antecedent(diss_universe, 'dissonance')

    # Membership functions for complexity and dissonance
    complexity_mf['low'] = fuzz.trimf(complexity_mf.universe, [0, 0, 500])
    complexity_mf['mid'] = fuzz.trimf(complexity_mf.universe, [0, 500, 1000])
    complexity_mf['high'] = fuzz.trimf(complexity_mf.universe, [500, 1000, 1000])

    dissonance_mf['low'] = fuzz.trimf(dissonance_mf.universe, [0, 0, 5458])
    dissonance_mf['mid'] = fuzz.trimf(dissonance_mf.universe, [0, 5458, 10915])
    dissonance_mf['high'] = fuzz.trimf(dissonance_mf.universe, [5458, 10915, 10915])

    # Step 2: Define the fuzzy sets for output variable (texture)
    texture_mf = ctrl.Consequent(np.arange(0, 39, 1), 'texture')

    # Membership functions for cost benefit
    texture_mf['low'] = fuzz.trimf(texture_mf.universe, [0, 0, 19])
    texture_mf['mid'] = fuzz.trimf(texture_mf.universe, [0, 19, 38])
    texture_mf['high'] = fuzz.trimf(texture_mf.universe, [19, 38, 38])

    # Step 3: Define the fuzzy rules
    rule1 = ctrl.Rule(complexity_mf['high'] & dissonance_mf['high'], texture_mf['low'])
    rule2 = ctrl.Rule(complexity_mf['high'] & dissonance_mf['low'], texture_mf['mid'])
    rule3 = ctrl.Rule(complexity_mf['high'] & dissonance_mf['mid'], texture_mf['mid'])

    rule4 = ctrl.Rule(complexity_mf['low'] & dissonance_mf['low'], texture_mf['high'])
    rule5 = ctrl.Rule(complexity_mf['low'] & dissonance_mf['high'], texture_mf['low'])
    rule6 = ctrl.Rule(complexity_mf['low'] & dissonance_mf['mid'], texture_mf['high'])

    rule7 = ctrl.Rule(complexity_mf['mid'] & dissonance_mf['high'], texture_mf['low'])
    rule8 = ctrl.Rule(complexity_mf['mid'] & dissonance_mf['low'], texture_mf['high'])
    rule9 = ctrl.Rule(complexity_mf['mid'] & dissonance_mf['mid'], texture_mf['mid'])


    # Step 4: Implement the fuzzy inference system
    texture_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9 ])
    texture_sim = ctrl.ControlSystemSimulation(texture_ctrl)

    # Step 5: Test the fuzzy logic system with sample inputs
    texture_sim.input['complexity'] = comp * 1000
    texture_sim.input['dissonance'] = (diss * 1000) + 5917

    texture_sim.compute()

    print("Heterogeneidade rítmicas: ", comp)
    print("Índice de consonância: ", diss)
    print("Índice na tabela de partições: ", texture_sim.output['texture'])


