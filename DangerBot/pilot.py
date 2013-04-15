import os
import sys

import md5
import urllib2
import re


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
    
    if self.state == 0 and self.config.bnc:
      self.state = 2

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
      if msg[1].count("366") and msg[1].count("#bots"): # End of /names list.
        self.state = 4

    elif self.state == 4:
      # for chan in self.config.channels:
      response = "PRIVMSG #bots :Highway to the DANGER ZONE!\r\n"
      self.state = 5

    elif self.state == 5:
      if len(msg) > 2 and msg[1].count("366"):
        self.state = 6

    elif self.state == 6:
      if len(msg) > 2:
        self.hq.log(msg[1])
        m = re.search("(\w+) (#.+) ", msg[1])
        if m:
          sender = m.group(1)
          chan = m.group(2)  
          if not chan:
            recip = sender
          else:
            recip = chan

        if msg[2].count("!btc"):
          response = "PRIVMSG " + recip + " :" + self.getBTC() + "\r\n"

        if msg[2].count("!md5"):
          response = "PRIVMSG " + recip + " :" + self.md5hash(msg) + "\r\n"

      # if self.perm8_state:
        # response = self.perm8(msg)

      # if len(msg) > 2 and msg[2].count("!eject"):
        # response = "QUIT :" + self.ident.quit + "\r\n"
        # Exit script here.

      # elif len(msg) > 2 and msg[2].count("!perm8") and not msg[2].count("!perm8-attack"):
        # response = "NOTICE moo :!perm8\r\n"
        # self.perm8_state = 1

    return response


  def getBTC(self):
    response = ""
    mtgox = urllib2.urlopen("https://mtgox.com/")
    while 1:
      line = mtgox.readline()
      if line.count("Last price:"):
        #self.hq.log(line)
        m = re.search("<span>(.+)</span>", line)
        response += "Last: " + m.group(1) + ", "
      if line.count("High:"):
        m = re.search("<span>(.+)</span>", line)
        response += "High: " + m.group(1) + ", "
      if line.count("Low:"):
        m = re.search("<span>(.+)</span>", line)
        response += "Low: " + m.group(1) + ", "
      if line.count("Weighted Avg:"):
        m = re.search("<span>(.+)</span>", line)
        response += "Weighted Avg: " + m.group(1) + ". Retrieved from MT.Gox"
        break
    return response

  def md5hash(self, msg):
    m = re.search("!md5 (.+)", msg[2])
    if m:
      hash = md5.new(m.group(1).strip("\r"))
      response = hash.hexdigest()
    else:
      response = "Input invalid."
    return response



  def getState(self):
    self.hq.log("Self.state: " + str(self.state) + 
                "\nSelf.perm8_state: " + str(self.perm8_state))
  
  
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
