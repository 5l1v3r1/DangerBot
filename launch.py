import os
import sys

from DangerBot.carrier import Ident, Config
from DangerBot.pilot import Pilot
from DangerBot.hq import HQ
from DangerBot.engine import Engine


def main():
  f = open(".pass", "r")
  password = f.readline()
  ident = Ident("DangerBot", password, "DangerBot IRC Bot", "Goooose!!!") # nick, pass, real, quit
  channels = ["#coffeesh0p", "#bots"]

  config = Config("funstuff.tk", 8888, True, 1, ident, channels, srv_pass="jaksod", bnc=True)  # server, port, ssl?, reconnects, ident, channels, server pass
  hq = HQ("output.txt", True)  # logfile, verbose?

  pilot = Pilot(config, hq)

  engine = Engine(pilot)

  engine.start()



if __name__ == "__main__":
  main()


