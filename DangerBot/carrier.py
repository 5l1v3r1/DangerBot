import os
import sys


class Config():
  def __init__(self, server, port, ssl, retry, ident, channels):
    self.server = server
    self.port = port
    self.ssl = ssl
    self.retry = retry
    self.ident = ident
    self.channels = channels


class Ident():
  def __init__(self, nick, password, realname, quit):
    self.nick = nick
    self.password = password
    self.realname = realname
    self.quit = quit

