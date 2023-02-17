"""
Antonio Bove
mat. 0622701898
"""

class NetworkFlow:

    """
    The NetworkFlow class represents an implementation of the Ford-Fulkerson algorithm 
    for finding the maximum flow in a flow network.
    """

    __slots__ = '_graph', '_source', '_sink'

    """
    This is the constructor of the class. It takes in a graph object and two optional 
    arguments representing the capacities of the edges from the source vertex s to the 
    other vertices, and from the other vertices to the sink vertex t, respectively. The 
    constructor inserts a source and a sink vertex into the graph and adds edges between 
    the source and the dominators, and between the dominated vertices and the sink.

    :param graph: the graph on which to build the flow network
    :param resCapSToN: the capacity of the edges from the source to the other vertices
    :param resCapNToT: the capacity of the edges from the other vertices to the sink

    Complexity: O(V), where V is the number of vertices in the graph. 
    """
    def __init__(self, graph, resCapSToN = 1, resCapNToT = 1):
        
        # Add source and sink vertices to the graph
        self._source = graph.insert_vertex('s')
        self._sink = graph.insert_vertex('t')

        # Add edges from source to dominators and from dominated to sink
        for v in graph.get_dominators().values():
            graph.insert_edge(self._source, v, resCapSToN)

        # Add edges from dominated to sink
        for v in graph.get_dominated().values():
            graph.insert_edge(v, self._sink, resCapNToT)

    """
    This method returns the source vertex of the flow network.

    Complexity: O(1)
    """
    def get_source(self):
        return self._source
    
    """
    This method returns the sink vertex of the flow network.

    Complexity: O(1)
    """
    def get_sink(self):
        return self._sink        
        
    """
    This method performs a modified version of a breadth-first search on the graph. It 
    starts from the source vertex and explores the graph level by level, marking the 
    vertices as discovered as it goes. The search stops when it reaches the sink vertex
    (with the additional condition that the edge has a weight > 0), or when it has explored 
    all reachable vertices.

    :param graph: the graph on which to perform the search 
    :param discovered: a dictionary mapping each vertex to the edge that was used to   

    Complexity: O(V + E), where V is the number of vertices (devices) and E is the number of 
                edges in the graph.
    """
    def bfs(self, graph, discovered):
        # First level includes only the source vertex
        level = [self._source]  
        while len(level) > 0:
            next_level = []  
            for u in level:
                for e in graph.incident_edges(u):  
                    # Consider only edges with positive residual capacity
                    if e.element() > 0:
                        v = e.opposite(u)
                        # Stop the search if the sink vertex is reached
                        if v is self._sink:
                            discovered[v] = e  
                            return True
                        # Otherwise, mark the vertex as discovered and add it to the next level
                        if v not in discovered:  
                            discovered[v] = e  
                            next_level.append(v)  
            level = next_level  
        
        return False

    """
    This method implements the Ford-Fulkerson algorithm for finding the maximum flow in the 
    flow network. It starts by calling the bfs method to find an augmenting path from the 
    source to the sink. It then decreases the flow along the path by the bottleneck unit and 
    increases the flow along the reverse edges by the same amount. This process is repeated 
    until there are no more augmenting paths. The final flow value is returned as the result.

    :param graph: the network flow on which to perform the maximum flow algorithm

    Complexity: Analytically, the Ford-Fulkerson algorithm has O(E*C) complexity, where E is the 
                number of edges of the graph and C is the maximum flow. In this case, we can rewrite 
                the complexity as O(E*V), where E is the number of edges in the graph and V is the 
                number of devices. 
                Particularly, the method repeatedly calls the 'bfs' method, which has a time complexity of O(V+E), 
                and updates the flow along the edges. The total number of times the bfs method is called is at most V,
                as each call can discover at least one new vertex.
    """
    def maxflow(self, graph):

        max_flow = 0

        # The discovery dictionary maps each vertex to the edge that was used to discover it
        discovery = {}
        # The source vertex is discovered using a dummy edge
        discovery[self._source] = None

        # Repeatedly perform breadth-first search to find an augmenting path
        while self.bfs(graph, discovery):
            
            # The bottleneck along the augmenting path is always 1 unit of flow beacuse the 
            # capacities of all the edges are at most 1. 
            bottleneck = 1
        
            max_flow += bottleneck

            # Update the flow along the path and the reverse edges
            edge = discovery.get(self._sink)
            while edge is not None:
                # Decrease the flow along the edge and increase the flow along the reverse edge 
                v1, v2 = edge.endpoints()
                edge.set_element(edge.element() - bottleneck)
                # If the reverse edge does not exist, create it
                if graph.get_edge(v2, v1) is None:
                    graph.insert_edge(v2, v1, 0)
                graph.get_edge(v2, v1).set_element(graph.get_edge(v2, v1).element() + bottleneck)
                # Move along the path
                edge = discovery.get(edge.get_origin())

            # Reset the discovery dictionary
            discovery = {}
            discovery[self._source] = None

        return max_flow