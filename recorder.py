import numpy as np

class Store:
    def __init__(self):
        pass
    
    def record(self,model,result,fieldFunctions):
        for function in fieldFunctions:
            fieldName = function.__name__
            if not hasattr(self,fieldName):
                setattr(self,fieldName,[])
        
            field = getattr(self,fieldName)
            field.append(function(model=model,result=result))


def anomalyScore(model,result):
    return result.inferences['anomalyScore']

def bestPrediction(model,result):
    return result.inferences['multiStepBestPredictions'][1]

def allPredictions(model,result):
    return result.inferences['multiStepPredictions'][1]

def predictedColumns(model,result):
    return model._prevPredictedColumns

def modelInput(model,result):
    name = model.getFieldInfo()[0].name
    return model._input[name]

def boostFactors(model,result):
    sp = model._getSPRegion().getSelf()._sfdr
    dimensions = sp.getColumnDimensions()
    boostFactorsArray = np.zeros(dimensions)
    sp.getBoostFactors(boostFactorsArray)
    return boostFactorsArray

def activeDutyCycles(model,result):
    sp = model._getSPRegion().getSelf()._sfdr
    dimensions = sp.getColumnDimensions()
    array = np.zeros(dimensions)
    sp.getActiveDutyCycles(array)
    return array

def activeCells(model,result):
    tp=model._getTPRegion().getSelf()._tfdr
    flatArray = tp.getActiveState()
    activeCells = flatArray.reshape([tp.numberOfCols,tp.cellsPerColumn])#,dtype='int8')#same dtype as predicted state
    return activeCells

def predictiveCells(model,result):
    tp=model._getTPRegion().getSelf()._tfdr
    array = tp.getPredictedState()
    return array

def activeColumns(model,result):
    """This doesn't work"""
    tp=model._getTPRegion().getSelf()._tfdr
    return tp.activeColumns

def debug(model,result):
    """
        This returns a random integer between 0 and 9
        """
    return np.random.randint(10)

def proximalSynapses(model,result):
    """"
    Returns the permanences of the spatial pooler synapses.
    """
    from nupic.bindings.math import GetNTAReal
    realType = GetNTAReal()

    sp = model._getSPRegion().getSelf()._sfdr
    numColumns = sp.getNumColumns()
    numInputs = sp.getNumInputs()
    proximalSynapses=[]

    for column in xrange(numColumns):
    
        #Get permanence values
        permanences=np.zeros(numInputs).astype(realType)
        sp.getPermanence(column,permanences)
        permanences=permanences.astype(float)

        #Get potential synapse map
        potentials = np.zeros(numInputs).astype('uint32')
        sp.getPotential(column,potentials)
        potentials=potentials.astype(bool)
        
        #Put everything into a list of indexes beacuse numpy is rubbish
        for i in xrange(len(permanences)):
            if potentials[i]:
                proximalSynapses.append([column,i,permanences[i]])
    return proximalSynapses
        
def fastProximalPermanences(model,result):
    """"
    Returns the permanences of the spatial pooler synapses.
    """
    from nupic.bindings.math import GetNTAReal
    realType = GetNTAReal()

    sp = model._getSPRegion().getSelf()._sfdr
    numInputs = sp.getNumInputs()
    numColumns = sp.getNumColumns()
    
    allPermanences=[]
    for column in xrange(numColumns):
        permanences=np.zeros(numInputs).astype(realType)
        sp.getPermanence(column,permanences)
        allPermanences.append(permanences)
    return np.concatenate(allPermanences)
    
def connectedProximalSynapseCount(model,result):
    """Returns the total number of proximal synapses that are connected."""
    sp = model._getSPRegion().getSelf()._sfdr
    numColumns = sp.getNumColumns()
    connectedSynapsesPerColumn=np.zeros(numColumns,dtype='uint32')
    sp.getConnectedCounts(connectedSynapsesPerColumn)
    return np.sum(connectedSynapsesPerColumn)

def distalSynapseCount(model,result):
    """Returns the total number of synapses in the temporal memory."""
    tp=model._getTPRegion().getSelf()._tfdr
    return tp.getNumSynapses()
    
def distalSegmentCount(model,result):
    """Returns the total number of segments in the temporal memory."""
    tp=model._getTPRegion().getSelf()._tfdr
    return tp.getNumSegments()