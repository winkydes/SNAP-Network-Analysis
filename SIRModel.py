import snap
import random
import pandas as pd
from openpyxl import load_workbook

book = load_workbook('SIR_model.xlsx')
writer = pd.ExcelWriter('SIR_model.xlsx', engine='openpyxl') 
writer.book = book

## ExcelWriter for some reason uses writer.sheets to access the sheet.
## If you leave it empty it will not know that sheet Main is already there
## and will create a new sheet.

writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
# panda setup

# load graph
LoadedGraph = snap.LoadEdgeList(snap.PNGraph, "./facebook_combined.txt")

snap.PrintInfo(LoadedGraph)

# constants
susceptible = []
infectious = []
removed = []
contagionProbability = 0.5
totalTimestep = 50
infectiousPeriod = 9

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

# get the node with maximum out degree
maxOutDegNodeId = LoadedGraph.GetMxOutDegNId()
print(maxOutDegNodeId)

# generate random node id to start the transmission
# randomNodeId = random.randrange(0,LoadedGraph.GetMxNId())
# print("random node no is", randomNodeId)
firstInfected = infectedElement(maxOutDegNodeId)
susceptible.remove(maxOutDegNodeId)
infectious.append(firstInfected)
tempInfectious = []

df = pd.DataFrame(columns=['susceptible','infectious', 'removed'])
data = {'susceptible': len(susceptible), 'infectious': len(infectious), 'removed': len(removed)}
df.at[1, :] = data

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

    data = {'susceptible': len(susceptible), 'infectious': len(infectious), 'removed': len(removed)}
    df.at[t+1, :] = data

print(df)

df.to_excel(writer, sheet_name="t=" + str(infectiousPeriod))

writer.save()

    
    
            



