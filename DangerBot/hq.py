import os
import sys

import time

class HQ():
  def __init__(self, logfile, verbose):
    self.logfile = open(logfile, 'a')
    self.verbose = verbose

  def log(self, msg, exception=None):
    if msg.count("[+]") or msg.count("[-]") or msg.count("[*]") or msg.count("[~]") or self.verbose:
      print msg
    if exception:
      self.logfile.write(time.asctime(time.gmtime()) + " " + msg + " error({0}): {1}".format(exception.errno, exception.strerror) + "\n")
    else:
      self.logfile.write(time.asctime(time.gmtime()) + " " + msg + "\n")


