#*************************************************************************
# Copyright (c) 2020 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#   calcTorqueDiff.py
#
#  Created on: October 14, 2020
#      Author: Anders Sandström
#    
#  Converts npz file to csv files
#  
#*************************************************************************

import sys
import numpy as np
import matplotlib.pyplot as plt

revs = 0
I=5260

def printOutHelp():
  print("calcTorqueDiff: calcs velo from position. ")
  print("python calcTorqueDiff.py  <filename.npz> <from_sample> <to_sample> <gain> <rev_count>" )
  print("example: python calcTorqueDiff.py data.npz 100 1500 -1 10")
  return

def openAndCalc(npzfilename,xmin,xmax,sign):    
  npzfile = np.load(npzfilename)
  # verify fft plugin
  if npzfile is None:
    print("Input file: " + npzfilename + " not valid.")
    return

  #for file in npzfile.files:
  #  print("Handling file:" + file)
  #return
  
  allvelo=[]
  velo=[]
  pos=[]
  velWithoutLinDec=[]
  x=[]
  dataArray=npzfile['rawdataY']
  if xmax==0:
    xmax=len(dataArray)-1
  dataArray=dataArray[xmin:xmax]
  sampleRate=npzfile['sampleRate']
  filterSize=int(sampleRate / 14.0)

  tempvelo=np.empty(int(filterSize))
  
  overflow = 0
  firstscan=True
  index=0
  posMinus1 = 0
  velMinus1 = 0
  time = 0
  for data in dataArray:
    posAct = data * sign
    time = time + 1.0 / sampleRate
    
    if firstscan:
      firstscan = False
      posMinus1 = posAct
      avgVelo = 0
      continue
    
    if(posAct < ( posMinus1 - 200 )):
      overflow = overflow + 1
      posMinus1 = posAct
      continue # ignore overflows

    actVelo = (posAct - posMinus1) * sampleRate / 360 * 60

    allvelo.append (actVelo)
    tempvelo[index] = actVelo

    if(index == filterSize - 1):
      avgVelo = np.average(tempvelo)
      print("velo: " + str(avgVelo))
      print("pos: " + str(posAct))
      velo.append(avgVelo)
      pos.append(posAct)
      x.append(time)
      index = 0
      print("tempvelo:" + str(tempvelo))
      tempvelo = np.empty(int(filterSize))
    else:
      index = index + 1
    
    posMinus1 = posAct

  # now we have velo in y[] and time in x

  # rescale velWithoutLinDec so that avg corresponds to velo for the time
  velWithoutLinDec , z = calcAcc(x, velo, 3, 1 / (sampleRate / filterSize))  
  npPos=np.array(pos)
  npPos=npPos-np.average(npPos)+180
    
  fig1=plt.figure(1)
  fig2=plt.figure(2)
  fig3=plt.figure(3)

  plotVeloPos(fig1,x,npPos,velo,velWithoutLinDec,z)
  angleRev, timeRev, accPolysVsAngle, accPolysVsTime= plotVeloDiff(fig2,x,npPos,velo,velWithoutLinDec)
  plotTorqueDiff(fig3,angleRev, timeRev, accPolysVsAngle, accPolysVsTime):

  fig1.savefig('fig1.svg')
  fig2.savefig('fig2.svg')
  fig3.savefig('fig3.svg')
  plt.show(block=True)

def plotVeloPos(fig,time,npPos,velo,velWithoutLinDec,z):
  overflows=findOverflows(npPos)

  ax1=fig.add_subplot(3, 1, 1)
  ax1.plot(time,velWithoutLinDec,'.-')
  ax1.grid()
  plotRevLines(ax1,overflows,time,np.min(velWithoutLinDec),np.max(velWithoutLinDec))

  ax1.set_ylabel("velocity (without linear comp) [rpm]")  
  ax2=fig.add_subplot(3, 1, 2)
  ax2.plot(time,velo,'.-')
  plotRevLines(ax2,overflows,time,np.min(velo),np.max(velo))
  #ax2.plot(time,np.polyval(z,time),'.-')
  ax2.grid()
  ax2.set_ylabel("velocity [rpm]")
  ax3=fig.add_subplot(3, 1, 3)  
  ax3.plot(time,npPos,'.-')
  plotRevLines(ax3,overflows,time,np.min(npPos),np.max(npPos))
  ax3.grid()  
  ax3.set_ylabel("position [deg]")
  ax3.set_xlabel("time [s]")
  ax1.set_title("Position and velocity during rampdown")

