from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

import CRC
import decoder

def plotPath(planeDict):
	# create new figure, axes instances.
	fig=plt.figure()
	ax=fig.add_axes([0.1,0.1,0.8,0.8])
	# setup mercator map projection.

	lon,lat = 151.1772,-33.9461
	r = 10.5
	print('Making map')
	m = Basemap(llcrnrlon=lon-r,llcrnrlat=lat-r,urcrnrlon=lon+r,urcrnrlat=lat+r,\
	            rsphere=(6378137.00,6356752.3142),\
	            resolution='c',projection='merc',\
	            lat_0=lat,lon_0=lon,lat_ts=20.)

	m.drawcoastlines()

	print('Plotting planes')
	for plane in planeDict.keys():
		points = decodePositions(planeDict[plane])
		
		'''
		lon1,lat1 = points[0,1],points[0,0],points[0,2]
		lon2,lat2 = lon,lat
		print('Range: ',Model.distanceBetweenPoints(lon1,lat1,lon2,lat2))
		'''
		if points.shape[0]>2:
			print(plane)
			m.plot(points[:,1],points[:,0],latlon=True)
		
	plt.savefig('FlightPaths.png',dpi=900)
	plt.show()
	plt.close()

def decodePositions(messages):
	msg0=''
	msg1=''
	t0=0
	t1=0
	points=[]
	for Time,msg in messages:
		Time = float(Time)
		tc = decoder.get_tc(msg)
		if tc>=9 and tc<=18:
			oe = decoder.get_oe_flag(msg)
			if oe==0:
				msg0=msg
				t0=Time
			else:
				msg1=msg
				t1=Time
			if msg0!='' and msg1!='':
				if abs(t0-t1)<10:
					decodedPositions = decoder.get_position(msg0, msg1, t0, t1)
					if decodedPositions != None and len(decodedPositions)>0:
						points.append(decodedPositions)
	return(np.asarray(points))

messageCount=0
print('Generating plane dict')
f = open('Syd.txt','r')
planeDict={}
for line in f:
	Time,Message = line[:-1].split(' ')
	isvalid = CRC.computeChecksum(Message)
	addr = decoder.get_icao_addr(Message)

	tc = decoder.get_tc(Message)	
	if tc>=9 and tc<=18:
		rawmsg=Message
		if isvalid==False:
			isvalid,Message = CRC.correctBitError(rawmsg)

		'''
		if isvalid==False:
			isvalid,Message = CRC.correct2BitError(rawmsg)
		'''
		if isvalid==True:
			messageCount+=1	
			addr = decoder.get_icao_addr(Message)
			if addr not in planeDict.keys():
				planeDict[addr] = [(Time,Message)]
			else:
				planeDict[addr].append((Time,Message))
print(messageCount)
plotPath(planeDict)