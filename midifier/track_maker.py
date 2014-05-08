from parser.parser import Parser
from parser.parser import Events as Tokens
from midifier.instruments import instruments
from midifier.track import Track
from midifier.events import *
import random

class StackFrame(object):
  def __init__(self, channel, key, last_note):
    self.channel = channel
    self.key = key
    self.last_note = last_note

class TrackMaker(object):

  def __init__(self, filename, content, ticks_per_quarter_note):
    self.filename = filename
    self.content = content
    self.ticks_per_quarter_note = ticks_per_quarter_note
    self.eighth_note = self.ticks_per_quarter_note / 2
    self.sixteenth_note = self.ticks_per_quarter_note / 4


  def _generate_key(self, note=None):
      '''
      generates a major key starting from the given note
      if note is None, generates a random key
      '''
      if note is None:
        note = random.randint(0, 127)
      if isinstance(note, basestring):
        note = from_language(note)

      key = [note, note+2, note+4, note+5, note+7, note+9, note+11, note+12]
      return key


  def make_track(self):
    track = Track()
    track.add_event(TempoEvent(60)) #bpm
    parser = Parser(self.content)

    channel_stack = []
    used_up_channels = []

    key = self._generate_key(random.randint(48, 72))
    last_note = random.choice(key)
    frame = StackFrame(track.new_channel(), key, last_note)

    frame.channel.add_event(ProgramChangeEvent, 0, random.choice(instruments.values()))
    frame.channel.add_event(SetVolumeEvent, 0, 0x32)
    frame.channel.add_event(NoteOnEvent, 0, last_note, 0x42)

    # for every function scope we enter, we want a new channel,
    # and we want a new key for it, and we want to immediately start
    # a note playing. In function scope, every assignment should end that note and start a new note
    # on that channel. Every other scope starts another note that ends when that scope ends, and behaves similarly
    # with assignments

    # when a scope ends we end its current note
    tok = parser.next_token()
    while tok is not None:
      if tok == Tokens.FUNCTION_START:
        # create a new channel, a new key, and the last note put on this channel
        # start that note playing
        key = self._generate_key(random.randint(48, 72))
        last_note = random.choice(key)
        channel_stack.append(frame)
        if used_up_channels:
          frame = used_up_channels.pop()
        else:
          frame = StackFrame(track.new_channel(), key, last_note)
        frame.channel.add_event(ProgramChangeEvent, 0, random.choice(instruments.values()))
        frame.channel.add_event(SetVolumeEvent, 0, 0x32)
        frame.channel.add_event(NoteOnEvent, 0, last_note, 0x42)
      elif tok == Tokens.FUNCTION_END:
        frame.channel.add_event(NoteOffEvent, self.eighth_note, last_note, 0x42)
        used_up_channels.append(frame)
        frame = channel_stack.pop()
      elif tok == Tokens.ASSIGNMENT:
        frame.channel.add_event(NoteOffEvent, self.eighth_note, last_note, 0x42)
        last_note = frame.key[(frame.key.index(frame.last_note) + 1) % len(frame.key)]
        frame.channel.add_event(NoteOnEvent, 0, last_note, 0x42)
      elif tok == Tokens.OTHER_SCOPE_START:
        pass
      elif tok == Tokens.OTHER_SCOPE_END:
        pass
      elif tok == Tokens.INVALID_SOURCE:
        pass
      tok = parser.next_token()
    return track
