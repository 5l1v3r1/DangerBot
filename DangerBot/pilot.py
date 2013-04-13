import os
import sys

import md5


class Pilot():
  def __init__(self, config, hq):
    self.config = config
    self.ident = config.ident
    self.hq = hq
    self.state = 0
    self.perm8_state = 0
    
  def parse(self, line):
    response = ""
    msg = line.split(':')
    
    if self.state == 0: # Just connected.
      if len(msg) > 2 and msg[1].count("376"): # End of MOTD
        if self.ident.password: # If we need to identify.
          self.state = 1
        else:
          self.state = 2

    elif self.state == 1:
      if len(msg) > 2 and msg[2].count("registered and protected"):
        response = "PRIVMSG nickserv :identify " + self.ident.password + "\r\n"
        self.hq.log("[+] Identifying with NickServ")
      if len(msg) > 2 and msg[2].count("recognized"): # Authenticated successfully.
        self.state = 2

    elif self.state == 2:
      for chan in self.config.channels:
        response += "JOIN " + chan + "\r\n"
        self.hq.log("[+] Joining " + chan)
      self.state = 3

    elif self.state == 3:
      if msg[1].count("366"): # End of /names list.
        self.state = 4

    elif self.state == 4:
      for chan in self.config.channels:
        response = "PRIVMSG " + chan + " :Highway to the DANGER ZONE!\r\n"
      self.state = 5

    elif self.state == 5:
      if self.perm8_state:
        response = self.perm8(msg)

      if len(msg) > 2 and msg[2].count("!eject"):
        response = "QUIT :" + self.ident.quit + "\r\n"
        # Exit script here.

      elif len(msg) > 2 and msg[2].count("!perm8") and not msg[2].count("!perm8-attack"):
        response = "NOTICE moo :!perm8\r\n"
        self.perm8_state = 1


    return response

  def perm8(self, msg):
    response = ""

    if self.perm8_state == 1:
      if len(msg) > 2 and msg[2].count("!md5"):
        perm8 = msg[2].split(" ")
        perm8.pop(0)
        string = " ".join(perm8)
        string = string.replace("\r", "")
        string = string.replace("\n", "")
        self.hq.log(string)
        hash = md5.new(string)
        perm8_result = hash.hexdigest()
        response = "NOTICE moo :!perm8-result " + perm8_result + "\r\n"
        self.perm8_state = 2

    elif self.perm8_state == 2:
      if len(msg) > 2 and msg[2].count("VERSION"):
        response = "NOTICE moo :\001VERSION DangerBot:1.0:MiG-28\001\r\n"
        self.perm8_state = 3
    
    elif self.perm8_state == 3:
      if len(msg) > 2 and msg[2].count("!perm8-attack"):
        response = "JOIN #takeoverz\r\n"
        self.perm8_state = 4

    elif self.perm8_state == 4:
      if len(msg) > 2 and msg[1].count("366"):
        response += "KICK #takeoverz moo :SUCK MY DICK\r\n"


    return response
