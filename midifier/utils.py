import struct

def _int_to_bytes(num, num_bytes):
  '''Takes an integer, returns a 4-byte string representing it'''
  format_str = {
      1: '>B', 2: '>H', 4: '>I', 8: '>Q'}[num_bytes] 
  return struct.pack(format_str, num)

