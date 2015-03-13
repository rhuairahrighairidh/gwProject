import numpy
import itertools
import matplotlib.pyplot as plt
import itertools

def flatten(inputList):
    """
    A function to return a flattened version of the input list. Not sure if it works on things that aren't lists
    """
    return list(itertools.chain.from_iterable(inputList))

def b(x=18,y=5):
    """
    Set the size of the current matplotlib figure (in "inches").
    The default values are reasonable for the ipython notebook.
    """
    global plt
    f=plt.gcf()
    f.set_size_inches([x,y])

def gaussian(x, mu=0, sig=1):
    """Gausian Function"""
    return numpy.exp(-numpy.power(x - mu, 2.) / (2. * numpy.power(sig, 2.)))

def createGlitch(frequency=1.0,phase=0.0,sampleRate=1/8.0,duration=1.0):
    """
        Creates a series of points for a sine-gaussian.
        Leave duration at 1, then frequency is just number of waves and sampleRate is number of samples.
        The sigma of the gaussian is set so that the edges correspond to a scaling of 0.1%
        The sample points lie in the interval [0,duration)
        
        frequecy -> Hertz
        phase -> Radians
        sampleRate -> Hertz
        duration -> seconds
        """
    
    t=numpy.arange(0,duration,sampleRate) #Creates points in the interval [0,duration).
    
    mu=duration/2.0
    sigma=numpy.sqrt((-(duration-mu)**2)/(2*numpy.log(0.001))) #Set the width of the gaussian such that the edges are at height 0.001 (0.1%)
    g = gaussian(t,mu=mu,sig=sigma)
    
    sine = numpy.sin(2*numpy.pi*frequency*t+phase)
    
    return g*sine

def plotSegmentInfo(model):
    tp=model._getTPRegion().getSelf()._tfdr
    si=tp.getSegmentInfo()
    
    print "Total Number Of Segements:"+str(si[0])
    print "Total Number of Synapses:"+str(si[1])
    
    fig,axes=plt.subplots(2,2)
    plotDistSegSizes(si,axes[0,0])
    plotDistNSegsPerCell(si,axes[0,1])
    plotDistPermValues(si,axes[1,0])
    plotDistAges(si,axes[1,1])
    fig.set_size_inches(18,10)

def plotDistSegSizes(segmentInfo,axis):
    x=segmentInfo[4].keys()
    axis.bar(x,segmentInfo[4].values(),align='center',width=1)
    axis.set_xticks(x);
    axis.set_xlabel('number of synapses')
    axis.set_ylabel('number of segments')
    
def plotDistNSegsPerCell(segmentInfo,axis):
    x=segmentInfo[5].keys()
    axis.bar(x,segmentInfo[5].values(),align='center',width=1)
    axis.set_xticks(x);
    axis.set_xlabel('number of segments')
    axis.set_ylabel('number of cells')

def plotDistPermValues(segmentInfo,axis):
    x=segmentInfo[6].keys()
    axis.bar(x,segmentInfo[6].values(),align='center',width=1)
    axis.set_xticks(x);
    axis.set_xlabel('permanence*10')
    axis.set_ylabel('number of synapses')

def plotDistAges(segmentInfo,axis):
    def toInts(string):
        return map(int,string.split('-'))

    ranges=numpy.array(segmentInfo[7])[:,0]
    ranges = numpy.array(map(toInts,ranges))
    left=ranges[:,0]
    width = map(lambda l: l[1]-l[0]+1,ranges)
    height = map(int,numpy.array(segmentInfo[7])[:,1])

    axis.bar(left,height,width)
    axis.set_xlabel('Segment Ages')
    axis.set_ylabel('Number Of Segments');