import unittest

from parser import Parser, Events

class ParserTest(unittest.TestCase):

  def test_scopes_end(self):
    #import pudb; pu.db
    p = Parser(' function() { if (1) { } else { } }')
    self.assertEqual(Events.FUNCTION_START, p._next_token())
    self.assertEqual(Events.OTHER_SCOPE_START, p._next_token())
    self.assertEqual(Events.OTHER_SCOPE_END, p._next_token())
    self.assertEqual(Events.OTHER_SCOPE_START, p._next_token())
    self.assertEqual(Events.OTHER_SCOPE_END, p._next_token())
    self.assertEqual(Events.FUNCTION_END, p._next_token())

  def test_strings(self):
    p = Parser('function() { "hello}" }')
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())
    self.assertEqual(None, p.next_token())

    p = Parser("function() { 'hello}' }")
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())
    self.assertEqual(None, p.next_token())

  def test_string_escape_quotes(self):
    p = Parser('f = function() { return "This is a close-brace: \\"}\\"." };')
    self.assertEqual(Events.ASSIGNMENT, p.next_token())
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())
    self.assertEqual(None, p.next_token())

  def test_assignments(self):
    for assignment in [
      '+=', '*=', '/=', '-=', '=', '%=', '<<=',
      '>>=', '>>>=', '&=', '^=', '|=']:
      p = Parser(' x %s 32' % assignment)
      self.assertEqual(Events.ASSIGNMENT, p.next_token())

    p = Parser('1 == 2')
    self.assertEqual(None, p.next_token())
    p = Parser('1 === 3')
    self.assertEqual(None, p.next_token())
    p = Parser('1 != 2')
    self.assertEqual(None, p.next_token())
    p = Parser('1 !== 3')
    self.assertEqual(None, p.next_token())

  def test_comments(self):
    p = Parser(''' a = 1; //a = 1
    function() {} ''')
    self.assertEqual(Events.ASSIGNMENT, p.next_token())
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())
    self.assertEqual(None, p.next_token())

    p = Parser(''' a = 1; /*
    fkljasdf
    asdfljaslkdjfasdjfas
    dfthis is all garbage *
    lets thro / in some random // stuff// around here
    let's also put in an assignemtn x = 1; function() blargh*/
    function() {}''')
    self.assertEqual(Events.ASSIGNMENT, p.next_token())
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())
    self.assertEqual(None, p.next_token())

  def test_objects(self):
    p = Parser(' function() { x = {} }; ')
    self.assertEqual(Events.FUNCTION_START, p.next_token())
    self.assertEqual(Events.ASSIGNMENT, p.next_token())
    self.assertEqual(Events.FUNCTION_END, p.next_token())

if __name__ == '__main__':
  unittest.main()
