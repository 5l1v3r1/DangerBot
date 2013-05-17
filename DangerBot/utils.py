import os
import sys

import re
import md5
import urllib2
import json


class Utilities():
  def __init__(self):
    return
  
  def functions(self):
    functions = ["btc", "md5", "time", "insult", "curse"]
    print "Utilities.functions() called."
    return functions

  def execute(self, msg):
    response = []
    if msg.count("btc"):
      response.append(self.getBTC())

    elif msg.count("md5"):
      response.append(self.md5hash(msg))

    elif msg.count("time"):
      response.append("http://i.imgur.com/CfNS0uY.gif")
    
    elif msg.count("insult"):
      m = re.search("insult (.+)$", msg)
      if m:
        response.append(m.group(1) + ", " + self.getInsult())
      else:
        response.append(self.getInsult())

    return response


  def getBTC(self):
    response = ""
    mtgox = urllib2.urlopen("http://data.mtgox.com/api/2/BTCUSD/money/ticker")

    data = json.load(mtgox)

    response += "Last: $" + str(data['data']['last']['value']) + ", "
    response += "High: $" + str(data['data']['high']['value']) + ", "
    response += "Low: $" + str(data['data']['low']['value']) + ", "
    response += "Weighted Avg: $" + str(data['data']['avg']['value']) + ". Retrieved from MT.Gox"
   
    return response


  def md5hash(self, msg):
    m = re.search("md5 (.+)", msg[2])
    if m:
      hash = md5.new(m.group(1).strip("\r"))
      response = hash.hexdigest()
    else:
      response = "Input invalid."
    return response


  def getInsult(self):
    insult = urllib2.urlopen("http://www.randominsults.net/")
    while 1:
      line = insult.readline()
      if line.count("<font face=\"Verdana\" size=\"4\"><strong><i>"):
        m = re.search("<font face=\"Verdana\" size=\"4\"><strong><i>(.+)</i>", line)
        response = m.group(1)
        break
    return response

