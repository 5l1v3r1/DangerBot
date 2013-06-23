import os
import sys

from DangerBot.carrier import Ident, Config
from DangerBot.pilot import Pilot
from DangerBot.hq import HQ
from DangerBot.engine import Engine


def main():
  f = open(".pass", "r")
  password = f.readline()
  ident = Ident("DangerBeta", None, "DangerBot IRC Bot", "Goooose!!!") # nick, pass, real, quit
  channels = ["#bots"]

  config = Config("irc.hackthissite.org", 7000, True, 1, ident, channels)  # server, port, ssl?, reconnects, ident, channels, srv_pass, bnc?
  hq = HQ("output.txt", True)  # logfile, verbose?

  pilot = Pilot(config, hq)

  engine = Engine(pilot)

  engine.start()



if __name__ == "__main__":
  main()


