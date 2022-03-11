#!/usr/bin/python
#*************************************************************************
# Copyright (c) 2020 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#   calcVelo.py
#
#  Created on: October 14, 2020
#      Author: Anders Sandström
#    
#  Converts npz file to csv files
#  
#*************************************************************************

import sys
import numpy as np

def printOutHelp():
  print("calcVelo: calcs velo from position. ")
  print("python calcVelo.py  <filename.npz> <filtersize>")
  print("example: python calcVelo.py data.npz 71")
  return

def openAndCalc(npzfilename, filterSize):    
  npzfile = np.load(npzfilename)
  # verify fft plugin
  if npzfile is None:
    print("Input file: " + npzfilename + " not valid.")
    return

  #for file in npzfile.files:
  #  print("Handling file:" + file)
  #return
  
  tempvelo=np.empty(filterSize)
  allvelo=[]
  dataArray=npzfile['rawdataY']
  sampleRate=npzfile['sampleRate']
  overflow = 0
  firstscan=True
  index=0
  valMinus1 = 0
  for data in dataArray:
    posAct = data
    if firstscan:
      firstscan = False
      valMinus1 = posAct
      continue
    
    #print(data)

    if(posAct  > (valMinus1 + 200)):
      overflow = overflow + 1
      # ignore oveflow data
      valMinus1 = data
      continue

    
    actVelo=(posAct - valMinus1) * sampleRate / 360 *60
    if abs(actVelo)>1000:
      valMinus1 = data
      continue


    allvelo.append (actVelo)
    tempvelo[index] = actVelo
    if(index == filterSize-1 ):    
      print(np.average(tempvelo))
      index = 0
      tempvelo=np.empty(filterSize)      
    else:
      index = index + 1
    valMinus1 = data
  #print("overflow")
  #print(overflow)

if __name__ == "__main__":  
  if len(sys.argv)!=3:
    printOutHelp()
    sys.exit()
  
  npzfilename=sys.argv[1]
  filterSize=int(sys.argv[2])

  
  if npzfilename is None:
    print("Input file: " + npzfilename + " not valid.")
    sys.exit()
  
  openAndCalc(npzfilename,filterSize)

  