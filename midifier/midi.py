import struct

def _int_to_bytes(num, num_bytes):
  '''Takes an integer, returns a 4-byte string representing it'''
  format_str = {
      1: '>b', 2: '>h', 4: '>i', 8: '>q'}[num_bytes] 
  return struct.pack(format_str, num)

class Formats(object):
  SINGLE_TRACK      = 0
  MULTI_TRACK_SYNC  = 1
  MUTTI_TRACH_ASYNC = 2

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

  def _write_headers(self, fh):
    headers = ['MThd']
    headers.append(_int_to_bytes(6, 4))
    headers.append(_int_to_bytes(self.file_format, 2))
    headers.append(_int_to_bytes(len(self.tracks), 2))
    headers.append(_int_to_bytes(self.delta_ticks, 2))
    fh.write(''.join(headers))
