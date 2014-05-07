from midifier.midi import Midi, Formats
from midifier.track import Track
from midifier.events import (
  NoteOnEvent, NoteOffEvent, ProgramChangeEvent, SetVolumeEvent,
  TempoEvent)
from midifier.instruments import instruments
from midifier.track_maker import TrackMaker


class Midifier(object):

  def __init__(self, files, output_file):
    self.files = files
    self.output_file = output_file
    self.ticks_per_quarter_note = 48
    self.tracks = []

  def make_midi(self):
    for fn in self.files:
      with open(fn, 'r') as f:
        content = f.read()
      self.tracks.append(TrackMaker(fn, content, self.ticks_per_quarter_note
                   ).make_track())

  def save(self):
    ff = Formats.SINGLE_TRACK if len(self.tracks) == 1 else Formats.MULTI_TRACK_SYNC
    midi = Midi(ff, self.tracks, self.ticks_per_quarter_note)
    midi.write(self.output_file)
