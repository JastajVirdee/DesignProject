# Global Variables:
NOSE_NORTH  = {'x':  0.0, 'y': 18.8, 'z':  0.0}
NOSE_EAST   = {'x': -5.0, 'y': 15.5, 'z':  0.0}
NOSE_SOUTH  = {'x':  0.0, 'y': 12.2, 'z':  0.0}
NOSE_WEST   = {'x':  5.0, 'y': 15.5, 'z':  0.0}
NOSE_CENTER = {'x':  0.0, 'y': 15.5, 'z':  0.0}
EAR_NORTH   = {'x': 12.2, 'y': 14.4, 'z':  9.0}
EAR_EAST    = {'x': 12.2, 'y':  9.4, 'z': 12.3}
EAR_SOUTH   = {'x': 12.2, 'y': 14.4, 'z': 15.6}
EAR_WEST    = {'x': 12.2, 'y': 19.4, 'z': 12.3}
EAR_CENTER  = {'x': 12.2, 'y': 14.4, 'z': 12.3}

def get_signals():
    '''
    Read signal levels from .log file.
    Returns: signals (list[time slice][signals (dictionary{str:float}])
    '''
    signals = []
    f = open('microchip.log', 'r')
    for line in f:
        if (line.startswith('3D DATA', 6, 13)):
            line_words = line.split()
            line_signals = {'South':line_words[8], 'West':line_words[9], 'North':line_words[10], 'East':line_words[11],'Center':line_words[12]}
            signals.append(line_signals)
    return signals
            

def get_distances(signals):
    '''
    Convert signal levels to distances
    Parameter 1: signals (list[time slice][signals (dictionary{str:float})])
    Returns: nose_distances, ear_distances (dictionary{str:float})
    '''

def get_position(nose_distances, ear_distances):
    '''
    Parameter 1: nose_distances = distance from nose to nose pad electrodes (dictionary{str:float})
    Parameter 2: ear_distances = distance from ear to ear pad electrodes (dictionary{str:float})
    Returns: nose_position, ear_position (dictionary{str:float})
    '''

signals = get_signals()
print(signals)