from parser.parser import Parser
from midifier.instruments import instruments
from midifier.track import Track
from midifier.events import *
import random

class TrackMaker(object):

  def __init__(self, filename, content, ticks_per_quarter_note):
    self.filename = filename
    self.content = content
    self.ticks_per_quarter_note = ticks_per_quarter_note
    self.eighth_note = self.ticks_per_quarter_note / 2
    self.sixteenth_note = self.ticks_per_quarter_note / 4

  def make_track(self):
    track = Track()
    chan = track.new_channel()
    chan.add_event(ProgramChangeEvent, 0, random.choice(instruments.values()))
    chan.add_event(SetVolumeEvent, 0, 0x32)
    track.add_event(TempoEvent(60)) #bpm
    chan.add_event(NoteOnEvent, 0,              'e5' , 0x42)
    chan.add_event(NoteOffEvent, self.eighth_note * random.randint(1, 6), 'e5' , 0x42)
    chan.add_event(NoteOnEvent, 0,              'd5' , 0x42)
    chan.add_event(NoteOffEvent, self.eighth_note * random.randint(1, 6), 'd5' , 0x42)
    return track
