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
  
  pvNames.append("AI1")
  pvNames.append("AI2")
  pvNames.append("AI3")
  pvNames.append("AI4")
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

  legstr=[]
  legstr.append("0deg")
  legstr.append("120deg")
  legstr.append("240deg")

  ax1=fig2.add_subplot(4, 1, 1)
  ax1.plot(yTime[0],yData[0]-yDataAvg[0], 'b')
  ax1.plot(yTime[1],yData[1]-yDataAvg[1], 'g')
  ax1.plot(yTime[2],yData[2]-yDataAvg[2], 'm')
  ax1.set_ylabel("Position [mm]")
  ax1.legend(legstr)
  ax1.grid()

  legstr=[]
  legstr.append("Vert")
  ax2=fig2.add_subplot(4, 1, 2)
  ax2.plot(yTime[3],yData[3]-yDataAvg[3], 'b')
  ax2.legend(legstr)
  ax2.set_ylabel("Position [mm]")
  ax2.grid()

  legstr=[]
  legstr.append("Opto")
  ax3=fig2.add_subplot(4, 1, 3)
  ax3.plot(yTime[4],yData[4]-yDataAvg[4], 'b')
  ax3.legend(legstr)
  ax3.set_ylabel("Position [mm]")
  ax3.grid()

  legstr=[]
  legstr.append("Velo")
  ax4=fig2.add_subplot(4, 1, 4)
  ax4.plot(yTime[5],yData[5], 'b')
  ax4.legend(legstr)
  ax4.grid()
  ax4.set_ylabel("Velocity [rpm]")
  
  plt.xlabel("Time [s]")
  plt.show()

if __name__ == "__main__":
  main()
