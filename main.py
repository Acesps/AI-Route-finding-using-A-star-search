import networkx as nx 
from MakeGraph import MakeGraph
import cPickle as pickle
import requests

class FindRoute:
	def Read_graph(self,filename):
		with open(filename, 'rb') as input:
			G = pickle.load(input)
			return G

	def FindH(self,start,end):
			key = 'AIzaSyDyMGJZJ7al3c5R0lcNAgupvury2ivzlpM'
			origin = G.node[start]['lat'] + "," + G.node[start]['lon']
			destination = G.node[end]['lat'] + "," + G.node[end]['lon'] 
			url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+origin+'&destinations='+destination+'&key='+key
			api_return = requests.get(url)
			resp = api_return.json()
			print " api_return "
			#print resp
			distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])/1000;
			print distance
			return distance

	def Astar(self,G,start_point,destination):
		start = start_point
		end   = destination
		opened = set()
		closed = set()
		opened.add(start)
		G.node[start]['G'] = 0.000001
		print start + " " + end
		while opened:
			current = min(opened, key=lambda id:G.node[id]['G'] + G.node[id]['H'])
			print	" current is " + current
			if current == end:
				route = []
				while G.node[current]['parent'] :
					route.append(current)
					print current + " is current"
					print G.node[current]['parent'] + " is parent"
					current = G.node[current]['parent']
				route.append(current)
				return route[::-1]
			opened.remove(current)
			closed.add(current)
			print "opened is"
			print opened
			print "closed is "
			print closed
			print "neighbors are" 
			print G.neighbors(current)
			for next in G.neighbors(current):
				new_G = G.node[current]['G'] + float(G.edge[current][next]['cost'])
				print "new_G for" + next + " is " + str(new_G)
				new_H = G.node[next]['H'];
				if G.node[next]['G'] == 0.0:
					new_H = self.FindH(next,end)
					print " new_H" + str(new_H)
				elif(G.node[next]['G'] < new_G):
					continue;
				G.node[next]['G'] = new_G
				G.node[next]['H'] = new_H
				G.node[next]['parent'] = current
				print "parent is " + current
				if next in closed:
					closed.remove(next)
				opened.add(next)
		#size of open is 0
		print "No Path Found"
if __name__ == '__main__':
	#should parse?
	#MakeGraph().XMLParser();
	#
	G = FindRoute().Read_graph("SAVED_GRAPH")
	start_point = '1'
	destination = '10'
	print G.nodes()
	print G.edges()
	route =	FindRoute().Astar(G,start_point,destination); 
	print route