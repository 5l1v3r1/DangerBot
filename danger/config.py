import os
import sys

class config():
  def __init__(self, server, port, ssl, retry, ident, channels):
    self.server = server
    self.port = port
    self.ssl = ssl
    self.retry = retry
    self.ident = ident
    self.channels = channels


