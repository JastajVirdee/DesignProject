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
    Returns: signal_levels (list[time slice][signals (dictionary{str:float}])
    '''

def get_distances(signal_levels):
    '''
    Convert signal levels to distances
    Parameter 1: signal levels (list[time slice][signals (dictionary{str:float})])
    Returns: nose_distances, ear_distances (dictionary{str:float})
    '''

def get_position(nose_distances, ear_distances):
    '''
    Parameter 1: nose_distances = distance from nose to nose pad electrodes (dictionary{str:float})
    Parameter 2: ear_distances = distance from ear to ear pad electrodes (dictionary{str:float})
    Returns: nose_position, ear_position (dictionary{str:float})
    '''

