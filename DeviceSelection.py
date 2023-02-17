"""
Antonio Bove
mat. 0622701898
"""

from bipartite_graph import BipartiteGraph
from network_flow import NetworkFlow

class DeviceSelection:

    __slots__ = "_stringsTuple", "_partitions", "_maxFlow", "_graph", "_network_flow", '_generators'

    def __init__(self, N, X, data):

        """
        This is the constructor of the class. It takes in three arguments: 
            - N, a tuple of strings identifying the devices; 
            - X, an integer;
            - data, a dictionary whose keys are the elements of N, and whose values are 
              tuples of X-2 elements describing the performances of the corresponding 
              device over sentences from 3-term to X-term.
        The constructor first creates the bipartite graph by calling the '_createGraph' 
        method.Then it creates a NetworkFlow object and calculates the maximum flow in the 
        graph using the 'maxflow' method of the NetworkFlow class. Subsequently, it calls the 
        '_createPartitions' method to create a list of lists containing the devices that 
        belong to the same partition and for which the no-interleaving property holds.
        Finally, it creates a list of generators, one for each partition, that will be used   
        to iterate over the devices in each partition. 

        Complexity: O(N^2 * X) 
        """

        self._stringsTuple = N

        self._graph = self._createGraph(N, X, data) #O(N^2 * X)

        self._network_flow = NetworkFlow(self._graph) # O(N)

        self._maxFlow = self._network_flow.maxflow(self._graph) #(E*N)
        
        self._createPartitions() # O(N+E)

        # We create a list of generators, one for each partition, that will be used to iterate over the devices in each partition
        self._generators = [None] * self.countDevices()
        for i in range(self.countDevices()): # O(N)
            self._generators[i] = self._createGenerator(i)
        

    def countDevices(self):
        """
        Returns the minimum number of subsets in which the devices are partitioned so that 
        every subset satisfies the non-interleaving property. 
        This value can be obtained by subtracting the value of the maximum flow from the 
        total number of devices. This is because the maximum flow tells us how many devices 
        are dominated and if we subtract this value from the total number of devices, we get 
        the devices that dominate, i.e. the heads of the partitions and therefore the number 
        of partitions.

        Complexity: O(1)
        """

        return len(self._stringsTuple) - self._maxFlow

    def nextDevice(self,i):
        """
        Takes in input an integer i between 0 and C-1 (C is the number of subsets in which
        the devices are partitioned), and returns the string identifying the device with 
        highest rank in the i-th subset that has been not returned before, or None if no 
        further device exists. The method throws an exception if the value in input is not 
        in the range [0, C-1]

        Complexity: O(1)
        """
        # If the input is not in the range [0, C-1], we raise an exception
        if i < 0 or i >= len(self._partitions):
            raise Exception("Invalid subset index")
        try:
            # We return the next device in the i-th partition
            return next(self._generators[i])
        except StopIteration:
            # If there are no more devices in the i-th partition, we create a new generator for that partition
            self._generators[i] = self._createGenerator(i)
            return None
    
    def _createGenerator(self, index):
        """
        This method creates a generator that iterates through the devices in the i-th partition.

        :param index: the index of the partition

        Complexity: O(1)
        """

        # The generator iterates through the devices in the i-th partition
        yield from self._partitions[index]


    def _createGraph(self, N, X, data):
        """
        This method creates a bipartite graph with N nodes on each side, with an edge between 
        node i and node j only if i represents a device that dominates the device represented by j.

        Complexity: O(N^2 * X)
        """
        graph = BipartiteGraph()
        
        for device in enumerate(N):
            graph.insert_double_vertex(device[1])
        
        for i, dominator in enumerate(N):
            for j, dominated in enumerate(N):
                # If the devices are the same, we skip the iteration
                if i == j:
                    continue
                # If the devices are not the same, we check if the first device dominates the second one 
                dominates = True
                for k in range(2, X):
                    # If the first device does not dominate the second one, we break the loop and move on to the next iteration
                    if data[dominator][k - 2] <= data[dominated][k - 2]:
                        dominates = False
                        break
                if dominates:
                    # The weight of each edge is set to 1 in anticipation of the subsequent construction of the flow network
                    graph.insert_edge(graph.get_dominators()[dominator], graph.get_dominated()[dominated], 1) 

        return graph

    
    def _isLeader(self, device):
        """
        This method returns True if the given device is a leader (i.e., it is the device that dominates 
        all other devices in its partition), and False otherwise. It does this by checking that there is
        no flow from the respective device in the dominated set to the sink vertex in the flow network, 
        because if there was flow it means that there is another leader who dominates the given input device.

        :param device: the device to check

        Complexity: O(1) expected
        """
        return self._graph.get_edge(self._graph.get_dominated()[device], self._network_flow.get_sink()).element() != 0
    

    def _createPartitions(self):
        """
        This method creates a list of lists containing the devices which belong to the same partition. 
        It does this by iterating through the dominators dictionary of the graph. If a dominator is a 
        leader (as determined by the '_isLeader' method), a new partition is created and the leader device 
        is added to it. The method then follows the edges from the leader to find all the other devices 
        that are dominated by him and adds them to the partition as well. This process is repeated until 
        all partitions have been created.

        Complexity: O(N + E), where N is the number of vertices (devices) and E is the number of 
                    edges in the graph.
        """

        # Create a list of lists, one for each partition 
        self._partitions = [[] for _ in range(len(self._stringsTuple) - self._maxFlow)] 

        partitionNumber = 0 

        # Iterate through the dominators dictionary of the graph 
        for key, value in self._graph.get_dominators().items(): 
            
            if self._isLeader(key): 
                
                # If the device is a leader, add it to the current partition
                self._partitions[partitionNumber].append(key)

                opposite = value

                # Follow the edges from the leader to find all the other devices that are dominated by him
                while True:  
                    
                    for edge in self._graph.incident_edges(opposite): 

                        # If the edge has no flow, it means that the device at the other end of the edge is dominated by the leader
                        if edge.element() == 0:
                            opposite = self._graph.get_dominators()[edge.opposite(opposite).element()]
                            self._partitions[partitionNumber].append(opposite.element())
                            break 
                    else:
                        # No more edges to follow, so we have found all the devices in the partition 
                        break 

                partitionNumber += 1