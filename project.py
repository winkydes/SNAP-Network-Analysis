import snap

# create a graph TNGraph
G1 = snap.TNGraph.New()
G1.AddNode(1)
G1.AddNode(5)
G1.AddNode(32)
G1.AddEdge(1,5)
G1.AddEdge(5,1)
G1.AddEdge(5,32)
print("G1: Nodes %d, Edges %d" % (G1.GetNodes(), G1.GetEdges()))