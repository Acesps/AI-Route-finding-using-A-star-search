import networkx as nx 
from MakeGraph import MakeGraph
import cPickle as pickle

class FindRoute:
	def Read_graph(self,filename):
		with open(filename, 'rb') as input:
			G = pickle.load(input)
			return G
	def Astar(self,G,start_point,destination):
		start = start_point
		end   = destination
		open = []
		closed = []



if __name__ == '__main__':
	#should parse?
	MakeGraph().XMLParser();
	#
	G = FindRoute().Read_graph("SAVED_GRAPH")
	start_point = G.node['1']
	destination = G.node['10']
	route =	FindRoute().Astar(G,start_point,destination); 