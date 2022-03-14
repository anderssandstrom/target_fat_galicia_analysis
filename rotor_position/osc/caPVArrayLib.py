#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
from datetime import datetime

class caPVArray:
  def __init__(self,name):
    self.name=name
    self.dataSet=np.array([])
    self.timeSet=np.array([])
    self.dataSetLength=0
    self.lastValue = 0
    self.firstscan = 1
    self.dataSetMod=np.array([])
    self.dataSetDeLin=np.array([])
    self.dataSetScale=np.array([])
    self.dataSetAdd=np.array([])
    self.turns = 0
    self.sampleTime=np.array([])
    self.lastTimeVal = 0

    return

  def setName(self, name):
    self.name=name
    return
  
  def getName(self):
    return self.name

  def getData(self):
    self.dataSet=self.dataSet.astype( np.dtype('float64'))
    return self.timeSet, self.dataSet

  def setValues(self,timeVal,value):
    self.dataSet=np.append(self.dataSet,value)
    self.timeSet=np.append(self.timeSet,timeVal)  
    if self.firstscan:
      self.lastTimeVal=timeVal      
      self.firstscan=0
    self.sampleTime=np.append(self.sampleTime,(timeVal-self.lastTimeVal).total_seconds())
    self.lastTimeVal=timeVal      
    self.dataSetLength=self.dataSetLength+1
    return

  def getSampleTime(self):
     return self.sampleTime

  def getLength(self):
    return self.dataSetLength

  def calcDeModValue(self,modulofactor):
    
    if self.dataSetLength <=1:
        print ("Error: Data set size to small." )
    
    
    timeSet, localdataSet=self.getData()
    #print localdataSet
    self.lastValue = localdataSet[0]
    
    for datapoint in localdataSet:
      
      if self.lastValue-datapoint > 0.75 * modulofactor:
        self.turns = self.turns + 1

      if datapoint-self.lastValue > 0.75 * modulofactor:
        self.turns = self.turns - 1

      self.dataSetMod=np.append(self.dataSetMod,datapoint + self.turns * modulofactor)    
      self.lastValue = datapoint
    
  def calcScale(self,scalefactor):
    timeSet, localdataSet=self.getData()
    for datapoint in localdataSet:
      self.dataSetScale=np.append(self.dataSetScale,datapoint *scalefactor)

  def calcAdd(self,addnumber):
    timeSet, localdataSet=self.getData()
    for datapoint in localdataSet:
      self.dataSetAdd=np.append(self.dataSetAdd,datapoint + addnumber)

  def substLin(self):
      timeSet, localdataSet=self.getData()
      x=range(0,self.getLength())
      y = localdataSet
      z = np.polyfit(x, y, 1)

      index = 0
      for datapoint in localdataSet:
        newData = datapoint - np.polyval(z,index)
        self.dataSetDeLin=np.append(self.dataSetDeLin,newData)
        index = index +1 

  def printDeLinValues(self):
    for i in range(1,self.getLength()):
      print (self.name + " " + self.timeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") + " " + str(self.dataSetDeLin[i]))

  def printDownSample(self,downSampleFactor):
    localTimeSet, localDataSet=self.getData()
    #print ("Length: " + str(self.getLength())+ "  " + str(localDataSet.size) + "  " + str(localTimeSet.size))
    for i in range(1,self.getLength(),int(downSampleFactor)):
      print (self.name + " " + localTimeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") + " " + str(localDataSet[i]))

  def printValues(self):
    localTimeSet, localDataSet=self.getData()    
    
    for i in range(1,self.getLength()):
      print (self.name + " " + localTimeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") + " " + str(localDataSet[i]))

  def printDiff(self):
    localTimeSet, localDataSet=self.getData()    
    if self.getLength()<2:
      print ("diff Error: To short data array.")
    for i in range(2,self.getLength()):
      print (self.name + " " + localTimeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") + " " + str(localDataSet[i-1]-localDataSet[i]))

  def printScaleValues(self):
    for i in range(1,self.getLength()):
      print (self.name + " " + str(self.timeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") ) + " " + str(self.dataSetScale[i]))

  def printDeModValues(self):
    for i in range(1,self.getLength()):
      print (self.name + " " + str(self.timeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") ) + " " + str(self.dataSetMod[i]))

  def printAddValues(self):
    for i in range(1,self.getLength()):
      print (self.name + " " + str(self.timeSet[i].strftime("%Y-%m-%d %H:%M:%S.%f") ) + " " + str(self.dataSetAdd[i]))
