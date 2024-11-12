from music21 import *

def main():
    my_rules = {'D': 'EXF', 'E': 'DYG', 'F': 'DEAXF', 'G': 'EGY'}
    pitch_map = {'D': 'D3', 'E': 'E3', 'F': 'F3', 'G': 'G3', 'A': 'A3'}
    octave = 0
    duration_map = {'Y': 0.25,'X': 0.5}

    my_stream = stream.Stream()

    current_duration = 0.5
    axiom = 'XD'
    string = lindenmayer_system(axiom, my_rules, 4)

    for symbol in string:
        if symbol in duration_map:
            new_duration = duration_map[symbol]
            if new_duration != current_duration:
                current_duration = new_duration
            else:
                octave = (octave + 1) % 2
        else:
            if symbol in pitch_map:
                new_pitch = symbol + str(3 + octave)
                dur = duration.Duration(current_duration)
                nota = note.Note(new_pitch, duration=dur)
                my_stream.append(nota)
    my_stream.show()

def lindenmayer_system(axiom: str, rules: dict, iterations: int):
    for _ in range(iterations):
        translation = [rules.get(symbol, symbol) for symbol in axiom]
        axiom = ''.join(translation)
    return axiom

if __name__ == '__main__':
    main()