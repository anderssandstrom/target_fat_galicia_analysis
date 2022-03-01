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
  #print("samplerate")
  #print(sampleRate)
  #print("filterSize")
  #print(filterSize)
  
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
      #posMinus1 = posMinus1 - 360
      
      # ignore overflow data
      posMinus1 = posAct
      continue

    actVelo = (posAct - posMinus1) * sampleRate / 360 *60

    #if abs(actVelo) > 1000:
    #  posMinus1 = posAct
    #  continue

    allvelo.append (actVelo)
    tempvelo[index] = actVelo

    if(index == filterSize - 1):
      #velMinus1 = avgVelo
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
  plt.subplot(3, 1, 1)
  plt.plot(x, acc,'.-')
  plt.grid()
  plt.ylabel("acceleration [rpm/s]")
  plt.subplot(3, 1, 2)
  plt.plot(x,velo,'.-')
  plt.plot(x,np.polyval(z,x),'.-')
  plt.grid()
  plt.ylabel("velocity [rpm]")
  plt.subplot(3, 1, 3)
  # remove offset
  npPos=np.array(pos)
  npPos=npPos-np.average(npPos)+180
  plt.plot(x,npPos,'o-')
  #plt.legend(legStr)
  plt.grid()
  #plt.title(fname)
  plt.ylabel("position [deg]")
  plt.xlabel("time [s]")
  plt.show()

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
  return acc - avgArrayValue + avgAcc, z
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

  