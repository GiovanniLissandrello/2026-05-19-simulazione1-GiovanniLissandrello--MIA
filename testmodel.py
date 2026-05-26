from model.model import Model

myModel = Model()
myModel.buildDiGraph(1)
nNodes, nEdges = myModel.getGraphDetails()
print(myModel._dict_popolarita.get(1))
print(f"Num nodes: {nNodes}, num edges: {nEdges}")