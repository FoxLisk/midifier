import struct

def _int_to_bytes(num, num_bytes):
  '''Takes an integer, returns a 4-byte string representing it'''
  format_strs = {
      1: '>B', 2: '>H', 4: '>I', 8: '>Q'}
  if num_bytes in format_strs:
    return struct.pack(format_strs[num_bytes], num)

  if num >= 0xff**num_bytes:
    raise Exception("Can't pack %d into %d bytes" % (num, num_bytes))
  s = ''
  while num_bytes:
    num_bytes -= 1
    s = struct.pack('>B', num & 0xff) + s
    num >>= 8
  return s

