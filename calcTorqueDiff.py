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

def printOutHelp():
  print("calcTorqueDiff: calcs velo from position. ")
  print("python calcTorqueDiff.py  <filename.npz> <from_sample> <to_sample> <gain>")
  print("example: python calcTorqueDiff.py data.npz 100 1500 -1")
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
  acc=[]
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

  # rescale acc so that avg corresponds to velo for the time
  acc , z = calcAcc(x, velo, 3, 1 / (sampleRate / filterSize))  
  npPos=np.array(pos)
  npPos=npPos-np.average(npPos)+180
    
  fig1=plt.figure(1)
  fig2=plt.figure(2)

  plotVeloPos(fig1,x,npPos,velo,acc,z)
  plotVeloDiff(fig2,x,npPos,velo,acc)

  fig1.savefig('fig1.svg')
  fig2.savefig('fig2.svg')
  plt.show(block=True)

def plotVeloPos(fig,time,npPos,velo,acc,z):
  ax1=fig.add_subplot(3, 1, 1)
  ax1.plot(time,acc,'.-')
  ax1.grid()
  ax1.set_ylabel("velocity (without linear comp) [rpm]")  
  ax2=fig.add_subplot(3, 1, 2)
  ax2.plot(time,velo,'.-')
  #ax2.plot(time,np.polyval(z,time),'.-')
  ax2.grid()
  ax2.set_ylabel("velocity [rpm]")
  ax3=fig.add_subplot(3, 1, 3)  
  ax3.plot(time,npPos,'o-')  
  ax3.grid()  
  ax3.set_ylabel("position [deg]")
  ax3.set_xlabel("time [s]")
  ax1.set_title("Position and velocity during rampdown")

def plotVeloDiff(fig,time,npPos,velo,acc):
  overflows=findOverflows(npPos)
  ax1=fig.add_subplot(1, 1, 1)
  start=overflows[0]
  index=0
  polys=[]
  
  slopediff=[]
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
    if index < len(overflows)-1 and index<12:
      end=overflows[index+1]-1
    else:
      continue

    if cIndex>=len(colors):
      cIndex=0
    ax1.plot(npPos[start:end], acc[start:end],"." + colors[cIndex])    
    cIndex=cIndex+1
    legStr.append("Rev " +str(index)+1)
    start=end+1
    index=index+1
  
  # plot fit valus
  index = 0
  cIndex=index
  start=overflows[0]
  # plot raw data
  for overflow in overflows:
    if index < len(overflows)-1 and index<12:
      end=overflows[index+1]-1
    else:
      continue

    if cIndex>=len(colors):
        cIndex=0
    z, res, g, g, g = np.polyfit(npPos[start:end], acc[start:end], 5, full=True)
    polys.append(z)    
    ax1.plot(npPos[start:end], np.polyval(z,npPos[start:end]),colors[cIndex])

    # find min, max of slope over the rev and calc difference
    zder=np.polyder(z)
    maximum=np.polyval(zder,npPos[start])
    minimum=maximum
    for pos in npPos[start:end]:
      val=np.polyval(zder,pos)
      if val>maximum:
          maximum=val
      if val<minimum:
          minimum=val
    slopediff.append(maximum-minimum)

    cIndex=cIndex+1    
    start=end+1
    index=index+1

  # only legend the "rawdata" use same colors for fit
  ax1.legend(legStr)
  print("Slopdiff: " +str(slopediff))  
  #skip last
  #plt.plot(npPos[start:-1], acc[start:-1],'.-')    

  ax1.grid()
  ax1.set_ylabel("velociy [rpm]")
  ax1.set_title("Velocity vs angle")

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
  acc=(velo-np.polyval(z,x))
  for data in acc:
   print("diff: "+ str(data))
  
  acc2=[]  
  acc2.append(0)
  accM1=0
  firstscan=1
  for vel in velo:
    if firstscan:
      velM1 = vel
      firstscan = 0
      continue
    currAcc=(vel-velM1) / sampleTimeS
    acc2.append( (currAcc + accM1) / 2)
    velM1 = vel
    accM1 = currAcc
  
  # avg acc must match the velo change over time, check and compensate
  # calc teoretical avg acc
  vStart=velo[0]
  vEnd=velo[-1]
  totalTime=x[-1]
  avgAcc = (vEnd-vStart) / totalTime
  
  # calc average value of array
  avgArrayValue=np.average(np.array(acc))
  print("avgArrayValue: "+ str(avgArrayValue))
  print("avgAcc:        "+ str(avgAcc))
  print("totalTime:     " + str(totalTime))
  return acc ,z #- avgArrayValue + avgAcc, z

if __name__ == "__main__":  
  if len(sys.argv)!=5:
    printOutHelp()
    sys.exit()
  
  npzfilename = sys.argv[1]
  xmin = int(sys.argv[2])
  xmax = int(sys.argv[3])
  gain = float(sys.argv[4])
  
  if npzfilename is None:
    print("Input file: " + npzfilename + " not valid.")
    sys.exit()
  
  openAndCalc(npzfilename,xmin,xmax,gain)
