import networkx as nx 
from MakeGraph import MakeGraph
import cPickle as pickle
import requests
import gmplot

class FindRoute:
	def Read_graph(self,filename):
		'''
		This fuction uses Pickle to write a python object to file
		'''

		with open(filename, 'rb') as input:
			G = pickle.load(input)
			return G

	def Display(self,G,route):
		'''
		This Function Displays the Route on terminal
		'''
		lat = []
		lon = [] 

		# Transform the the fetched latitude and longitude data into two separate lists
		for point in route:
			lat.append(float(G.node[point]['lat']))
			lon.append(float(G.node[point]['lon']))
		# Initialize the map to the first location in the list
		gm = gmplot.GoogleMapPlotter(lat[0], lon[0], 10)
		# /usr/local/lib/python3.5/dist-packages/gmplot/markers/
		gm.plot(lat, lon, '#FF6666', edge_width=10)
		# Write the map in an HTML file
		gm.draw('map.html')
		for point in route:
			A = "Go to node " + point + " at " + G.node[point]['lat'] + "," + G.node[point]['lon']
			B = ""
			if G.node[point]['name']:
				B = " also known as" + G.node[point]['name']
			print A + B 
	def FindH(self,start,end):
		'''
		This function uses distancematrix Api to find distance between two nodes
		'''
		#key = 'AIzaSyDyMGJZJ7al3c5R0lcNAgupvury2ivzlpM'
		#key = 'AIzaSyCazRdAPV0hyFjXZZsyAyOLExLdkRLlTVk'
		#key = 'AIzaSyDnD1fg0ljZUTEhrg8txoT36vJLbkgWX6k'
		key = 'AIzaSyD-yEDz5znPN4ShxDUTuocXl-XDTu33ZVc'
		origin = G.node[start]['lat'] + "," + G.node[start]['lon']
		destination = G.node[end]['lat'] + "," + G.node[end]['lon'] 
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+origin+'&destinations='+destination+'&key='+key
		api_return = requests.get(url)
		resp = api_return.json()
		distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])/1000;
		return distance

	def Astar(self,G,start_point,destination):
		'''
		This function is an implementation of A* algorithm
		'''
		start = start_point
		end   = destination
		opened = set()
		closed = set()
		opened.add(start)
		#just putting a non-zero value, avoiding infinite loop
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
			#checking for all the successors 
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
		print "NO Path Found"

if __name__ == '__main__':
	#No need to parse Every time
	choice = raw_input("Do you want to parse the Graph from map.xml?(Yes/No)")
	if(choice == "Yes"):
		MakeGraph().XMLParser();
		print "Parsing completed"

	#Reading Graph
	G = FindRoute().Read_graph("SAVED_GRAPH")
	
	#static Points 
	start_point = '2803176462'
	destination = '4185292728'
	
	
	route =	FindRoute().Astar(G,start_point,destination);
	FindRoute().Display(G,route);

