import os
import math
import numpy as np
import scipy.signal
import scipy.stats
import time

import decoder
import PreambleDetection
import CRC

import matplotlib.pyplot as plt

def decodeMessage(m,messageStart):
	bitTemplate = np.hstack((np.ones(5),-np.ones(5)))
	bitString =''
	confidenceArray =np.zeros((112))
	for index in range(0,112):
		fragment = m[messageStart+10*index:messageStart+10*(index+1)]
		bitValue = np.dot(bitTemplate,fragment)
		confidenceArray[index]=abs(bitValue)
		if bitValue>0:
			bitString+='1'
		else:
			bitString+='0'
	return(bitString,confidenceArray)
		
def grabData(fileName,numSeconds,LNAGain=14,IFGain=10,MIXGain=10):
	targetFreq = 1092.5
	numSamples = int(numSeconds*Fs)
	os.system('airspy_rx -r '+fileName+' -t '+str(sampleType)+' -f '+str(targetFreq-Fs/(4.0*10**6))+' -l '+str(LNAGain)+' -v '+str(IFGain)+' -m '+str(MIXGain)+'  -n '+str(numSamples))

def findPossibleMessages():	
	segmentLength = 0.2 #Seconds
	f = open("data.bin", "r")
	Input = np.fromfile(f, dtype=np.int16)
	Input = Input[10**4:]

	messageList=[]
	for segment in range(0,numSeconds/segmentLength):
		print(segment)
		InputSegment=Input[2*segmentLength*Fs*segment:2*segmentLength*Fs*(segment+1)]
		
		#Strip out the I and Q
		I = InputSegment[0::2].astype(float) 
		Q = InputSegment[1::2].astype(float)
		
		m = np.sqrt(I**2+Q**2)
		messages = PreambleDetection.findPreambles(m,threshold,'8D')
		
		for messageStart in messages:
			Time = (acquisitionTime-startTime)+(segment*segmentLength)+messageStart/Fs
			bitString,confidenceArray = decodeMessage(m,messageStart)
			hexString = CRC.bin2hex(bitString)
			if hexString[0:2] == '8D':
				messageList.append((Time,hexString))
	return(messageList)

Fs = 10.0*10**6      # sample rate, Hz
numSeconds = 10
threshold = 1000
startTime = time.time()

f = open('Syd.txt','w')
for i in range(0,1):
	
	acquisitionTime = time.time()
	#grabData('data.bin',numSeconds,LNAGain=14,IFGain=10,MIXGain=10)
	messageList = findPossibleMessages()
	print('Num Messages',len(messageList))
	for Time,message in messageList:
		f.write(str(Time)+' '+message+'\n')
	f.flush()
f.close()

'''
string1 =  "{0:b}".format(int('8DAC644520041332CB2D603D9AEB',16)).zfill(112)
for Time,message in messageList:
	if decoder.get_tc(message)==4:
		string2 = "{0:b}".format(int(message,16)).zfill(112)
		print(CRC.hammingDistance(string1,string2,0,112))
'''	





