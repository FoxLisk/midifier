from midi import Midi, Formats
from track import Track
from events import (
  NoteOnEvent, NoteOffEvent, ProgramChangeEvent, SetVolumeEvent,
  TempoEvent)
from instruments import instruments

track = Track()
track.add_event(ProgramChangeEvent(0, 0, instruments['Bright Acoustic Piano']))
track.add_event(SetVolumeEvent(0, 0, 0x32))
track.add_event(TempoEvent(60))
track.add_event(NoteOnEvent(0, 0, 'c4', 0x42))
track.add_event(NoteOnEvent(20, 0, 'g4', 0x42))
track.add_event(NoteOffEvent(20, 0, 'c4', 0x42))
track.add_event(NoteOffEvent(50, 0, 'g4', 0x42))

midi = Midi(Formats.SINGLE_TRACK, [track])
midi.write('test2.mid')
