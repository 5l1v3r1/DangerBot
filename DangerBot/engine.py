import os
import sys

import socket
import ssl

# This class takes care of the connection to the IRC server.
# Basic error handling
class Engine():
  def __init__(self, pilot):
    self.config = pilot.config  # Configuration class for the connection.
    self.hq = pilot.hq
    self.pilot = pilot
    self.hq.log("[+] Engine initialised.")

    # Shortcut variables for server and port even though they are already in config.
    self.server = self.config.server
    self.port = self.config.port
    self.nick = self.config.ident.nick

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if self.config.ssl:
      self.hq.log("[*] SSL Enabled.")
      self.socket = ssl.wrap_socket(self.socket)

  def connect(self):
    self.hq.log("[+] Attempting to connect.")
    retry = self.config.retry + 1 # If retry is set to 0, we want to still connect at least once.
    while retry:
      print "[*] Trying connection."
      try:
        self.socket.connect((self.server, self.port))
        return
      except socket.timeout, e:
        self.hq.log("[-] Connection timeout.", e)
        retry -= 1 # Decrement retries for each fail.
      except Exception, e:
        self.hq.log("[-] Connection error.", e) # Catch all other errors.
        return

    self.hq.log("[-] Unable to connect! Attempted to reconnect " + self.config.retry + " times.")

  def start(self):
    self.hq.log("[+] Starting Engine")
    self.connect()
    
    if not self.config.srv_pass:
      while(1):
        a = self.socket.recv(512)
        a.strip("\r")
        b = a.split("\n")
        for msg in b:
          self.hq.log("IN: " + msg)
        if a.count("Found"):
          break

    self.hq.log("[+] Sending auth info.")
    self.hq.log('NICK ' + self.nick + '\r\n')
    self.socket.send('NICK ' + self.nick + '\r\n')

    self.hq.log('USER ' + self.nick + ' ' + self.server + ' ' +
                'NAME :' + self.config.ident.realname + '\r\n')
    self.socket.send('USER ' + self.nick + ' ' + self.server + ' ' +
                     'NAME :' + self.config.ident.realname + '\r\n')
    
    if self.config.srv_pass:
      self.hq.log("[+] Sending server password.")
      self.socket.send('PASS ' + self.nick + ':' + self.config.srv_pass + '\r\n')

    buf = ""  # Used for message pump.              
    while 1:
      recvd = self.socket.recv(512)
      lines = recvd.split('\n')
      lines[0] = buf + lines[0] # If buffer contains anything, prepend it with the first line.
      last = len(lines)
      last -= 1
      if not lines[last].count('\r'): #Check to see if we should add the last line to the buffer (incomplete).
        buf = lines.pop()
      
      # Now, we go through each line received.
      for line in lines:
        msg = line.split(':')
        if msg[0].count("PING"):
          self.hq.log("[*] PONG :" + msg[1])
          self.socket.send('PONG :' + msg[1] + '\r\n')
          self.pilot.getState()
        else:
          self.hq.log("IN: " + line)
          
          response = self.pilot.parse(line)
          if response and response != "":
            try:
              self.socket.send(response)
              self.hq.log("OUT: " + response)
            except Exception, e:
              self.hq.log("Error sending to socket: " + response, e)

