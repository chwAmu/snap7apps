import xml.etree.ElementTree as ET

def XMLImport(path):
	return ET.parse(path)

def getrootfromXML(tree):
	return tree.getroot()

def listReturn():
	Record1=list()
	Record=list()

	root=getrootfromXML(XMLImport('config\machine.xml'))
	# from config import logCtrl
	# logCtrl.printTerminalMessage("Data is starting to import.")
	#get xml top tag
	# print(root.tag)
	#get elemnets
	for elemnet in root:
		Record.append(elemnet.attrib['name'])

	for x in root.findall('loggingRecord'):
		d={}
		#get the logging label and logging tag node id
		for p in x.findall('point'):
			#get the logging label
			label=p.text
			#get the logging node id
			nodeid=p.get('NodeID')
			#group-up these two elements into a dictionary
			d[label]=nodeid
		#group-up a whole logging Record into a array element
		Record1.append(d)

	
	q=list()
	print('-------logging Structure-------')
	for i in range(0,4):
		k={}
		k[Record[i]]=Record1[i]
		q.append(k)

	import pprint
	pp=pprint.PrettyPrinter()
	pp.pprint(q)
	print('------------End-------------')
	# logCtrl.printTerminalMessage("Data is imported.")
	return q

