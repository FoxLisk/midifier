from events import TRACK_END_EVENT
from utils import _int_to_bytes


class Track(object):
  def __init__(self):
    self.events = []

  def add_event(self, event):
    self.events.append(event)

  def encode(self):
    _bytes = ['MTrk', _int_to_bytes(self.len_in_bytes(), 4)]
    _bytes.extend([event.encode() for event in self.events])
    _bytes.append(TRACK_END_EVENT.encode())
    return ''.join(_bytes)

  def len_in_bytes(self):
    return sum(event.len_in_bytes() for event in self.events
      ) + TRACK_END_EVENT.len_in_bytes()
