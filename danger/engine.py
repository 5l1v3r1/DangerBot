import os
import sys

import socket

# This class takes care of the connection to the IRC server.
# Basic error handling
class engine():
  def __init__(self, config, hq, pilot):
    self.config = config  # Configuration class for the connection.
    self.hq = hq
    self.pilot = pilot

    # Shortcut variables for server and port even though they are already in config.
    self.server = config.server
    self.port = config.port
    self.nick = config.ident.nick

    self.socket = socket.socket()

  def connect(self):
    while self.config.retry:
      try:
        self.socket.create_connection((self.server, self.port), timeout=15)
        if self.config.ssl:
          self.socket = socket.ssl(self.socket)
        return

      except socket.timeout, e:
        self.hq.log("Connection timeout.", e)
          self.config.retry -= 1 # Decrement retries for each fail.

      except Exception, e:
        self.hq.log("Connection error.", e) # Catch all other errors.
        return

  def start(self):
    self.connect()
    self.socket.send('NICK ' + self.nick + '\r\n')
    self.socket.send('USER ' + self.nick + ' ' + self.server + 
                         ' NAME :' + self.config.realname + '\r\n')

    buf = ""  # Used for message pump.              
    while 1:
      recvd = self.socket.recv(5000)
      lines = recvd.split('\n')
      lines[0] = buf + lines[0] # If buffer is full prepend with next line.
      last = len(lines)
      last -= 1
      if not lines[last].count('\r'):
        buf = lines.pop()
      for line in lines:
        self.hq.log("IN: " + line)
        msg = line.split(':')
        if msg[0].count("PING"):
          self.socket.send('PONG :' + msg[1] + '\r\n')
        else:
          response = pilot.parse(line)
          self.socket.send(response)

