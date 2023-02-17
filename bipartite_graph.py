"""
Antonio Bove
mat. 0622701898
"""

from TdP_collections.graphs.graph import Graph

class BipartiteGraph(Graph):

    """
    The BipartiteGraph class is derived from the Graph class and adds two additional 
    instance variables: '_dominators' and '_dominated'. These dictionaries store the 
    vertices in the two disjoint sets of the bipartite graph, with the keys being the 
    elements of the vertices and the values being the vertex objects themselves.
    """

    __slots__ = '_dominators', '_dominated'

    #------------------------- nested Edge class --------------------------------
    class Edge(Graph.Edge):

        """
        Nested Edge class that extends the Edge class of the base Graph class with 
        'set_element' and 'get_origin' methods. The 'set_element' method allows the 
        element of an edge to be modified, while the 'get_origin' method returns the 
        origin vertex of the edge.
        """
        
        """
        Set element associated with this edge.

        :param x: the element to associate with this edge

        Complexity: O(1)
        """
        def set_element(self, x):
            self._element = x
        
        """
        Returns the value of the instance variable '_origin' of the edge.

        Complexity: O(1)
        """
        def get_origin(self):
            return self._origin

    #------------------------- Graph methods -------------------------------------
    """
        Create an empty bipartite graph (directed, by default).
        Graph is undirected if optional paramter is set to False.

        Complexity: O(1)
    """
    def __init__(self, directed=True):
        super().__init__(directed)
        self._dominators = {}
        self._dominated = {}
    
    """
    This method inserts a pair of vertices into the bipartite graph, one for each 
    of the disjoint sets. The vertices are inserted with the same element x. The 
    method returns the two vertex objects.
    
    :param x: the element to associate with the new vertices

    Complexity: O(1) expected 
    """
    def insert_double_vertex(self, x):
        # Insert the two vertices into the graph
        sx_vertex = super().insert_vertex(x)
        dx_vertex = super().insert_vertex(x)

        # Insert the two vertices into the dictionaries
        self._dominators[sx_vertex.element()] = sx_vertex
        self._dominated[dx_vertex.element()] = dx_vertex

        return sx_vertex, dx_vertex
    
    """
    This method returns the '_dominators' dictionary of the bipartite graph.

    Complexity: O(1)
    """
    def get_dominators(self):
        return self._dominators
    
    """
     This method returns the '_dominated' dictionary of the bipartite graph.

    Complexity: O(1)
    """
    def get_dominated(self):
        return self._dominated