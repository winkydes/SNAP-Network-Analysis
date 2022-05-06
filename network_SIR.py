from sqlite3 import Timestamp
import snap
import random
import pandas as pd
from openpyxl import load_workbook

book = load_workbook('network_SIR.xlsx')
writer = pd.ExcelWriter('network_SIR.xlsx', engine='openpyxl') 
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

# load graph
LoadedGraph = snap.LoadEdgeList(snap.PNGraph, "./facebook_combined.txt")

snap.PrintInfo(LoadedGraph)

# constants
susceptible = []
infectious = []
removed = []
contagionProbability = 0.5
totalTimestep = 50
infectiousPeriod = 5

# infectious element with infectious period
class infectedElement:
    def __init__(item, id):
        item.id = id
        item.time = infectiousPeriod
    
    def dec(item):
        item.time = item.time - 1

# SIR model

# generate random node id to start the transmission
# randomNodeId = random.randrange(0,LoadedGraph.GetMxNId())
# print("random node no is", randomNodeId)
df = pd.DataFrame(columns=['id','outDegree', 'stopTime'])

test = []
for i in range(0,200):
    test.append(random.randrange(0,LoadedGraph.GetMxNId()))
test.sort()

outDegree = []
for item in test:
    outDegree.append(LoadedGraph.GetNI(item).GetOutDeg())

for firstNode in test:
    # add all nodes into susceptible
    for NI in LoadedGraph.Nodes():
        susceptible.append(NI.GetId())

    firstInfected = infectedElement(firstNode)
    susceptible.remove(firstNode)
    infectious.append(firstInfected)
    tempInfectious = []

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
        
        if len(infectious) == 0:
            infectious.clear()
            removed.clear()
            susceptible.clear()
            data = {'id': firstNode, 'outDegree': LoadedGraph.GetNI(firstNode).GetOutDeg(), 'stopTime': t}
            break
            
    df.at[firstNode, :] = data

        # data = {'susceptible': len(susceptible), 'infectious': len(infectious), 'removed': len(removed)}
        # df.at[t+1, :] = data

    # print(df)

df.to_excel(writer, sheet_name="network effect")

writer.save()

