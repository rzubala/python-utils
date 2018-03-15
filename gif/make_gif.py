#!/usr/bin/env python

import sys
import os
import commands

def make_gif(input_f, output_f, fps):
  tmp = os.path.join('.', 'tmp');
  if not os.path.exists(tmp):
    os.mkdir(tmp)
  to_jpg(tmp, input_f, fps)  
  to_gif(tmp, output_f, fps)  
  clean(tmp)  

def to_jpg(tmp, input_f, fps):
  cmd = 'ffmpeg -i ' + input_f + ' -r ' + str(fps) + ' ' + os.path.join(tmp, 'f%04d.jpg')  
  print 'dumping:', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output

def to_gif(tmp, output_f, fps):
  cmd = 'convert -delay ' + str(100/fps) + ' -loop 0 '  + os.path.join(tmp, '*.jpg') + ' ' + output_f
  print 'creating gif:', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output

def clean(tmp):
  cmd = 'rm -rf '+ tmp
  print 'cleaning:', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output

def num(s):
  try:
    return int(s)
  except ValueError:
    return 0

def main():
  args = sys.argv[1:]
  if not args:
    print "usage: output.gif input.mp4 [--fps fps]";
    sys.exit(1)
  
  if len(args) < 2:
    print "error: must specify output.gif and imput.mp4"
    sys.exit(1)
  
  output_f = args[0]
  del args[0]
  input_f = args[0]
  del args[0]

  fps = 5
  if len(args) > 1 and args[0] == '--fps':
    fps = num(args[1])
    if fps == 0:
      fps = 5
    del args[0:2]

  print 'Converting',input_f,'to',output_f,'with',fps,'fps'
  make_gif(input_f, output_f, fps)

if __name__ == "__main__":
  main()
