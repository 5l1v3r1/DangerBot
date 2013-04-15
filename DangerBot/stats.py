import os
import sys

class Stats():
  def __init__(self, config, hq):
    self.config = config
    self.hq = hq
    self.channels = {}
    for chan in self.config.channels:
      self.channels[chan] = False # Not connected yet.

  def join(self, chan):
    self.channels[chan] = True

  def getStats(self):
    response = "Currently in the following channels: "
    for chan in self.config.channels:
      if self.channels[chan]:
        response += chan + " "
    return response