def plotVeloDiff(fig,time,npPos,velo,velWithoutLinDec):
  overflows=findOverflows(npPos)
  ax1=fig.add_subplot(2, 1, 1)
  ax2=fig.add_subplot(2, 1, 2)
  start=overflows[0]
  index=0
  velRevPolysAngle=[]
  accPolysVsTime=[]
  accPolysVsAngle = []
  timeRev  = []
  angleRev =[]
  slopediffDeg=[]
  slopediffTime=[]
  legStr=[]
  
  colors=[]
  colors.append('-b')
  colors.append('-g')
  colors.append('-r')
  colors.append('-c')
  colors.append('-m')
  colors.append('-y')
  colors.append('-k')

  cIndex=index
  # plot raw data
  for overflow in overflows:
    if index < len(overflows)-1 and index<revs:
      end=overflows[index+1]-1
    else:
      continue

    if cIndex>=len(colors):
      cIndex=0
    ax1.plot(npPos[start:end], velWithoutLinDec[start:end],"." + colors[cIndex])    
    
    legStr.append("Rev " +str(index+1))
  
    ax2.plot(time[start:end]-time[start], velWithoutLinDec[start:end],"." + colors[cIndex])    
    
    cIndex=cIndex+1
    start=end+1
    index=index+1
  
    
  # plot fit values
  index = 0
  cIndex=index
  start=overflows[0]
  # plot raw data
  for overflow in overflows:
    if index < len(overflows)-1 and index<revs:
      end=overflows[index+1]-1
    else:
      continue

    if cIndex>=len(colors):
        cIndex=0
    z, res, g, g, g = np.polyfit(npPos[start:end], velWithoutLinDec[start:end], 5, full=True)
    velRevPolysAngle.append(z)    
    ax1.plot(npPos[start:end], np.polyval(z,npPos[start:end]),colors[cIndex])

    # find min, max of slope vs angle over the rev and calc difference
    zder=np.polyder(z)
    accPolysVsAngle.append(zder)
    maximum=np.polyval(zder,npPos[start])
    minimum=maximum
    for pos in npPos[start:end]:
      val=np.polyval(zder,pos)
      if val>maximum:
          maximum=val
      if val<minimum:
          minimum=val
    slopediffDeg.append(maximum-minimum)

    z, res, g, g, g = np.polyfit(time[start:end]-time[start], velWithoutLinDec[start:end], 5, full=True)    
    ax2.plot(time[start:end]-time[start], np.polyval(z,time[start:end]-time[start]),colors[cIndex])

    # find min, max of slope vs time over the rev and calc difference
    zder=np.polyder(z)
    accPolysVsTime.append(zder)
    maximum=np.polyval(zder,0)
    minimum=maximum
    for t in time[start:end]-time[start]:
      val=np.polyval(zder,t)
      if val>maximum:
          maximum=val
      if val<minimum:
          minimum=val
    slopediffTime.append(maximum-minimum)
    
    timeRev.append(time[start:end])
    angleRev.append(npPos[start:end])
    cIndex=cIndex+1    
    start=end+1
    index=index+1

  # only legend the "rawdata" use same colors for fit
  ax1.legend(legStr,loc='upper right')
  npSlopeDiffDeg=np.array(slopediffDeg)
  print("slopediffDeg: " +str(slopediffDeg) +  "Avg: " + str(np.average(npSlopeDiffDeg)))

  npSlopeDiffTime=np.array(slopediffTime)
  print("slopediffTime: " +str(npSlopeDiffTime) +  "Avg: " + str(np.average(npSlopeDiffTime)))
  
  alfa=npSlopeDiffTime * 2*3.1415/60

  torque=I*alfa/2

  print("torque (+-): " + str(torque) + "Nm (Avg " +str(np.average(torque))+ "Nm)")


  #skip last
  #plt.plot(npPos[start:-1], velWithoutLinDec[start:-1],'.-')    

  ax1.grid()
  ax1.set_xlabel("Wheel angle [deg]")
  ax1.set_ylabel("velociy [rpm]")
  ax1.set_title("Velocity vs angle for " + str(int(revs)) + " revs")
  ax2.grid()
  ax2.legend(legStr,loc='upper right')
  ax2.set_xlabel("Time [s]")
  ax2.set_ylabel("velociy [rpm]")
  ax2.set_title("Velocity vs time for " + str(int(revs)) + " revs")

  return angleRev, timeRev, accPolysVsAngle, accPolysVsTime

