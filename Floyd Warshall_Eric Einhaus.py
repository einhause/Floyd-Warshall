#
#
#	Author: Eric Einhaus
#
#
import math
import copy

class WeightedAdjacencyMatrix :

    __slots__ = ['_W']


    def __init__(self, size) :
        """Initializes a weighted adjacency matrix for a graph with size nodes.

        Graph is initialized with size nodes and 0 edges.
        
        Keyword arguments:
        size -- Number of nodes of the graph.
        """
        
        self._W = list() #the list of lists
        for i in range(size) :
            row_i = list()
            for j in range(size) :
                if i == j : #diagonal 
                    row_i.append(0)
                else : #anything else
                    row_i.append(math.inf)
            self._W.append(row_i)
        
        
    def add_edge(self, u, v, weight) :
        """Adds a directed edge from u to v with the specified weight.

        Keyword arguments:
        u -- source vertex id (0-based index)
        v -- target vertex id (0-based index)
        weight -- edge weight
        """


        self._W[u][v] = weight


        
    def floyd_warshall(self) :
        """Floyd Warshall algorithm for all pairs shortest paths.

        Returns a matrix D consisting of the weights of the shortest paths between
        all pairs of vertices.  This method does not change the weight matrix of the graph itself.

        Extra Credit version: Returns a tuple (D, P) where D is a matrix consisting of the
        weights of the shortest paths between all pairs of vertices, and P is the predecessors matrix.
        """

        D = copy.deepcopy(self._W)
        n = len(D)
        

        for k in range(n) :
            for i in range(n) :
                for j in range(n) :
                    if D[i][j] > D[i][k] + D[k][j] :
                        D[i][j] = D[i][k] + D[k][j]
        return D
    
                                        
    
def haversine_distance(lat1, lng1, lat2, lng2) :
    """Computes haversine distance between two points in latitude, longitude.

    Keyword Arguments:
    lat1 -- latitude of point 1
    lng1 -- longitude of point 1
    lat2 -- latitude of point 2
    lng2 -- longitude of point 2

    Returns haversine distance in meters.
    """

    R = 6371000 #radius of the earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2-lat1)
    delta_lambda = math.radians(lng2-lng1)

    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d


#Graph data located under the 'simple graphs' from http://tm.teresco.org/graphs/

def parse_highway_graph_data(filename) :
    """Parses a highway graph file and returns a WeightedAdjacencyMatrix.

    Keyword arguments:
    filename -- name of the file.

    Returns a WeightedAdjacencyMatrix object.
    """
    latList = list() #list of V latitudes
    lngList = list() #list of V longitudes
    edgeList = list() #list of tuples with E from-to values
    V, E = 0, 0

    with open(filename) as f :
        f.readline() #skipping first line
        VE = f.readline().split(' ')
        V, E = VE[0], VE[1]
        for line in f :
            for i in range(0, int(V)) :
                IDLatLong = line.split(' ')
                lat = float(IDLatLong[1])
                latList.append(lat) #vertex ID is i, lat[i] is latitude
                lng = float(IDLatLong[2])
                lngList.append(lng) #vertex ID is i, lng[i] is longitude
                line = f.readline()
            for j in range(0, int(E)) :
                fromTo = line.split(' ')
                edgeList.append((fromTo[0], fromTo[1]))
                line = f.readline()

    G = WeightedAdjacencyMatrix(int(V))
    for i in range(0, len(edgeList)) :
        v1 = int(edgeList[i][0])
        v2 = int(edgeList[i][1])
        weight = haversine_distance(latList[v1], lngList[v1], latList[v2], lngList[v2])
        G.add_edge(v1, v2, weight)
        G.add_edge(v2, v1, weight)

    return G
    
        

def test_with_your_own_graphs() :

    m = WeightedAdjacencyMatrix(4) #initializes a WeightedAdjancencyMatrix with inf weight (besides the diagonal, with weight of 0)
    m.add_edge(1, 3, 5)
    m.add_edge(0, 1, 2)
    m.add_edge(0, 2, 4)
    m.add_edge(1, 2, -1)
    m.add_edge(3, 2, 6)
    m.add_edge(3, 0, 4)
    D = m.floyd_warshall()

    print("Weighted Adjacency Matrix")
    for i in range(len(D)) :
        for j in range(len(D)) :
            print(D[i][j], '\t', end=' ')
        print()


    

def test_with_highway_graph(L) :

    G = parse_highway_graph_data('aruba.txt') #name of text file goes on this line
    D = G.floyd_warshall()

    for i in range(len(D)) :
        for j in range(len(D)) :
            print(i, j, D[i][j], D[j][i], sep='\t')

if __name__ == "__main__":
    '''
        Aruba's graph has 28 vertices
    '''
    L = []
    for x in range(28) :
        for y in range(28) :
            L.append((x, y))
    test_with_highway_graph(L)
    

    

    
