import networkx as nx 
from MakeGraph import MakeGraph
import cPickle as pickle
import requests

class FindRoute:
	def Read_graph(self,filename):
		with open(filename, 'rb') as input:
			G = pickle.load(input)
			return G
	def Display(self,G,route):
		for point in route:
			A = "Go to node " + point + " at " + G.node[point]['lat'] + "," + G.node[point]['lon']
			B = ""
			if G.node[point]['name']:
				B = " also known as" + G.node[point]['name']
			print A + B 
	def FindH(self,start,end):
		#key = 'AIzaSyDyMGJZJ7al3c5R0lcNAgupvury2ivzlpM'
		key = 'AIzaSyCazRdAPV0hyFjXZZsyAyOLExLdkRLlTVk'
		origin = G.node[start]['lat'] + "," + G.node[start]['lon']
		destination = G.node[end]['lat'] + "," + G.node[end]['lon'] 
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+origin+'&destinations='+destination+'&key='+key
		api_return = requests.get(url)
		resp = api_return.json()
		distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])/1000;
		return distance

	def Astar(self,G,start_point,destination):
		start = start_point
		end   = destination
		opened = set()
		closed = set()
		opened.add(start)
		G.node[start]['G'] = 0.000001
		while opened:
			current = min(opened, key=lambda id:G.node[id]['G'] + G.node[id]['H'])
			if current == end:
				route = []
				while G.node[current]['parent'] :
					route.append(current)
					current = G.node[current]['parent']
				route.append(current)
				return route[::-1]
			opened.remove(current)
			closed.add(current)
			for next in G.neighbors(current):
				new_G = G.node[current]['G'] + float(G.edge[current][next]['cost'])
				new_H = G.node[next]['H'];
				if G.node[next]['G'] == 0.0:
					new_H = self.FindH(next,end)
				elif(G.node[next]['G'] < new_G):
					continue;
				G.node[next]['G'] = new_G
				G.node[next]['H'] = new_H
				G.node[next]['parent'] = current
				if next in closed:
					closed.remove(next)
				opened.add(next)
		#size of open is 0
if __name__ == '__main__':
	choice = raw_input("Do you want to parse the Graph from map.xml?(Yes/No)")
	if(choice == "Yes"):
		MakeGraph().XMLParser();
		print "Parsing completed"

	
	G = FindRoute().Read_graph("SAVED_GRAPH")
	
	start_point = '2177311098'
	destination = '2177311054'
	route =	FindRoute().Astar(G,start_point,destination); 
	FindRoute().Display(G,route);  