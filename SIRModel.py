import snap
import random

# load graph
LoadedGraph = snap.LoadEdgeList(snap.PNGraph, "./facebook_combined.txt")

snap.PrintInfo(LoadedGraph)

# constants
susceptible = []
infectious = []
removed = []
contagionProbability = 1
totalTimestep = 100
infectiousPeriod = 2

# infectious element with infectious period
class infectedElement:
    def __init__(item, id):
        item.id = id
        item.time = infectiousPeriod
    
    def dec(item):
        item.time = item.time - 1

# SIR model

# add all nodes into susceptible
for NI in LoadedGraph.Nodes():
    susceptible.append(NI.GetId())

# generate random node id to start the transmission
randomNodeId = random.randrange(0,LoadedGraph.GetMxNId())
print("random node no is", randomNodeId)
firstInfected = infectedElement(randomNodeId)
susceptible.remove(randomNodeId)
infectious.append(firstInfected)
tempInfectious = []

print("At time 0")
print("no of sus", len(susceptible))
print("no of inf", len(infectious))
print("no of removed", len(removed))

# perform t updates to the graph
for t in range(totalTimestep):

    # change from suceptible to infectious
    for infected in infectious:
        for x in range(LoadedGraph.GetNI(infected.id).GetOutDeg()):
            if random.uniform(0,1) < contagionProbability:
                if LoadedGraph.GetNI(infected.id).GetOutNId(x) in susceptible:
                    tempInfectious.append(LoadedGraph.GetNI(infected.id).GetOutNId(x))
                    susceptible.remove(LoadedGraph.GetNI(infected.id).GetOutNId(x))
    for id in tempInfectious:
        infectedItem = infectedElement(id)
        infectious.append(infectedItem)
    tempInfectious.clear()

    # change from infectious to removed and decrease infectious time stamp
    for infected in infectious:
        if infected.time == 0:
            removed.append(infected.id)
            infectious.remove(infected)
        infected.dec()

    print("At time", t+1)
    print("no of sus", len(susceptible))
    print("no of inf", len(infectious))
    print("no of removed", len(removed))
    
    
            



