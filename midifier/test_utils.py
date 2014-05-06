import utils
import unittest

class BytesTest(unittest.TestCase):

  def test_bytes(self):
    self.assertEqual('\x0d\x0e\xdb', utils._int_to_bytes(0x0d0edb, 3))

if __name__ == '__main__':
  unittest.main()
