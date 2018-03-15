#!/usr/bin/python

import sys
import os
import commands
from time import strftime, localtime

def get_size(dumpname):
 cmd = 'du -sh ' + dumpname
 (status, output) = commands.getstatusoutput(cmd)
 if status:
   sys.stderr.write(output)
   sys.exit(status)
 return output
    
def dump_db(database, user, dumpname):
  cmd = 'pg_dump ' + database + ' -Z6 -U ' + user + ' -f ' + dumpname
  print 'dumping:', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print 'dump created: ' + get_size(dumpname)
    
def clean_old_dumps(days, dumpdir, namebase):
  cmd = "find " + dumpdir + " -maxdepth 1 -mtime +" + str(days) + " -name \"" + namebase + "*.gz\" -exec rm -rf '{}' ';'"
  print 'removing:', cmd  
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)

def get_time_name(time):
  return strftime("%Y-%m-%d_%H_%M_%S", time)  

def num(s):
  try:
    return int(s)
  except ValueError:
    return 0

def main():
  args = sys.argv[1:]
  if not args:
    print "usage: [--dumpdir dir] [--clean days] database user";
    print "e.g. ./db_backup.py --dumpdir . operatus jboss_user";
    sys.exit(1)
  
  dumpdir = '/tmp'
  if args[0] == '--dumpdir':
    dumpdir = args[1]
    del args[0:2]
  
  clean = 0
  if len(args) > 1 and args[0] == '--clean':
    clean = num(args[1])
    del args[0:2]
  
  if len(args) < 2:
    print "error: must specify database and user"
    sys.exit(1)

  database = args[0]
  user = args[1]
  namebase = 'dump_' + database + '_'  
  dumpname = os.path.join(dumpdir, namebase + get_time_name(localtime()) + '.sql.gz')

  dump_db(database, user, dumpname)

  if clean:
    print "Removing dumps made before (days):", clean
    clean_old_dumps(clean, dumpdir, namebase)

if __name__ == "__main__":
  main()
