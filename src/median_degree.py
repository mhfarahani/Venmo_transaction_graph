#import pdb
import sys
import json
import datetime
import time
import heapq
import numpy as np
#import matplotlib.pylab as plt

class Vertex(object):
    ''' This class creates vertex objects of the graph class.
    key: the vertex id
    connections: a list of vertices that are connected to the currebt 
                 vertex
    '''
    def __init__(self,key):
        self.id = key
        self.connections ={}

    def addConnection(self,v,tstmp=0):
        '''Adds a connection from one vertex to another'''
        self.connections[v] = tstmp
        return True

    def getConnection(self):
        '''Returns all the vertices in the adjacency list'''
        return self.connections.keys()

    def isConnection(self,v):
        '''Checks if the current vortex and v are connected '''
        if v in self.connections:
           return True
        else:
           return False

    def getId(self):
        '''Returns vortex id'''
        return self.id

    def getWeight(self,v):
        '''Returns weight of an edge between the current vertex and v'''
        return self.connections[v]

    def getDegree(self):
        '''Returns degree of vertex (the number of neighbouring vertices'''
        return len(self.connections)

    def delConnection(self,v):
        '''Removes the connectivity between vertices'''
	if v in self.connections:
	    del(self.connections[v])
	    return True
	else:
  	    raise KeyError('%s is not connected to %s' % (v.getId(),self.getId()))

    def __del__(self):
	class_name = self.__class__.__name__

class Graph(object):
    ''' Graph class (Type: Adjacency list)
    graph_size: Number of vertices in the graph
    vertex_list: A dictionary of all the vertices in the graph.
    '''
    def __init__(self):
        self.vertex_list = {}
        self.graph_size = 0

    def addVertex(self,key):
        ''' Adds new vertex into the graph'''
        if key not in self.vertex_list:
            self.vertex_list[key] = Vertex(key)
            self.graph_size += 1
        return True

    def getVertex(self,key):
        ''' Given a vertex key, the vertex will be returned '''
        if key in self.vertex_list.keys():
            return self.vertex_list[key]
        else:
            raise KeyError('%s does not exist' % key)

    def addEdge(self,v1,v2,tstmp=0):
        ''' Sets up an edge between v1 and v2 vertices'''
        if v1 not in self.vertex_list.keys():
            self.addVertex(v1)
        if v2 not in self.vertex_list.keys():
            self.addVertex(v2)
        self.getVertex(v1).addConnection(self.getVertex(v2),tstmp)
        self.getVertex(v2).addConnection(self.getVertex(v1),tstmp)
        
    def getVertices(self):
        ''' Returns all the vertices in the graph'''
        return self.vertex_list.keys()

    def printEdges(self):
        ''' Prints all distinct edges in the graph'''
        temp = {}
        for v in self.vertex_list.values():
            temp.add(v.getId())
            for w in v.getConnection():
                if w.getId() in temp:
                    continue
                print("( %s , %s , %s )" % (v.getId(), w.getId(), v.getWeight(w)))
   
    def getDegrees(self):
        ''' Returns a list of all the vertex degrees'''
        degrees = []
	for v in self.vertex_list.values():
            degrees.append(v.getDegree())
        return degrees

    def getWeight(self,v1,v2):
        ''' Returns weight of an edge between v1 and v2 vertices'''
        return self.getVertex(v1).getWeight(self.getVertex(v2))

    def edgeExist(self,v1,v2):
        ''' Checks if an edge exist between v1 and v2 vertices.'''
        return self.getVertex(v1).isConnection(self.getVertex(v2))

    def delVertex(self,key):
        ''' Removes a vertex from the graph'''
	if key not in self.vertex_list.keys():
	    raise KeyError('%s does not exist' % key)
	else:
	    del self.vertex_list[key]
	    return True
	    
    def delEdge(self,v1,v2):
        ''' Delets the edge between v1 and v2 vertices'''
	self.vertex_list[v1].delConnection(self.vertex_list[v2])
	self.vertex_list[v2].delConnection(self.vertex_list[v1])
	if len(self.vertex_list[v1].connections) == 0:
	    del self.vertex_list[v1]
	if len(self.vertex_list[v2].connections) == 0:
	    del self.vertex_list[v2]
        return True
 

