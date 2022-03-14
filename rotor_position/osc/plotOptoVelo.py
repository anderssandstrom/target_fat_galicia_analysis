#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotOptoVelo.py")
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

  
  pvNames=[]
  
  pvNames.append("Opto")
  pvNames.append("Velo")

  dataFile=sys.stdin

  parser = caMonitorArrayParser()
  pvY=[]  
  for pvname in pvNames:
   pvY.append(caPVArray(pvname))
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue
    
    lineValid = False
    for pvname in pvNames:
      if line.find(pvname)!=-1:
        lineValid=True;

    if not lineValid:
      continue  
    

    pvName, timeVal, data = parser.getValues(line)
    
    index=0
    for pvname in pvNames:      
      if pvName.find(pvname)>=0:
        pvY[index].setValues(timeVal,data)
      index=index+1

  yTime=[]
  yData=[]
  index=0

  for pvname in pvNames:
    yTimeTemp,yDataTemp = pvY[index].getData()
    print(pvname +"[" + str(len(yDataTemp)) + "]")
    yTime.append(yTimeTemp)
    yData.append(yDataTemp)
    index=index+1
  
  yDataAvg=[]
  index=0
  for pvname in pvNames:
    yDataAvg.append(np.mean(yData[index]))
    index=index+1
 
  fig2=plt.figure(2)

  print("len: " + str(len(yData[0])))
  time0=np.arange(0,len(yData[0]))*0.001
  time1=np.arange(0,len(yData[1]))*25.714/len(yData[1])

  print("len0: " + str(len(time0)))
  print("len1: " + str(len(time1)))

  

  legstr=[]

  legstr=[]
  legstr.append("Opto")
  ax1=fig2.add_subplot(2, 1,1 )
  ax1.plot(time0,yData[0]-yDataAvg[0]-0.5, 'b')
  ax1.legend(legstr)
  ax1.set_ylabel("Position [mm]")
  ax1.grid()

  legstr=[]
  legstr.append("Velo")
  ax2=fig2.add_subplot(2, 1, 2)
  ax2.plot(time1,yData[1], 'b')
  ax2.legend(legstr)
  ax2.grid()
  ax2.set_ylabel("Velocity [rpm]")
  
  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