def plotTorqueDiff(fig,angleRev, timeRev, accPolysVsAngle, accPolysVsTime):
  ax1=fig.add_subplot(2, 1, 1)
  ax2=fig.add_subplot(2, 1, 2)
  index = 0
  cIndex=index
  colors=[]
  colors.append('-b')
  colors.append('-g')
  colors.append('-r')
  colors.append('-c')
  colors.append('-m')
  colors.append('-y')
  colors.append('-k')
  print("jshdak.lsjföasbföalskalsknfd")
  for z in accPolysVsTime:
    if cIndex>=len(colors):
       cIndex=0

    ax2.plot(timeRev, np.polyval(z,timeRev,colors[cIndex])
    legStr.append("Rev " +str(index+1))

    cIndex=cIndex+1  
    index=index+1

  ax2.grid()
  ax2.set_xlabel("Wheel angle [deg]")
  ax2.set_ylabel("velociy [rpm]")
  ax2.set_title("Velocity vs angle for " + str(int(revs)) + " revs")
  ax2.legend(legStr,loc='upper right')

  #ax1.grid()
  #ax1.legend(legStr,loc='upper right')
  #ax1.set_xlabel("Time [s]")
  #ax1.set_ylabel("velociy [rpm]")
  #ax1.set_title("Velocity vs time for " + str(int(revs)) + " revs")

      

def plotRevLines(ax,overflows,time,ymin,ymax):
   for of in overflows:
       x=time[of]
       print("X: " + str(x))
       ax.plot([x ,x], [ymin, ymax], "-r")


def findOverflows(positions):
  overflows=[]
  posMinus1=positions[0]
  index=0
  for pos in positions:
    if(pos < ( posMinus1 - 200 )):
      overflows.append(index+1)            
    posMinus1 = pos
    index=index+1
  return overflows   

def calcAcc(x,velo,order, sampleTimeS):
  z, res, g, g, g = np.polyfit(x, velo, order, full=True)
  # subtract poly
  velWithoutLinDec=(velo-np.polyval(z,x))
  for data in velWithoutLinDec:
   print("diff: "+ str(data))
  
  velWithoutLinDec2=[]  
  velWithoutLinDec2.append(0)
  velWithoutLinDecM1=0
  firstscan=1
  for vel in velo:
    if firstscan:
      velM1 = vel
      firstscan = 0
      continue
    currvelWithoutLinDec=(vel-velM1) / sampleTimeS
    velWithoutLinDec2.append( (currvelWithoutLinDec + velWithoutLinDecM1) / 2)
    velM1 = vel
    velWithoutLinDecM1 = currvelWithoutLinDec
  
  # avg velWithoutLinDec must match the velo change over time, check and compensate
  # calc teoretical avg velWithoutLinDec
  vStart=velo[0]
  vEnd=velo[-1]
  totalTime=x[-1]
  avgvelWithoutLinDec = (vEnd-vStart) / totalTime
  
  # calc average value of array
  avgArrayValue=np.average(np.array(velWithoutLinDec))
  print("avgArrayValue:       " + str(avgArrayValue))
  print("avgvelWithoutLinDec: " + str(avgvelWithoutLinDec))
  print("totalTime:           " + str(totalTime))
  return velWithoutLinDec ,z #- avgArrayValue + avgvelWithoutLinDec, z

if __name__ == "__main__":  
  if len(sys.argv)!=6:
    printOutHelp()
    sys.exit()
  
  npzfilename = sys.argv[1]
  xmin = int(sys.argv[2])
  xmax = int(sys.argv[3])
  gain = float(sys.argv[4])
  revs = float(sys.argv[5])
  
  if npzfilename is None:
    print("Input file: " + npzfilename + " not valid.")
    sys.exit()
  
  openAndCalc(npzfilename,xmin,xmax,gain)
