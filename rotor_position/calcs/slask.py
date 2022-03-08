#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 

scale=0.7379332696892712
 
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

  pvY1name = "AI1"
  pvY2name = "AI2"
  pvY3name = "AI3"
  pvY4name = "AI4"
  pvY5name = "Opto"
    
  dataFile=sys.stdin

  parser = caMonitorArrayParser()
  pvY1   = caPVArray(pvY1name)
  pvY2   = caPVArray(pvY2name)
  pvY3   = caPVArray(pvY3name)
  pvY4   = caPVArray(pvY4name)
  pvY5   = caPVArray(pvY5name)
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    if line.find(pvY1name)==-1 and line.find(pvY2name)==-1 and line.find(pvY3name)==-1 and line.find(pvY4name)==-1 and line.find(pvY5name)==-1:
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

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()
  y3Time,y3Data = pvY3.getData()
  y4Time,y4Data = pvY4.getData()
  y5Time,y5Data = pvY5.getData()

  # Scaling of sensors due to wrong material (optional) only for AI1..AI4
  y1Data = y1Data * scale
  y2Data = y2Data * scale
  y3Data = y3Data * scale
  y4Data = y4Data * scale
  #y5Data=y5Data*scale  # scale of optical sensor is OK

  # subtract avg
  y1Data = y1Data - np.mean(y1Data)
  y2Data = y2Data - np.mean(y2Data)
  y3Data = y3Data - np.mean(y3Data)
  y4Data = y4Data - np.mean(y4Data)
  y5Data = y5Data - np.mean(y5Data)

  print("Lengths")
  print(len(y1Data))
  print(len(y2Data))
  print(len(y3Data))
  print(len(y4Data))
  print(len(y5Data))
  #print("Statistics: ")
  #pvLength = pvY1.getLength()
  #pvMax = np.max(y1Data)
  #pvMin = np.min(y1Data)
  #pvAvg = np.mean(y1Data)
  #pvStd = np.std(y1Data)
  #legStr = pvY1.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  #print (legStr)
  #
  #pvLength = pvY2.getLength()
  #pvMax = np.max(y2Data)
  #pvMin = np.min(y2Data)
  #pvAvg = np.mean(y2Data)
  #pvStd = np.std(y2Data)
  #legStr = pvY2.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  #print (legStr)

  fig = plt.figure(1)

  #ax1=fig.add_subplot(5, 1, 1)
  #ax1.plot(y1Time, y1Data, 'o-b')
  #ax1.legend("0deg")
  #ax1.set_ylabel("position [mm]")  
  #ax1.grid()
#
  #ax2=fig.add_subplot(5, 1, 2)
  #ax2.plot(y2Time, y2Data, 'o-g')
  #ax2.legend("120deg")
  #ax2.set_ylabel("position [mm]")  
  #ax2.grid()
#
  #ax3=fig.add_subplot(5, 1, 3)
  #ax3.plot(y3Time, y3Data, 'o-r')
  #ax3.legend("240deg")
  #ax3.set_ylabel("position [mm]")  
  #ax3.grid()
#
  #ax4=fig.add_subplot(5, 1, 4)
  #ax4.plot(y4Time, y4Data, 'o-c')
  #ax4.legend("Vertical")
  #ax4.set_ylabel("position [mm]")  
  #ax4.grid()
#
  #ax5=fig.add_subplot(5, 1, 5)
  #ax5.plot(y5Time, y5Data, 'o-m')
  #ax5.legend("Circumference (120deg)")
  #ax5.set_ylabel("position [mm]")  
  #ax5.grid()
  #
#
  #plt.xlabel("Time [s]")
  bin_count=50
  fig2=plt.figure(2)
  ax1=fig2.add_subplot(1, 5, 1)
  ax1.hist(y1Data, bins=bin_count, color='b')
  ax1.legend("0deg")
  ax1.set_ylabel("position [mm]")  
  ax1.grid()
  
  ax2=fig2.add_subplot(1, 5, 2)
  ax2.hist(y2Data, bins=bin_count, color='g')
  ax2.legend("120deg")
  ax2.set_ylabel("position [mm]")  
  ax2.grid()

  ax3=fig2.add_subplot(1, 5, 3)
  ax3.hist(y3Data, bins=bin_count, color='r')
  ax3.legend("240deg")
  ax3.set_ylabel("position [mm]")  
  ax3.grid()

  ax4=fig2.add_subplot(1, 5, 4)
  ax4.hist(y4Data, bins=bin_count, color='c')
  ax4.legend("Vert")
  ax4.set_ylabel("position [mm]")  
  ax4.grid()

  ax5=fig2.add_subplot(1, 5, 5)
  ax5.hist(y5Data, bins=bin_count, color='m')
  ax5.legend("Circumference (120deg)")
  ax5.set_ylabel("position [mm]")  
  ax5.grid()

  plt.show()

if __name__ == "__main__":
  main()
