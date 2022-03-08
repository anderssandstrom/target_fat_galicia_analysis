#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
from datetime import datetime

class caMonitorArrayParser:
  def __init__(self):
    self.timeLowLimit = 0
    self.timeHighLimit = 0
    self.timeLowLimtSet = 0
    self.timeHighLimtSet = 0
    self.lastTimestamp = 0
    self.lastTimeStampSet = 0
    return

  def lineValid(self, line):
    # Two cases..
    # 1. Normal: TARGET_DU:Rotation-Brk-Temp1-Act-Slow 2019-05-24 12:08:02.763000 28.8   
    # 2. Undefined timetsamp: TARGET_DU:Rotation-Brk-Torque-Cmd <undefined> 56.9986 
    # for case two then use last valid time stamp (for any other PV)

    if len(line.split()) == 3: 
      pos1=line.rfind('<undefined>')
      if pos1<=0 or not self.lastTimeStampSet:
        print ("Ignoring line: " + line + " (Undefined timestamp and no fallback timestamp set).")
        return 0
      print("Warning: Time stamp undefined. Using last valid timestamp (" +line +").")
      return 1 

    pos1=line.rfind(':')
    if pos1<0:      
      print("Ignoring line: " + line + " (Missing timestamp \":\").")
      return 0

    if(line.count('-')<2):
      print("Ignoring line: " + line + " (Missing timestamp \":\").")
      return 0

    if(line.count(':')<2):
      print("Ignoring line: " + line + " (Missing timestamp \":\").")
      return 0
    
    pos1=line.rfind('Not connected')
    if pos1>=0:
      print("Ignoring line: " + line + " (\"Not connected\").")
      return 0

    pos1=line.rfind('*')
    if pos1>=0:
      print("Ignoring line: " + line + " (Invalid char \"*\").")
      return 0

    if len(line.split()) < 4: 
      print("Ignoring line: " + line + " (not three columns")
      return 0

    #Check time low limit
    if self.timeLowLimtSet:
      mylist=line.split()      
      timeString=mylist[1]+" "+mylist[2]
      timeVal=self.getTimeFromString(str(timeString))
      if timeVal < self.timeLowLimit:
        #print "Ignoring line: Data point low time limit."
        return 0

    #Check time high limit
    if self.timeHighLimtSet:
      mylist=line.split()      
      timeString=mylist[1]+" "+mylist[2]
      timeVal=self.getTimeFromString(str(timeString))
      if timeVal > self.timeHighLimit:
        #print "Ignoring line: Data point high time limit."
        return 0
  
    # Line OK
    return 1

  def setLowTimeLimit(self,timeLimitStr):
    if len(timeLimitStr)==0:
      print("Warning: invalid time limit: " + timeLimitStr)
      return
    self.timeLowLimit=self.getTimeFromString(timeLimitStr)
    self.timeLowLimtSet = 1

  def setHighTimeLimit(self,timeLimitStr):
    if len(timeLimitStr)==0:
      print("Warning: invalid time limit: " + timeLimitStr)
      return
    self.timeHighLimit=self.getTimeFromString(timeLimitStr)
    self.timeHighLimtSet = 1

  def getTimeFromString(self,line):

    pos1=line.rfind(".")
    if len(line)-pos1 >= 6:
      line=line[:-3]

    return datetime.strptime(line,"%Y-%m-%d %H:%M:%S.%f") 

  def getValues(self,line):    
    mylist=line.split()
    
    #use last timestamp if "undefined" timestamp    
    if len(line.split()) == 3: 
      pos1=line.rfind('<undefined>')
      if(pos1>=0):
        timeVal=self.lastTimestamp
        data = np.array(mylist[2])
    elif len(line.split()) == 4: 
        timeString=mylist[1]+" "+mylist[2]
        timeVal=self.getTimeFromString(str(timeString))
        self.lastTimestamp = timeVal
        self.lastTimeStampSet = 1
        data = np.array(mylist[3])        
    else:        #Array
      timeString=mylist[1]+" "+mylist[2]
      timeVal=self.getTimeFromString(str(timeString))
      self.lastTimestamp = timeVal
      self.lastTimeStampSet = 1
      data = np.array(mylist[4:])      
    
    pvName=mylist[0]
    return pvName, timeVal, data

  def checkModuloAndPrintOut(self,line,modulofactor):
    mylist=line.split()
    data = np.array(mylist[3])
    if self.firstscan:
        self.lastValue = data
        self.firstscan = 0

    if self.lastValue-data > 0.75 * modulofactor:
        self.turns = self.turns + 1

    if data-self.lastValue > 0.75 * modulofactor:
        self.turns = self.turns - 1
    data = data + self.turns * modulofactor

    # print new string to std out
    print(mylist[0:2] + data.str())