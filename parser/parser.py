'''
we want:
  1. function start/end
  2. assignments:
    += *= /= -= = %= <<= >>= >>>= &= ^= |=
  3. non-function 'scope' starts (if/else/for/while/do-while/try/catch/finally/switch/with)

  when we encounter one, we emit the appropriate event.
'''

import re

class EOF(Exception):
  pass

class Events(object):
  FUNCTION_START = 0
  FUNCTION_END = 1
  ASSIGNMENT = 2
  OTHER_SCOPE_START = 3
  OTHER_SCOPE_END = 4


class Parser(object):
  def __init__(self, content):
    self.content = content
    self.pos = 0
    self.skip_whitespace()
    self.scope_stack = []
    self.word_start_re = re.compile(r'[^\d\W]', re.UNICODE)
    self.word_cont_re = re.compile(r'\w', re.UNICODE)

  @property
  def next_char(self):
    self.pos += 1
    if self.pos >= len(self.content):
      raise EOF()
    return self.content[self.pos]

  @property
  def current_char(self):
    return self.content[self.pos]

  def peek(self):
    return self.content[self.pos + 1]

  def skip_whitespace(self):
    while self.current_char.isspace():
      self.next_char

  def _parse_word(self):
    if not self.word_start_re.match(self.current_char):
      raise Exception('Invalid start of identifier: %c' % self.current_char)
    w = ''
    while True:
      w += self.current_char
      c = self.next_char
      if not self.word_cont_re.match(c):
        return w

  def _parse_string(self):
    end_str = self.current_char
    while True:
      c = self.next_char
      if c == '\n':
        raise Exception('Unterminated string literal')
      if c == end_str:
        self.next_char
        return
      elif c == '\\':
        self.next_char

  def _next_token(self):
    token_starts = '+*/-=%<>&^|'
    while True:
      self.skip_whitespace()
      if self.word_start_re.match(self.current_char):
        word = self._parse_word()
        print word
      elif self.current_char in ['"', "'"]:
        self._parse_string()
      elif self.current_char in token_starts:
        token = self.parse_token()
        print token
      else:
        self.next_char
