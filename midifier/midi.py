import struct

def _int_to_bytes(num, num_bytes):
  '''Takes an integer, returns a 4-byte string representing it'''
  format_str = {
      1: '>B', 2: '>H', 4: '>I', 8: '>Q'}[num_bytes] 
  return struct.pack(format_str, num)

def encode_ticks(ticks):
  if ticks >= 0b10000000:
    raise Exception('Currently does not support waiting more than %d ticks' % (0b10000000 - 1))
  return ticks
  

class Formats(object):
  SINGLE_TRACK      = 0
  MULTI_TRACK_SYNC  = 1
  MUTTI_TRACH_ASYNC = 2

class Track(object):
  def __init__(self):
    self.events = []

  def add_event(self, event):
    self.events.append(event)

class Note(object):
  def __init__(self, wait_ticks, note):
    self.wait_ticks = encode_ticks(wait_ticks)
    self.note = note

  @classmethod
  def from_language(cls, note_name, wait_ticks):
    letter = note_name[:-1]
    num = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b'].index(letter.lower())
    octave = int(note_name[-1])
    return Note(wait_ticks, octave * 12 + num)

  def on_event(self, channel):
    if not 0 <= channel <= 15:
      raise Exception("Channel must be in range 0 <= channel <= 15")
    note_on_event = 0x80 | channel
    return _int_to_bytes(self.wait_ticks, 1) + _int_to_bytes(note_on_event, 1) + _int_to_bytes(self.note, 1) + '\x42' # last part is velocity - figure out later

  def off_event(self, channel):
    if not 0 <= channel <= 15:
      raise Exception("Channel must be in range 0 <= channel <= 15")
    note_on_event = 0x90 | channel
    return _int_to_bytes(self.wait_ticks, 1) + _int_to_bytes(note_on_event, 1) + _int_to_bytes(self.note, 1) + '\x42' # last part is velocity - figure out later


def program_change_event(wait_ticks, channel, program_number):
  return _int_to_bytes(encode_ticks(wait_ticks), 1) + _int_to_bytes(0xC0 | channel, 1) + _int_to_bytes(program_number, 1)

def set_volume_event(wait_ticks, channel, volume):
  return _int_to_bytes(encode_ticks(wait_ticks), 1) + _int_to_bytes(0xB0 | channel, 1) + '\x07' + _int_to_bytes(volume, 1)


class Midi(object):

  def __init__(self, file_format, tracks=None):
    self.file_format = file_format
    if tracks is not None:
      self.tracks = tracks
    else:
      self.tracks = []

    self.delta_ticks = 16*3

  def write(self, filename):
    with open(filename, 'wb') as f:
      self._write_headers(f)
      for track in self.tracks:
        self._write_track(track, f)

  def _write_headers(self, fh):
    headers = ['MThd']
    headers.append(_int_to_bytes(6, 4))
    headers.append(_int_to_bytes(self.file_format, 2))
    headers.append(_int_to_bytes(len(self.tracks), 2))
    headers.append(_int_to_bytes(self.delta_ticks, 2))
    fh.write(''.join(headers))

  def _write_track(self, track, fh):
    fh.write('MTrk')
    track_str = ''.join(track.events)
    fh.write(_int_to_bytes(len(track_str) + 4, 4)) # + 4 for the meta-event track end
    fh.write(track_str)
    fh.write('\x00\xff\x2f\x00') # end track meta-event
    
