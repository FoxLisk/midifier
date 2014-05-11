#!/usr/bin/env python
import argparse
from midifier import Midifier

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Listen to your JavaScript!')
  parser.add_argument('files', nargs='*')
  parser.add_argument('-o', '--output-file', dest='output_file', required=True)
  parser.add_argument('-u', '--unstable', action='store_true', default=False)
  args = parser.parse_args()
  print 'Midifying %s into %s' % (', '.join(args.files), args.output_file)
  midifier = Midifier(args.files, args.output_file, args.unstable)
  midifier.make_midi()
  midifier.save()
