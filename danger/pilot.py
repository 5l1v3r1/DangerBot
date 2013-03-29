import os
import sys

class pilot():
  def __init__(self, config, hq):
    self.ident = config
    self.hq = hq
    self.state = 0
    
  def parse(self, line):
    if self.state == 0: # Just connected.
      msg = line.split(':')
      if len(msg) > 2 and msg[2].count("End of /MOTD command."):
        response = "JOIN #bots\r\n"
        self.state = 1

    if self.state == 1:
      response = "PRIVMSG #bots :Highway to the DANGER ZONE!\r\n"

    return reponse
