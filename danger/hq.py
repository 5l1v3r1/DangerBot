import os
import sys

class hq():
  def __init__(self, logfile, verbose):
    self.logfile = open(logfile, 'a')
    self.verbose = verbose

  def log(self, msg, exception):
    self.logfile.write(gmtime + " " + msg)
    

