#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py [<filename>]")
  print ("example: python plotData.py xx.txt")
  print ("example stdin: cat data.log | grep -E 'thread|CPU' | python plotData.py" )
  print ("cat log.log | grep 'DIFF(ref-send)' | awk '{print $3}' | python ~/sources/ecmccomgui/pyDataManip/plotData.py")
def main():
  # Check args
  if len(sys.argv)>1:
    print(sys.argv[1] )
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)!=2 and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==1:
    fname=""
    dataFile=sys.stdin
 
  x=[]
  y=[]
  counter=0
  for line in dataFile:     
    print("LINE:" + line)
    if(len(line.strip())>0 and line.find(":") < 0 and line.find("/") < 0):        
      y.append(-float(line))
      x.append(counter/14)
      counter=counter+1
  
  pvMax = np.max(y)
  pvMin = np.min(y)
  pvAvg = np.mean(y)
  pvStd = np.std(y)
  #legStr = "[" + str(counter) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  
  plt.plot(x,y,'o-')
  plt.legend("Velcoity")
  plt.grid()
  #plt.title(fname)
  plt.ylabel("Velocity [rpm]")
  plt.xlabel("Time [s]")
  plt.show()
  
if __name__ == "__main__":
  main()
