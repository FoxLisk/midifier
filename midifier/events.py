from abc import ABCMeta, abstractmethod

from utils import _int_to_bytes


def encode_ticks(ticks):
  if ticks >= 0b10000000:
    raise Exception('Currently does not support waiting more than %d ticks' % (0b10000000 - 1))
  return _int_to_bytes(ticks, 1)


class Event(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def encode(self):
    pass

  @abstractmethod
  def len_in_bytes(self):
    pass
  

class ChannelEvent(Event):
  def __init__(self, _type, wait_ticks, channel, *args):
    self.wait_ticks = encode_ticks(wait_ticks)
    self._type = _type
    self.channel = channel
    self.args = args

  def encode(self):
    _bytes = self.wait_ticks
    _bytes += _int_to_bytes(self._type | self.channel, 1)
    _bytes += ''.join([_int_to_bytes(arg, 1) for arg in self.args])
    return _bytes

  def len_in_bytes(self):
    return len(self.wait_ticks) + 1 + len(self.args)

def curry(func, arg):
  return lambda *args: func(arg, *args)

def note_from_language(note_name):
  if isinstance(note_name, int):
    return note_name
  letter = note_name[:-1]
  num = {'c': 0,
   'c#': 1,
   'db': 1,
   'd': 2,
   'd#': 3,
   'eb': 3,
   'e': 4,
   'f': 5,
   'f#': 6,
   'gb': 6,
   'g': 7,
   'g#': 8,
   'ab': 8,
   'a': 9,
   'a#': 10,
   'bb': 10,
   'b': 11
   }[letter.lower()]

  octave = int(note_name[-1])
  return octave*12 + num

# just use \x42 for velocity until i actually understand it
def NoteOnEvent(wait_ticks, channel, note_name, velocity):
  return ChannelEvent(0x90, wait_ticks, channel, note_from_language(note_name), velocity)

def NoteOffEvent(wait_ticks, channel, note_name, velocity):
  return ChannelEvent(0x80, wait_ticks, channel, note_from_language(note_name), velocity)

ProgramChangeEvent = curry(ChannelEvent, 0xc0)



ControllerEvent = curry(ChannelEvent, 0xb0)
SetVolumeEvent = lambda wait_ticks, channel, volume: ControllerEvent(wait_ticks, channel, 0x07, volume)

class MetaEvent(Event):
  def __init__(self, _type, *args):
    self._type = _type
    self.args = args

  def encode(self):
    _bytes = '\x00\xff' + _int_to_bytes(self._type, 1)
    _bytes += _int_to_bytes(len(self.args), 1)
    _bytes += ''.join(_int_to_bytes(a, 1) for a in self.args)
    return _bytes

  def len_in_bytes(self):
    return 4 + len(self.args)
    

TRACK_END_EVENT = MetaEvent(0x2f)

MICROSECONDS_PER_MINUTE = 60000000
class TempoEvent(Event):
  def __init__(self, bpm):
    # microseconds per quarter note
    self.mpqn = MICROSECONDS_PER_MINUTE / bpm

  def encode(self):
    _bytes = '\x00\xff\x51\x03'
    _bytes += _int_to_bytes(self.mpqn, 3)
    return _bytes

  def len_in_bytes(self):
    return 7

