import snap7
import struct
from multiprocessing import Process
from config import xmlConfigRead
import logging,logging.config
from time import sleep as timer
import signal

#class of db mapping
class dbmap():
	def __init__(self,start,size):
		self.dbnumbers=3
		self.start=start
		self.size=size
		self.listarray=[]

class snap7client():
	def __init__(self,ip,rail,slot):
		self.ip=ip
		self.rail=rail
		self.slot=slot
		self.plc = snap7.client.Client()
		self.realdb=dbmap(0,52)
		self.booldb=dbmap(204,4)

	def makeconnection(self):
		self.plc.connect(self.ip,self.rail,self.slot)

	def realdataunpack(self,db):
		return struct.iter_unpack("!f",db[:self.realdb.size])

	def readRealArea(self):
		y=self.realdataunpack(self.plc.db_read(self.realdb.dbnumbers,self.realdb.start,self.realdb.size))
		self.listarray= [f for f, in y]
		return self.listarray

	def destoryconnect(self):
		self.plc.destroy()

	def sendData(self,start,value):
		self.plc.db_write(self.realdb.dbnumbers,start,self.realswaptoByteArray(value))

	def realpacktoByteArray(self,value):
		return bytearray(struct.pack("f",value))

	def realswaptoByteArray(self,valueinb):
		t=self.realpacktoByteArray(valueinb)
		t1=t   
		t1[0]=t[3]
		t1[1]=t[2]
		t1[2]=t[1]
		t1[3]=t[0]
		return t1

	def readBoolArea(self):
		db2=self.plc.db_read(3,204,4)
		x=[self.booldataunpack(db2,i) for i in range(len(db2)*8)]
		print(x)

	def booldataunpack(self,data,num):
		base=int(num/8)
		shift = num%8
		return (data[base] & (1<<shift)) >> shift

class tag():
	def __init__(self,tagname,value):
		self.tagname=tagname
		self.value=value

	def gettagname(self):
		return self.tagname
	def printvalue(self):
		print(self.value)

class realtag(tag):
	def __init__(self,tagname,value=0.0):
		tag.__init__(self,tagname,value)


class Booltag(tag):
	def __init__(self,tagname,value=False):
		tag.__init__(self,tagname,value)
		self.dbx=dbx

class realtaglist():
	def __init__(self):
		self.reallist=[]
	def addelements(self,realtag):
		self.reallist.append(realtag)

class Booltaglist():
	def __init__(self):
		self.Boollist=[]
	def addelements(self,Booltag):
		self.Boollist.append(Booltag)	

def Dummy():
	pass

if __name__=='__main__':
	plc1=snap7client(ip='192.168.0.1',rail=0,slot=1)
	plc1.makeconnection()
	plc1.sendData(20,20.0)

	plc1.readBoolArea()

	a=[]
	plist=realtaglist()
	blist=Booltaglist()

	test1=xmlConfigRead.XMLConfiger()

	#make a dummylist
	q=0


	for i in range(0,2):
		templist=test1.getNodeList()	
		for j in range(0,len(templist[i])):
			plist.addelements(realtag(tagname=templist[i][j],value=0))
			q+=1
		a.append(plist)
		plist=realtaglist()

	logging.config.fileConfig('logging.conf')
	gtlogger=logging.getLogger('Temperature')
	mtlogger=logging.getLogger('Motor')
	r=logging.getLogger('root')
	print(q)

	while True:
		xx=plc1.readRealArea()
		q=0
		for i in range(0,2):
			templist=test1.getNodeList()	
			for j in range(0,len(templist[i])):
				msg=a[i].reallist[j].gettagname()+'/'+str(xx[q])
				q+=1
				if i==0:
					gtlogger.info(msg)
				elif i==1:
					mtlogger.info(msg)
		r.info('data logged')		
		timer(1)





