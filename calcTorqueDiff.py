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
      #accTemp = (avgVelo - velMinus1) * sampleRate
      #acc.append(accTemp)
      #print("acc: " + str(accTemp))
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
  
  overflows=findOverflows(npPos)
  fig1=plt.figure(1)
  fig2=plt.figure(2)

  ax11=fig1.add_subplot(2, 1, 1)
  start=overflows[0]
  index=0
  polys=[]
  
  slopediff=[]

  for overflow in overflows:
    if index < len(overflows)-1 and index<12:
      end=overflows[index+1]-1
    else:
      continue
    z, res, g, g, g = np.polyfit(npPos[start:end], acc[start:end], 3, full=True)
    polys.append(z)
    ax11.plot(npPos[start:end], acc[start:end],'.-')
    ax11.plot(npPos[start:end], np.polyval(z,npPos[start:end]))
    
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

    start=end+1
    index=index+1

  print("Slopdiff: " +str(slopediff))  
  #skip last
  #plt.plot(npPos[start:-1], acc[start:-1],'.-')    

  ax11.grid()
  ax11.set_ylabel("acceleration [rpm/s]")

  #fig1.add_subplot(3, 1, 2)
  #plt.plot(x,velo,'.-')
  #plt.plot(x,np.polyval(z,x),'.-')
  #plt.grid()
  #plt.set_ylabel("velocity [rpm]")
  ax12=fig1.add_subplot(2, 1, 2)
  # remove offset
  ax12.plot(x,npPos,'o-')
  #plt.legend(legStr)
  ax12.grid()
  #plt.title(fname)
  ax12.set_ylabel("position [deg]")
  ax12.set_xlabel("time [s]")  
  fig1.savefig('filename.svg')  
  plt.show(block=True)


def plotVeloPos(fig,npPos,velo):


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
  #return acc

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

  