class DataStorage(object):
    ''' This class stors edges of the graph in a dictionary. The timestamps are 
	used as the key of dictionary and all edges with the same timestamp are   
	added to a set under the same key.In a set, add() and remove() are O(1).  
        Moreover, set avoids storing duplicated edges with a same timestamp in 
        the dictionary. Using the timestamps as the dict keys allow us to find
        the set of all the payments of the timestamp in O(1).
    '''  
    def __init__(self):
	self.data = {}

    def getKeys(self):
	return self.data.keys()

    def keyExist(self,key):
        '''Returns the keys (timestamps) of data structure '''
	if key in self.getKeys():
	    return True
	else:
	    return False

    def addData(self,key,edge):
        ''' Adds data into the data structure'''
	if self.keyExist(key):
	    self.data[key].add(edge)
	else:
	    self.data.update({key:{edge}})
	return True

    def removeData(self,key,edge):
        '''Removes data from data structure'''
	if self.keyExist(key):
           if edge in self.data[key]:
	       self.data[key].remove(edge)
               return True
           else:
               self.data[key].remove(edge[::-1])
               return True
        return False

    def popData(self,key):
        '''Pops data from data structure'''
        if self.keyExist(key):
            return self.data[key].pop()
        return False

    def isSetEmpty(self,key):
        '''Returns True if the set data structure under a key is empty'''
	if len(self.data[key]) == 0:
	    return True
	else:
	    return False

    def delKey(self,key):
        '''Removes a key from dictionary if the related set is empty'''
        if self.keyExist(key):
            if self.isSetEmpty(key):
                del(self.data[key])
                return True
            else:
                print('Warning: key is not empty! No action performed')
                return False
        else:
            print('Warining: Key does not exist')
            return False

def DateTime_Parser(t):
    '''Converts Json date/time into python date/time  '''
    return time.mktime(datetime.datetime.strptime(t,r'%Y-%m-%dT%H:%M:%SZ').timetuple())

def MaintainTSecData(agraph,data,alist,ctime,T):
    '''Removes transations that occured T sec older than the current time'''
    del_list = [] 
    for tstmp in alist:
        if ctime - tstmp >= T:
            while not data.isSetEmpty(tstmp):
                v1,v2 = data.popData(tstmp)
                agraph.delEdge(v1,v2)
            del_list.append(tstmp)
        else:
            break
    if len(del_list):
        for tstmp in del_list:
            data.delKey(tstmp)
            heapq.heappop(alist)

def Get_Median(agraph):
    '''Returns the median of the degrees of graph'''
    return np.median(np.array(agraph.getDegrees()))


def Read_DataStream(time_period,input_path,output_path):
    JSON_file = open(input_path,'r')
    outputfile = open(output_path,'w')
    graph = Graph()
    data = DataStorage()
    heap = []
    current_time = 0
    for line in JSON_file:
        theJson = json.loads(line)
        tstmp =  theJson['created_time']
        actor = theJson['actor']
        target = theJson['target']
        if actor == '' or target == '' or tstmp == '':
            continue
        transaction_time = DateTime_Parser(tstmp)
        if transaction_time > current_time:
            current_time = transaction_time
            heapq.heappush(heap,current_time)
        elif (current_time - transaction_time) >= time_period:
            outputfile.write('%.2f\n' % Get_Median(graph))
            continue
        graph.addVertex(actor)
        graph.addVertex(target)
        if graph.edgeExist(actor,target):
           existing_tstmp = graph.getWeight(actor,target)
           if existing_tstmp != transaction_time:
               flag = data.removeData(existing_tstmp,(actor,target))
        data.addData(transaction_time,(actor,target))
        graph.addEdge(actor,target,transaction_time)
        MaintainTSecData(graph,data,heap,current_time,time_period)
        outputfile.write('%.2f\n' % Get_Median(graph))
    JSON_file.close()
    outputfile.close()

def main():
     'This code parse the data from a stream of venmo transations and'
     'creats a graph for the transation within the last T sec (defult'
     'T = 60 sec). It returns the median of the graph degrees. '
     args = sys.argv[1:]
 
     input_path = args[0]
     output_path = args[1] 
     time_window = 60
     Read_DataStream(time_window,input_path,output_path)

if __name__ == '__main__':
    main()
