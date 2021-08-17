#  python coordstoland.py -i test1.txt -o test2.txt
from global_land_mask import globe
# import numpy as np
import argparse
import os.path

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  # parser.add_argument("-i", type=argparse.FileType('r'))
  # parser.add_argument("-o", "filename", required=True,
  #   help="input file with two matrices", metavar="FILE")
  parser.add_argument(
        '--input', '-i', type=argparse.FileType('r'),  metavar='PATH',
        help="Input file (default: standard input).")
  parser.add_argument(
        '--output', '-o', type=argparse.FileType('w'), metavar='PATH',
        help="Output file (default: standard output)")
  args = parser.parse_args()

  sourcefile = "test1.txt"
  destfile = "test2.txt"

  # print(args.file.readlines())

  def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

  # print(args.input)

  with args.input as ifile:
  # f = open(sourcefile, "r")
    flines = ifile.read().split("\n")
    outputList = []
    # print(flines)
    for i in flines:
      outputList.append(eval(i))

  for i in outputList:
    land = globe.is_land(i[1],i[0])
    # print('lat={}, lon={} is on land: {}'.format(i[0],i[1],land))
    print('{}'.format(land), file = args.output)

  # print(outputList)
  args.input.close()
  args.output.close()

  print("done")

  
  # # destFile = open('ledcoords_land2.txt', 'w')

  # for i in outputList:
  #   # pointlong1 = (i[1] + 180) % 360 - 180
  #   land = globe.is_land(i[0],i[1])
  #   print('lat={}, lon={} is on land: {}'.format(i[0],i[1],land))
    
  #   print('{},{},{}'.format(i[0],i[1],land), file = file)

  