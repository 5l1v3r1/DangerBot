import os
import sys


class Config():
  def __init__(self, server, port, ssl, retry, ident, channels, srv_pass=None, bnc=False):
    self.server = server
    self.port = port
    self.ssl = ssl
    self.retry = retry
    self.ident = ident
    self.channels = channels
    self.srv_pass = srv_pass
    self.bnc = bnc


class Ident():
  def __init__(self, nick, password, realname, quit):
    self.nick = nick
    self.password = password
    self.realname = realname
    self.quit = quit

