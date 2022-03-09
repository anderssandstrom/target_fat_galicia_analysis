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

  pvY1name = "AI1Max"
  pvY2name = "AI2Max"
  pvY3name = "AI3Max"
  pvY4name = "ActMax"

  pvY5name = "AI1Min"
  pvY6name = "AI2Min"
  pvY7name = "AI3Min"
  pvY8name = "ActMin"

  dataFile=sys.stdin

  parser = caMonitorArrayParser()
  pvY1   = caPVArray(pvY1name)
  pvY2   = caPVArray(pvY2name)
  pvY3   = caPVArray(pvY3name)
  pvY4   = caPVArray(pvY4name)
  pvY5   = caPVArray(pvY5name)
  pvY6   = caPVArray(pvY6name)
  pvY7   = caPVArray(pvY7name)
  pvY8   = caPVArray(pvY8name)
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    if line.find(pvY1name)==-1 and line.find(pvY2name)==-1 and line.find(pvY3name)==-1 and line.find(pvY4name)==-1 and line.find(pvY5name)==-1 and line.find(pvY6name)==-1 and line.find(pvY7name)==-1 and line.find(pvY8name)==-1:
      continue

    pvName, timeVal, data = parser.getValues(line)
    
    if pvName.find(pvY1name)>=0:
       pvY1.setValues(timeVal,data)

    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)

    if pvName.find(pvY3name)>=0:
       pvY3.setValues(timeVal,data)

    if pvName.find(pvY4name)>=0:
       pvY4.setValues(timeVal,data)

    if pvName.find(pvY5name)>=0:
       pvY5.setValues(timeVal,data)

    if pvName.find(pvY6name)>=0:
       pvY6.setValues(timeVal,data)

    if pvName.find(pvY7name)>=0:
       pvY7.setValues(timeVal,data)

    if pvName.find(pvY8name)>=0:
       pvY8.setValues(timeVal,data)

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()
  y3Time,y3Data = pvY3.getData()
  y4Time,y4Data = pvY4.getData()
  y5Time,y5Data = pvY5.getData()
  y6Time,y6Data = pvY6.getData()
  y7Time,y7Data = pvY7.getData()
  y8Time,y8Data = pvY8.getData()

  # do not scale opto
  y1Data = y1Data * scale
  y2Data = y2Data * scale
  y3Data = y3Data * scale
  
  y5Data = y5Data * scale
  y6Data = y6Data * scale
  y7Data = y7Data * scale

  
  y1DataAvg = np.mean(y1Data)
  y2DataAvg = np.mean(y2Data)
  y3DataAvg = np.mean(y3Data)
  y4DataAvg = np.mean(y4Data)
  y5DataAvg = np.mean(y5Data)
  y6DataAvg = np.mean(y6Data)
  y7DataAvg = np.mean(y7Data)
  y8DataAvg = np.mean(y8Data)
  
  diff1=y1DataAvg-y5DataAvg
  diff2=y2DataAvg-y6DataAvg
  diff3=y3DataAvg-y7DataAvg
  diff4=y4DataAvg-y8DataAvg

  # subtract avg
  y1Data = y1Data - y1DataAvg + diff1 / 2.0
  y5Data = y5Data - y5DataAvg - diff1 / 2.0

  y2Data = y2Data - y2DataAvg + diff2 / 2.0
  y6Data = y6Data - y6DataAvg - diff2 / 2.0
  
  y3Data = y3Data - y3DataAvg + diff3 / 2.0
  y7Data = y7Data - y7DataAvg - diff3 / 2.0

  y4Data = y4Data - y4DataAvg + diff4 / 2.0
  y8Data = y8Data - y8DataAvg - diff4 / 2.0

  
  print("statistics")

  fig2=plt.figure(2)
  ax1=fig2.add_subplot(2, 1, 1)
  ax1.plot(y1Time,y1Data, color='b')
  ax1.plot(y2Time,y2Data, color='g')
  ax1.plot(y3Time,y3Data, color='m')
  ax1.plot(y4Time,y4Data, color='k')
  ax1.set_ylabel("position [mm]")
  ax1.set_ylim(1, 3)
  ax1.grid()  
  ax1.legend("Odeg", "120deg", "240deg")
  
  ax2=fig2.add_subplot(2, 1, 2)  
  ax2.plot(y5Time,y5Data, color='b')
  ax2.plot(y6Time,y6Data, color='g')
  ax2.plot(y7Time,y7Data, color='m')
  ax2.plot(y8Time,y8Data, color='k')
  ax2.set_ylabel("position [mm]")  
  ax2.set_ylim(-3, -1)
  ax2.grid()
  plt.xlabel("Time [s]")
  plt.title("Horizontal position sensors")
  plt.show()

if __name__ == "__main__":
  main()
