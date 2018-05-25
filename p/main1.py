import snap7
from snap7.util import *
import struct

def access_bit(data, num):
	base=int(num/8)
	shift = num%8
	return (data[base] & (1<<shift)) >> shift


plc = snap7.client.Client()

plc.connect("192.168.0.1",0,1)

db=plc.db_read(3,0,52)
d=struct.iter_unpack("!f",db[:52])
print( "3 x Real Vars:", [f for f, in d] )

db2=plc.db_read(3,204,4)
print(len(db2))

x=[access_bit(db2,i) for i in range(len(db2)*8)]
print(x)

#Get CPU INFO
x=plc.get_cpu_info()
print (x.ModuleTypeName)
print ("""CPU Information:
%s
Serial Number:
%s
AS Name:
%shift
Copy Right:
%s
Module Name:
%s
"""
%(x.ModuleTypeName.decode("utf-8"),
x.SerialNumber.decode("utf-8"),
x.ASName.decode("utf-8"),
x.Copyright.decode("utf-8"),
x.ModuleName.decode("utf-8")
)
)

value=195.9
valueinb=bytearray(struct.pack("f",value))
print(valueinb)
print(len(valueinb))

#try to shift the lsb and hsp
t=valueinb[0]
valueinb[0]=valueinb[3]
valueinb[3]=t

t1=valueinb[1]
valueinb[1]=valueinb[2]
valueinb[2]=t1

print('start to write..',value)
plc.db_write(3,0,valueinb)
print('data is write..')



plc.disconnect()