import os
import sys

import redis

class Stats():
  def __init__(self, config, hq):
    self.config = config
    self.hq = hq
    self.channels = {}
    for chan in config.channels:
      self.channels[chan] = False # Not connected yet.
    self.db = redis.Redis(host=config.db['host'], db=config.db['db'])

  def join(self, chan):
    self.channels[chan] = True

  def getStats(self):
    response = []
    response.append("Currently in the following channels: ")
    for chan in self.config.channels:
      if self.channels[chan]:
        response[0] += chan + ", "
    response[0].strip(', ')
    
    response.append("Command stats: ")
    for cmd in self.db.keys("command:*"):
      response[1] += cmd.replace("command:","") + ": " + str(self.db.get(cmd)) + ", "
    response[1] = response[1].strip(", ")
    return response

  def count(self, cmd):
    self.db.incr("command:"+cmd)

