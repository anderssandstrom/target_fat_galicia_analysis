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

  
  pvNames=[]
  
  pvNames.append("TorqueMin")
  pvNames.append("TorqueMax")
  pvNames.append("VeloMin")
  pvNames.append("VeloMax")

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
  
  legstr=[]
  legstr.append("Torque Min")
  legstr.append("Torque Avg")
  legstr.append("Torque Max")
  fig2=plt.figure(2)
  ax1=fig2.add_subplot(2, 1, 1)
  ax1.plot(yTime[0],yData[0], 'b')
  ax1.plot(yTime[1],(yData[1]+yData[0])/2, 'g')
  ax1.plot(yTime[1],yData[1], 'm')

  ax1.set_ylabel("Torque [Nm]")
  ax1.legend(legstr)
  ax1.set_ylim(80,200)
  ax1.grid()
  
  legstr=[]
  legstr.append("Velocity Min")
  legstr.append("Velocity Avg")
  legstr.append("Velocity Max")
  ax2=fig2.add_subplot(2, 1, 2)
  ax2.plot(yTime[2],yData[2], 'b')
  
  length=len(yData[2])
  if len(yData[2])<length:
    length=len(yData[2])

  ax2.plot(yTime[2][0:length],(yData[2][0:length]+yData[3][0:length])/2, 'g')
  
  ax2.plot(yTime[3],yData[3], 'm')
  ax2.set_ylabel("Velocity [rpm]")
  ax2.legend(legstr)
  ax2.set_ylim(23.5,24.5)
  ax2.grid()
  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
