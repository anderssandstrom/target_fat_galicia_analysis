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

  pvNames.append("Velo")
  pvNames.append("AI1")
  pvNames.append("AI2")  
  pvNames.append("AI3")
  

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
  yDataMax=[]
  yDataMin=[]
  yDataLen=[]
  index=0
  for pvname in pvNames:
    yAvgTemp=np.mean(yData[index])
    yDataAvg.append(yAvgTemp)
    yMaxTemp=np.max(yData[index])
    yDataMax.append(yMaxTemp)
    yMinTemp=np.min(yData[index])
    yDataMin.append(yMinTemp)
    yLenTemp=len(yData[index])
    yDataLen.append(yLenTemp)
    print(pvname + "[" + str(yLenTemp) + "] " + str(yMinTemp) + ".." + str(yMaxTemp) + "avg: " + str(yAvgTemp)  )
    index=index+1
 
  fig2=plt.figure(2)

  print("len: " + str(len(yData[0])))
  timeVelo=np.arange(0,len(yData[0]))*25.714/len(yData[1])

  timeOther=np.arange(0,len(yData[1]))*0.001
  
  print("len0: " + str(len(timeVelo)))
  print("len1: " + str(len(timeOther)))


  print("")
 
  legstr=[]
  legstr.append("0deg")
  legstr.append("120deg")
  legstr.append("240deg")
  ax1=fig2.add_subplot(2, 1,1 )
  ax1.plot(timeOther,yData[1]-(yDataMax[1]+yDataMin[1])/2, 'b')
  ax1.plot(timeOther,yData[2]-(yDataMax[2]+yDataMin[2])/2, 'g')
  ax1.plot(timeOther,yData[3]-(yDataMax[3]+yDataMin[3])/2, 'm')
  ax1.legend(legstr)
  ax1.set_ylabel("Position [mm]")
  ax1.grid()

  legstr=[]
  legstr.append("Velo")
  ax2=fig2.add_subplot(2, 1, 2)
  ax2.plot(timeVelo,yData[0], 'b')
  ax2.legend(legstr)
  ax2.grid()
  ax2.set_ylabel("Velocity [rpm]")
  
  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
