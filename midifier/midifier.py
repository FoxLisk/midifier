from midi import Midi, Formats

midi = Midi(Formats.SINGLE_TRACK)
midi.write('test.mid')
