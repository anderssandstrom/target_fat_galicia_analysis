#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python slask.py")
  print ("Custom plot for target rotor displacement sensors: cat *.log | slask.py")

def main():
  # Check args
  if len(sys.argv)>1:    
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()

  scale=1.0  # default

  if len(sys.argv)==2:      
     scale=float(sys.argv[1])

  pvY1name = "Torque"
  pvY2name = "Max"
  pvY3name = "Min"
  
  dataFile=sys.stdin

  parser = caMonitorArrayParser()
  pvY1   = caPVArray(pvY1name)
  pvY2   = caPVArray(pvY2name)
  pvY3   = caPVArray(pvY2name)
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    if line.find(pvY1name)==-1 and line.find(pvY2name)==-1 and line.find(pvY3name)==-1:
      continue

    pvName, timeVal, data = parser.getValues(line)
    
    if pvName.find(pvY1name)>=0:
       pvY1.setValues(timeVal,data)

    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)

    if pvName.find(pvY3name)>=0:
       pvY3.setValues(timeVal,data)

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()
  y3Time,y3Data = pvY3.getData()
 
  legstr=[]
  legstr.append("Torque")
  fig2=plt.figure(2)
  ax1=fig2.add_subplot(2, 1, 1)
  ax1.plot(y1Time,y1Data, 'b')
  ax1.set_ylabel("Torque [Nm]")
  ax1.legend(legstr)
  ax1.set_ylim(100,180)
  ax1.grid()
  
  legstr=[]
  legstr.append("Velocity Max")
  legstr.append("Velocity Min")
  ax2=fig2.add_subplot(2, 1, 2)
  ax2.plot(y2Time,y2Data, 'm')
  ax2.plot(y3Time,y3Data, 'b')
  ax2.set_ylabel("Velocity [rpm]")
  ax2.legend(legstr)
  ax2.set_ylim(23.5,24.5)
  ax2.grid()

  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
