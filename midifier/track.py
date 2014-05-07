from events import TRACK_END_EVENT
from utils import _int_to_bytes


class Track(object):

  class Channel(object):

    def __init__(self, channel, track):
      self.channel = channel
      self.track = track

    def add_event(self, _class, wait_ticks, *args):
      self.track.add_event(_class(wait_ticks, self.channel, *args))


  def __init__(self):
    self.events = []
    self.next_channel = 0

  def new_channel(self):
    if self.next_channel > 0xF:
      raise Exception('You can only have %d channels per track' % 0xF)
    channel = Track.Channel(self.next_channel, self)
    self.next_channel += 1
    return channel

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
