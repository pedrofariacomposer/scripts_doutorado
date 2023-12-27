from scamp import *
from random import random, choice

s = Session() # inicia a sessão
cello = s.new_part("cello") # define um instrumento
s.start_transcribing() # avisa ao programa para iniciar o processo de transcrição

def wrap_in_range(value, low, high):  # função para manter as alturas escolhidadas em um alcance determinado
    return (value - low) % (high - low) + low

forte_piano = Envelope.from_levels_and_durations(          # envelope da dinâmica fp
    [0.8, 0.4, 1.0], [0.2, 0.8], curve_shapes = [0, 3]
)
diminuendo = Envelope.from_levels([0.8, 0.3]) # envelope para diminuendo

interval = 1 # intervalo inicial de um semitom
cello_pitch = 48 # altura inicial
bar_lines = [] # lista de tempos onde vão estar as barras de compasso

while s.time() < 60:  #início do processo musical
    if random() < 0.7:
        cello.play_note(cello_pitch, forte_piano, choice([1.0, 1.5]))
    else:
        bar_lines.append(s.time())
        cello.play_note(cello_pitch, diminuendo, choice([2.0, 2.5, 3.0]))
        wait(choice([0.5, 1.0]))
    cello_pitch = wrap_in_range(cello_pitch + interval, 36, 60)
    interval += 1
s.stop_transcribing().to_score(bar_line_locations=bar_lines).show() # termina a transcrição e gera a partitura





