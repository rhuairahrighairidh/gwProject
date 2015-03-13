import numpy as np
import recorder as r


def runModel(model,testSignal,fieldFunctions = [r.modelInput,r.bestPrediction,r.anomalyScore]):
    """
    This runs the model through the supplied signal. At each point it saves out data specied in fieldFunctions.
    This takes the model input to be the first field in model.getFieldInfo().
    """
    store = r.Store()
    
    for sample in testSignal:
        result = model.run({model.getFieldInfo()[0].name: float(sample)})
        store.record(model,result,fieldFunctions)
  
    return store
    
    
    
##calculate average error for each noise level, using the big dictionary from above
def computeError(store): #Error bars would be nice as well
    actual = np.array(store.modelInput[1:])
    predicted = np.array(store.bestPrediction[:-1])
    return np.sum(np.abs(actual-predicted)) / len(predicted)
    
    
    
def computeAverageAnomaly(store):
    return np.array(store.anomalyScore).mean()
    
    
    
def runAverageingTest(model,testSignals,errorFunction=computeError):
    """
    This function runs the model on each signal in the list testSignals, reseting the sequence inbetween each.
    For each sigal an error is computed (using the suplied errorFunction).
    The average and standard deviation of these errors will be returned.
    """
    errors = []
    for signal in testSignals:
        model.resetSequenceStates()
        errors.append(errorFunction(runModel(model,signal)))#The data generated when running is lost here. You could modify this to save it into a store.
    
    errors = np.array(errors)
    return {'average': errors.mean(), 'stdDev':errors.std()}