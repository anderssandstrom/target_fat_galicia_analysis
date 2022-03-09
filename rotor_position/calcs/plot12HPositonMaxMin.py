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

  pvY1name = "Max"
  pvY2name = "Min"
    
  dataFile=sys.stdin

  parser = caMonitorArrayParser()
  pvY1   = caPVArray(pvY1name)
  pvY2   = caPVArray(pvY2name)
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    if line.find(pvY1name)==-1 and line.find(pvY2name)==-1:
      continue

    pvName, timeVal, data = parser.getValues(line)
    
    if pvName.find(pvY1name)>=0:
       pvY1.setValues(timeVal,data)

    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()

  y1Data = y1Data * scale
  y2Data = y2Data * scale

  y1DataAvg = np.mean(y1Data)
  y2DataAvg = np.mean(y2Data)
  
  diff=y1DataAvg-y2DataAvg

  # subtract avg
  y1Data = y1Data - y1DataAvg + diff / 2.0
  y2Data = y2Data - y2DataAvg - diff / 2.0
  
  print("statistics")

  pvLen = len(y1Data)
  pvMax = np.max(y1Data)
  pvMin = np.min(y1Data)
  pvAvg = np.mean(y1Data)
  pvStd = np.std(y1Data)
  legStr = pvY1name + "[" + str(pvLen) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  print (legStr)

  pvLen = len(y2Data)
  pvMax = np.max(y2Data)
  pvMin = np.min(y2Data)
  pvAvg = np.mean(y2Data)
  pvStd = np.std(y2Data)
  legStr = pvY2name + "[" + str(pvLen) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  print (legStr)

  fig2=plt.figure(2)
  ax1=fig2.add_subplot(2, 1, 1)
  ax1.plot(y1Time,y1Data, color='b')
  ax1.set_ylabel("position [mm]")  
  ax1.set_ylim(1, 2)
  ax1.grid()
  
  ax2=fig2.add_subplot(2, 1, 2)
  ax2.plot(y2Time,y2Data, color='g')
  ax2.set_ylabel("position [mm]")  
  ax2.set_ylim(-2, -1)
  ax2.grid()

  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
