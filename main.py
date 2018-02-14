import networkx as nx 
from MakeGraph import MakeGraph
import cPickle as pickle
import Queue as Q  # ver. < 3.0

class FindRoute:
	def Read_graph(self,filename):
		with open(filename, 'rb') as input:
			G = pickle.load(input)
			return G
	def Astar(self,G,start_point,destination):
		start = start_point
		end   = destination
		open = Q.PriorityQueue()
		open.put((0.0,start))#F(),ID
		closed = []
		while not open.empty():
			tup = open.get();
			if tup[1] == end:
				break
			parent = tup[1]
			for next in G.neighbors(parent):
				
				new_G = G.node[parent]['G'] + float(G.edge[parent][next]['cost'])
				new_H = self.FindH(next,end)
			#pop with min H 

if __name__ == '__main__':
	#should parse?
	MakeGraph().XMLParser();
	#
	G = FindRoute().Read_graph("SAVED_GRAPH")
	start_point = '1'
	destination = '10'
	route =	FindRoute().Astar(G,start_point,destination); 