from utils import _int_to_bytes

class Formats(object):
  SINGLE_TRACK      = 0
  MULTI_TRACK_SYNC  = 1
  MUTTI_TRACH_ASYNC = 2

class Midi(object):
  def __init__(self, file_format, tracks=None, delta_ticks=48):
    self.file_format = file_format
    if tracks is not None:
      self.tracks = tracks
    else:
      self.tracks = []

    self.delta_ticks = delta_ticks

  def write(self, filename):
    with open(filename, 'wb') as f:
      self._write_headers(f)
      for track in self.tracks:
        f.write(track.encode())

  def _write_headers(self, fh):
    headers = ['MThd']
    headers.append(_int_to_bytes(6, 4))
    headers.append(_int_to_bytes(self.file_format, 2))
    headers.append(_int_to_bytes(len(self.tracks), 2))
    headers.append(_int_to_bytes(self.delta_ticks, 2))
    fh.write(''.join(headers))
