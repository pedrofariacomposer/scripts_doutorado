import abjad
import math

def make_tuplet(outer, inner, retrograde=False):
    numerator = 1 + outer
    exponent = int(math.log(numerator, 2))
    denominator = 2**exponent
    outer_string = f"{numerator}:{denominator}"
    lone_note_denominator = denominator * 4
    lone_note_duration = (1, lone_note_denominator)
    lone_note = abjad.Note("c'", lone_note_duration)
    duration = (outer, lone_note_denominator)
    ratio = inner * (1,)
    maker = abjad.makers.tuplet_from_duration_and_ratio
    inner_tuplet = maker(duration, ratio)
    multiplier = abjad.Fraction(*inner_tuplet.multiplier)
    pair = abjad.duration.with_denominator(multiplier, inner)
    inner_tuplet.multiplier = pair
    inner_tuplet.hide = inner_tuplet.trivial()
    if retrograde:
        contents = [inner_tuplet, lone_note]
        label = f'"({outer} | {inner}) : 1"'
    else:
        label = f'"1 : ({outer} | {inner})"'
        contents = [lone_note, inner_tuplet]
    outer_tuplet = abjad.Tuplet(outer_string, contents)
    markup = abjad.Markup(rf"\markup {label}")
    note = abjad.select.note(outer_tuplet, 0)
    abjad.attach(markup, note, direction=abjad.UP)
    outer_tuplet.hide = outer_tuplet.trivial()
    abjad.tweak(inner_tuplet, r"\tweak staff-padding 0")
    abjad.tweak(outer_tuplet, r"\tweak staff-padding 2")
    return outer_tuplet

def make_row(outer, column_count, retrograde=False):
    tuplets = []
    for inner in range(1, column_count + 1):
        tuplet = make_tuplet(outer, inner, retrograde=retrograde)
        tuplets.append(tuplet)
    return tuplets

def make_score(row_count, column_count, retrograde=False):
    score = abjad.Score(name="Score")
    for row_number in range(1, row_count + 1):
        tuplets = make_row(row_number, column_count, retrograde=retrograde)
        voice = abjad.Voice(tuplets, name=f"Row_{row_number}_Voice")
        staff = abjad.Staff([voice], name=f"Row_{row_number}_Staff")
        score.append(staff)
    return score

preamble = r"""#(set-global-staff-size 12)

\layout {
    \context {
        \Staff
        \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 20
    }
    \context {
        \Score
        \override BarLine.stencil = ##f
        \override Clef.stencil = ##f
        \override StaffSymbol.stencil = ##f
        \override SystemStartBar.stencil = ##f
        \override TextScript.color = #blue
        \override TextScript.staff-padding = #6
        \override TimeSignature.stencil = ##f
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
        proportionalNotationDuration = #(ly:make-moment 1 40)
        tupletFullLength = ##t
    }
}
"""

score = make_score(5, 6)
lilypond_file = abjad.LilyPondFile([preamble, score])
abjad.show(lilypond_file)