#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py [<filename>]")
  print ("example: python plotCaMonitor.py xx.txt")
  print ("example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitor.py" )

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
    dataFile=sys.stdin;

  parser=caMonitorArrayParser()
  pvs=[]

  for line in dataFile:
    if not parser.lineValid(line):      
      continue

    pvName, timeVal, data=parser.getValues(line)
    newPv=True;
    pvToAddDataTo=caPVArray(pvName)
    # See if old or new pv
    for pv in pvs:
      if pv.getName() == pvName:        
        pvToAddDataTo=pv
        newPv=False;
        break;
    
    pvToAddDataTo.setValues(timeVal,data)    
    if newPv:       
      pvs.append(pvToAddDataTo)
      print("Added PV: " + pvName)
  
  print("Statistics: ")
  legend=[]
  print (pvs)

  for pv in pvs: 
    timeSet, dataSet=pv.getData()
    #for d in dataSet:
    #  print d
    pvLength = pv.getLength()
    pvMax = np.max(dataSet)
    pvMin = np.min(dataSet)
    pvAvg = np.mean(dataSet)
    pvStd = np.std(dataSet)
    legStr = pv.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
    legend.append(pv.getName())
     
    x=timeSet - relativedelta(minutes=5)
    y=dataSet
    print (legStr)
    plt.plot(x,y,'o-')

  plt.legend(legend)
  plt.grid()
  plt.title(fname)
  plt.xlabel("time")
  plt.show()
  
if __name__ == "__main__":
  main()
