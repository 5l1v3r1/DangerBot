import os
import sys

from stats import Stats
from utils import Utilities

import md5
import urllib2
import re
import json


class Pilot():
  def __init__(self, config, hq):
    self.config = config
    self.ident = config.ident
    self.hq = hq
    self.state = 0
    self.perm8_state = 0
    self.stats = Stats(config, hq)
    self.utils = Utilities()


  def parse(self, line):
    response = ""
    msg = line.split(':')
    if self.state == 0: # Just connected.
      if len(msg) > 2 and msg[1].count("376"): # End of MOTD
        if self.ident.password and not self.config.bnc: # If we need to identify.
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
      if not self.config.bnc:
        for chan in self.config.channels:
          response += "JOIN " + chan + "\r\n"
          self.hq.log("[+] Joining " + chan)
      self.state = 3

    elif self.state == 3:
      if len(msg) > 2:
        msg[2] = msg[2].strip("\r")
        self.hq.log(msg[1])
        m = re.search("^:(\w+)!(.+) (\w+) (.+) :(.+)$", line)
        if m:
          nick = m.group(1)
          host = m.group(2)
          msgtyp = m.group(3)
          chan = m.group(4)
          message = m.group(5)
          if chan.count(self.ident.nick):
            recip = nick
          else:
            recip = chan
          response = self.process(nick, host, msgtyp, recip, message)

        else:
          m = re.search("^.+ (.+) $", msg[1])
          chan = m.group(1)
        if msg[1].count("366"):
          self.stats.join(chan)
        elif msg[1].count("KICK"):
          self.stats.leave(chan)
          response = "JOIN " + chan + "\r\n"
          
    return response


  def process(self, nick, host, msgtype, recip, message):
    
    self.hq.log("[~] " + message)
    responses = []
    response = ""
    if message.count(self.ident.nick):
      for util in self.utils.functions():
        if message.count(util):
          print "[*] It's a utility"
          responses = self.utils.execute(message)
          response = self.privMsg(recip, responses)
          self.stats.count(util)
          break
      if message.count("stats"):
        print "[*] Stat!"
        stats = self.stats.getStats()
        self.stats.count("stats")
        response = self.privMsg(recip, stats)
      elif message.count("goose"):
        response = "QUIT :" + self.ident.quit + "\r\n"

    print response
    return response


  def getState(self):
    self.hq.log("Self.state: " + str(self.state))
    return
  
  def privMsg(self, recip, msgs):
    response = ""
    for msg in msgs:
      response += "PRIVMSG " + recip + " :" + msg + "\r\n"
    return response
