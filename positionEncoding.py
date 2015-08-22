import math
import decoder

def NL(lat):
	"""Lookup table to convert the latitude to index. """
	if lat < 0 : lat = -lat             # Table is symmetric about the equator.
	if lat < 10.47047130 : return 59
	if lat < 14.82817437 : return 58
	if lat < 18.18626357 : return 57
	if lat < 21.02939493 : return 56
	if lat < 23.54504487 : return 55
	if lat < 25.82924707 : return 54
	if lat < 27.93898710 : return 53
	if lat < 29.91135686 : return 52
	if lat < 31.77209708 : return 51
	if lat < 33.53993436 : return 50
	if lat < 35.22899598 : return 49
	if lat < 36.85025108 : return 48
	if lat < 38.41241892 : return 47
	if lat < 39.92256684 : return 46
	if lat < 41.38651832 : return 45
	if lat < 42.80914012 : return 44
	if lat < 44.19454951 : return 43
	if lat < 45.54626723 : return 42
	if lat < 46.86733252 : return 41
	if lat < 48.16039128 : return 40
	if lat < 49.42776439 : return 39
	if lat < 50.67150166 : return 38
	if lat < 51.89342469 : return 37
	if lat < 53.09516153 : return 36
	if lat < 54.27817472 : return 35
	if lat < 55.44378444 : return 34
	if lat < 56.59318756 : return 33
	if lat < 57.72747354 : return 32
	if lat < 58.84763776 : return 31
	if lat < 59.95459277 : return 30
	if lat < 61.04917774 : return 29
	if lat < 62.13216659 : return 28
	if lat < 63.20427479 : return 27
	if lat < 64.26616523 : return 26
	if lat < 65.31845310 : return 25
	if lat < 66.36171008 : return 24
	if lat < 67.39646774 : return 23
	if lat < 68.42322022 : return 22
	if lat < 69.44242631 : return 21
	if lat < 70.45451075 : return 20
	if lat < 71.45986473 : return 19
	if lat < 72.45884545 : return 18
	if lat < 73.45177442 : return 17
	if lat < 74.43893416 : return 16
	if lat < 75.42056257 : return 15
	if lat < 76.39684391 : return 14
	if lat < 77.36789461 : return 13
	if lat < 78.33374083 : return 12
	if lat < 79.29428225 : return 11
	if lat < 80.24923213 : return 10
	if lat < 81.19801349 : return 9
	if lat < 82.13956981 : return 8
	if lat < 83.07199445 : return 7
	if lat < 83.99173563 : return 6
	if lat < 84.89166191 : return 5
	if lat < 85.75541621 : return 4
	if lat < 86.53536998 : return 3
	if lat < 87.00000000 : return 2
	else : return 1

def computeXZYZ(lon,lat,i):
	NZ = 15
	Dlat = 360.0/(4.0*NZ-i)
	YZ = math.floor(2**17*((lat%Dlat)/Dlat)+0.5)

	Rlat = Dlat*((YZ/2**17)+math.floor(lat/Dlat))
	Dlon = 360.0/(NL(Rlat)-i)

	XZ = math.floor(2**17*((lon%Dlon)/Dlon)+0.5)

	YZ = YZ%2**17
	XZ = XZ%2**17

	#print(XZ,YZ)
	YZ = "{0:0b}".format(YZ).zfill(17)
	XZ = "{0:0b}".format(XZ).zfill(17)	
	return(XZ,YZ)

lon1,lat1 = -118.381,33.945
lon2,lat2 = -118.383,33.947

t0=0
t1=1

cprlon0,cprlat0 = computeXZYZ(lon1,lat1,0)
cprlon1,cprlat1 = computeXZYZ(lon2,lat2,1)

msg0 = '0'*54 + cprlat0 + cprlon0+'0'*24 
msg1 = '0'*54 + cprlat1 + cprlon1+'0'*24 

msg0 = "{0:0x}".format(int(msg0,2)).zfill(28)
msg1 = "{0:0x}".format(int(msg1,2)).zfill(28)

cprlat0 = decoder.get_cprlat(msg0)
cprlat1 = decoder.get_cprlat(msg1)
cprlon0 = decoder.get_cprlon(msg0)
cprlon1 = decoder.get_cprlon(msg1)

#print(cprlat0, cprlat1, cprlon0, cprlon1)
lat,lon = decoder.cpr2position(cprlat0, cprlat1, cprlon0, cprlon1, t0, t1)

print(111*(lat-lat2),111*(lon-lon2))
print(111*(lat-lat1),111*(lon-lon1))



