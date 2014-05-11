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
  FUNCTION_START = 'fs'
  FUNCTION_END = 'fe'
  ASSIGNMENT = 'a'
  OTHER_KEYWORD = 'ok'
  INVALID_SOURCE = 'is'


class Parser(object):
  def __init__(self, content):
    self.content = content
    self.pos = 0
    self.scope_depth = 0
    self.word_start_re = re.compile(r'[^\d\W]', re.UNICODE)
    self.word_cont_re = re.compile(r'\w', re.UNICODE)
    self.line_no = 1
    self.num_open_braces = 0

  @property
  def is_eof(self):
    return self.pos >= len(self.content)

  def next_char(self):
    self.pos += 1
    if self.is_eof:
      raise EOF()
    if self.content[self.pos] == '\n':
      self.line_no += 1
    return self.content[self.pos]

  @property
  def current_char(self):
    return self.content[self.pos]

  def peek(self):
    return self.content[self.pos + 1]

  def skip_whitespace(self):
    while self.current_char.isspace():
      self.next_char()

  def _parse_word(self):
    if not self.word_start_re.match(self.current_char):
      raise Exception('Invalid start of identifier: %c' % self.current_char)
    w = ''
    while True:
      w += self.current_char
      c = self.next_char()
      if not self.word_cont_re.match(c):
        return w

  def _parse_string(self):
    end_str = self.current_char
    while True:
      c = self.next_char()
      if c == '\n':
        raise Exception('Unterminated string literal')
      if c == end_str:
        self.next_char()
        return
      elif c == '\\':
        self.next_char()

  def _parse_line_comment(self):
    assert self.current_char == '/'
    self.next_char()
    while self.current_char != '\n':
      self.next_char()

  def _parse_block_comment(self):
    assert self.current_char == '*'
    self.next_char()
    while True:
      if self.current_char == '*' and self.peek() == '/':
        self.next_char()
        self.next_char()
        return
      self.next_char()

  def _parse_comment(self):
    assert self.current_char == '/'
    assert self.peek() in '/*'
    c = self.next_char()
    if c == '/':
      self._parse_line_comment()
    else:
      self._parse_block_comment()

  def _parse_token(self):
    if self.current_char == '/':
      if self.peek() in '/*':
        self._parse_comment()
        return ''
    w = self.current_char
    self.next_char()
    while self.current_char in '+*/-%<>&^|=':
      w += self.current_char
      self.next_char()
    return w

  def next_token(self):
    if self.is_eof:
      return None

    try:
      return self._next_token()
    except EOF:
      if self.scope_depth:
        return Events.INVALID_SOURCE
      return None
    except Exception as e:
      import traceback
      traceback.print_exc()
      return Events.INVALID_SOURCE

  def _next_token(self):
    token_starts = '+*/-=%<>&^|!'
    keywords = ['if', 'else', 'for', 'while', 'do', 'try', 'catch', 'finally', 'switch', 'with']
    assignment_operators = ['+=', '*=', '/=', '-=', '=', '%=', '<<=', '>>=', '>>>=', '&=', '^=', '|=']
    while True:
      self.skip_whitespace()
      if self.word_start_re.match(self.current_char):
        word = self._parse_word()
        if word == 'function':
          self.scope_depth += 1
          return Events.FUNCTION_START
        elif word in keywords:
          return Events.OTHER_KEYWORD
      elif self.current_char in ['"', "'"]:
        self._parse_string()
      elif self.current_char in token_starts:
        token = self._parse_token()
        if token in assignment_operators:
          return Events.ASSIGNMENT
      elif self.current_char == '{':
        self.num_open_braces += 1
        self.next_char()
      elif self.current_char == '}':
        try:
          self.next_char()
        except EOF:
          # catch it later
          pass

        return_end = False
        if self.num_open_braces == self.scope_depth:
          self.scope_depth -= 1
          return_end = True
        self.num_open_braces -= 1
        if self.num_open_braces < 0:
          return Events.INVALID_SOURCE

        if return_end:
          return Events.FUNCTION_END
      else:
        self.next_char()
