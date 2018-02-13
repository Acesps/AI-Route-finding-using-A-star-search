from math import sin, cos, sqrt, atan2, radians
import networkx as nx 
import xml.etree.cElementTree as ET
import cPickle as pickle



class MakeGraph:
	def save_Graph(self,Graphobject, filename):
		with open(filename, 'wb') as File:# Overwrites any existing file.
			pickle.dump(Graphobject, File, pickle.HIGHEST_PROTOCOL)

	def FindDistance(self,G,id1,id2):
		R = 6373.0
		lat1 = radians(float(G.node[id1]['lat']))
		lon1 = radians(float(G.node[id1]['lon']))
		lat2 = radians(float(G.node[id2]['lat']))
		lon2 = radians(float(G.node[id2]['lon']))
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a)) 
		return  R * c 

	def XMLParser(self):
		root = ET.parse(open("map.xml","r")).getroot()
		G=nx.Graph()
		for Node in root.findall('node'):
			id = Node.get('id')
			G.add_node(id,lat = Node.get('lat'))
			G.node[id]['lon'] = Node.get('lon')
			FLAG = 0;
			for tag in Node.findall('tag'):
				if(tag.get('k') == "name"):
					FLAG = 1;
					G.node[id]['name'] = tag.get('v')
					break
			if(not FLAG):
				G.node[id]['name'] = ''

		for way in root.findall('way'):
			route = way.findall('nd')
			for i in range(len(route)-1):
				id1 = route[i].get('ref')
				id2 = route[i+1].get('ref')
				distance = self.FindDistance(G,id1,id2)				
				G.add_edge(id1,id2,{'cost' : distance})
		self.save_Graph(G,'SAVED_GRAPH')

if __name__ == '__main__':
	c = MakeGraph();
	c.XMLParser();
