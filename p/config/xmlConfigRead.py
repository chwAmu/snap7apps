from config.read import nodeid

class XMLConfiger():

	def __init__(self):
		self.Taglist=nodeid.listReturn()
		self.LoggingRecordCaterlogs=self.setLoggingRecordCaterlogs()
		self.LoggingRecordTagList=self.setLoggingRecordTagList()
		self.NameList=self.setNameList()
		self.NodeIdList,self.NodeIdNameList=self.setNodeList()

	def setLoggingRecordCaterlogs(self):
		LoggingRecordCaterlogs=[]
		taglist=self.getLoggingTagsList()
		for x in taglist:
			for k in x:
				LoggingRecordCaterlogs.append(k)
		return LoggingRecordCaterlogs		

	def setLoggingRecordTagList(self):
		LoggingRecordTagList={}
		taglist=self.getLoggingTagsList()
		configLen=self.getLoggingRecordCaterlogsLen()
		for x in range(configLen):
			for k,v in taglist[x][self.LoggingRecordCaterlogs[x]].items():
				LoggingRecordTagList[k]=v		
		return LoggingRecordTagList	

	def setNameList(self):
		taglist=self.getLoggingTagsList()
		NameList=[]
		configLen=self.getLoggingRecordCaterlogsLen()

		for x in range(configLen):
			NameList.append(str(taglist[x].keys()).replace('dict_keys([',"").replace('])',"").replace(r"'",''))
		return NameList

	def getNameList(self):
		return self.NameList

	def setNodeList(self):
		taglist=self.getLoggingTagsList()
		nameList=self.getNameList()
		NodeIdList=[]
		NodeIdNameList=[]
		configLen=self.getLoggingRecordCaterlogsLen()
		for x in range(configLen):
			tempidlist=[]
			tempnamelist=[]
			for k,v in taglist[x][nameList[x]].items():
				tempidlist.append(k)
				tempnamelist.append(v)
			NodeIdList.append(tempidlist)
			NodeIdNameList.append(tempnamelist)
		return NodeIdList,NodeIdNameList

	def getNodeList(self):
		return self.NodeIdList
	def getNodeNamelist(self):
		return self.NodeIdNameList

	def printLoggingRecordCaterlogs(self):
		return self.LoggingRecordCaterlogs

	def getLoggingRecordCaterlogsLen(self):
		return len(self.LoggingRecordCaterlogs)

	def getLoggingTagsList(self):	
		return self.Taglist
	def getLoggingRecordTagList(self):
		return self.LoggingRecordTagList
	

if __name__=='__main__':
	x=XMLConfiger()
	print(x.getNameList())
	print(x.getNodeList())
	print(x.getNodeNamelist())
	# print(x.getLoggingRecordTagList())

