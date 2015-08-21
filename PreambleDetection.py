import numpy as np
import scipy.signal
import scipy.stats

import decoder

def checkMessageStatistics(messageIndex,m):
	message = m[messageIndex:messageIndex+1120]
	message = message/message.mean()
	statisticsValid=False
	if message.max()<5:
		if scipy.stats.kurtosis(message)<1:
			statisticsValid=True
	return(statisticsValid)

def findPreambles(m,threshold,extendedPreamble):
	messageIndexes=[]
	k = 20.0/60.0
	preambleTemplate = np.hstack((np.ones(5),-k*np.ones(5),np.ones(5),-k*np.ones(20),np.ones(5),-k*np.ones(5),np.ones(5),-k*np.ones(30)))
	
	#Generate Bit array to look for plane
	binString = decoder.hex2bin(extendedPreamble)
	bitArray = np.zeros(2*len(binString))
	for i in range(0,len(binString)):
		if binString[i]=='1':
			bitArray[2*i]=1
			bitArray[2*i+1]=-1
		else:
			bitArray[2*i]=-1
			bitArray[2*i+1]=1

	bitArray = np.repeat(bitArray, 5)
	preambleTemplate = np.hstack((preambleTemplate,bitArray))
	corr = scipy.signal.fftconvolve(m,preambleTemplate[::-1])

	#Find where the correlation is greater than the threshold
	possibleMessages = np.where(corr>threshold)[0]
	
	blockStart = 0
	blockLength = 1200
	for message in possibleMessages:
		if message > blockStart + blockLength:
			blockOffset = np.argmax(corr[message:message+blockLength])
			messageIndex = message + blockOffset + 1  - len(binString)*10
			if (m.size-messageIndex)>blockLength:
				statisticsValid = checkMessageStatistics(messageIndex,m)
				if statisticsValid==True:
					blockStart=message
					#Make sure we will save a compute message
					messageIndexes.append(messageIndex)
	return(messageIndexes)

