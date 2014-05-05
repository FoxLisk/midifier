from midi import Midi, Formats, program_change_event, Track, set_volume_event, Note

track = Track()
track.add_event(program_change_event(0, 0, 48))
track.add_event(set_volume_event(0, 0, 0x32))
#import pudb; pu.db
track.add_event(Note.from_language('C4', 0).on_event(1))
track.add_event(Note.from_language('G4', 20).on_event(1))
track.add_event(Note.from_language('C4', 10).off_event(1))
track.add_event(Note.from_language('G4', 20).off_event(1))

midi = Midi(Formats.SINGLE_TRACK, [track])
midi.write('test.mid')
