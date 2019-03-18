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

def get_signals(type):
    '''
    Read signal levels from .log file.
    Parameter 1: signal type (nose or ear)
    Returns: signals (list[time slice][signals (dictionary{str:float}])
    '''
    signals = []
    f = open('../' + type + '.log', 'r')
    for line in f:
        if (line.startswith('3D DATA', 6, 13)):
            line_words = line.split()
            line_signals = {'North':line_words[10], 'East':line_words[11], 'South':line_words[8], 'West':line_words[9], 'Center':line_words[12]}
            signals.append(line_signals)
    return signals
            

def get_distances(signals, type):
    '''
    Convert signal levels to distances
    Parameter 1: signals (list[time slice][signals (dictionary{str:float})])
    Parameter 2: signal type (nose or ear)
    Returns: nose_distances, ear_distances (list[time slice][dictionary{str:float}])
    '''
    distances = []
    if type == 'nose':
        for i in range(0, len(signals)):
            north_distance = -279 - 0.343*float(signals[i]['North']) - 1.03*10**(-4)*float(signals[i]['North'])**2
            east_distance = -10.4 + 0.176*float(signals[i]['East']) - 4.26*10**(-4)*float(signals[i]['East'])**2
            south_distance = -290 - 0.676*float(signals[i]['South']) - 3.88*10**(-4)*float(signals[i]['South'])**2
            west_distance = 697 + 1.08*float(signals[i]['West']) + 4.20*10**(-4)*float(signals[i]['West'])**2
            center_distance = 182 - 0.362*float(signals[i]['Center']) + 1.82*10**(-4)*float(signals[i]['Center'])**2
            distances.append({'North':north_distance, 'East':east_distance, 'South':south_distance, 'West':west_distance, 'Center':center_distance})
    return distances

def get_position(nose_distances, ear_distances):
    '''
    Parameter 1: nose_distances = distance from nose to nose pad electrodes (dictionary{str:float})
    Parameter 2: ear_distances = distance from ear to ear pad electrodes (dictionary{str:float})
    Returns: nose_position, ear_position (dictionary{str:float})
    '''

# Get signals
nose_signals = get_signals('nose')
#ear_signals = get_signals('ear')

# Convert signals to distances
nose_distances = get_distances(nose_signals, 'nose')
#ear_distances = get_distances(ear_signals, 'ear')