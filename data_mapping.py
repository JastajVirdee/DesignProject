import math
from scipy.optimize import fsolve

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

def solve(f1, f2, f3, x0, y0, z0):
    '''
    Solve system of equations
    Paramters 1-3: equations
    Paramters 4-6: initial estimates
    Returns: solution to system of equations.
    '''
    func = lambda x: [f1(x[0],x[1],x[2]), f2(x[0],x[1],x[2]), f3(x[0],x[1],x[2])]
    return fsolve(func,[x0,y0,z0])

def get_signals(type):
    '''
    Read signal levels from .log file.
    Parameter: signal type (nose or ear)
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
    elif type == 'ear':
        for i in range(0, len(signals)):
            north_distance = 3.35 + 1.25*10**(-3)*float(signals[i]['North']) - 2.23*10**(-7)*float(signals[i]['North'])**2
            east_distance = -242 + 0.106*float(signals[i]['East']) - 1.13*10**(-5)*float(signals[i]['East'])**2
            south_distance = 3.67 - 2.78*10**(-3)*float(signals[i]['South']) + 1.54*10**(-6)*float(signals[i]['South'])**2
            west_distance = 122 - 0.0864*float(signals[i]['West']) + 1.58*10**(-5)*float(signals[i]['West'])**2
            center_distance = 6.16 - 2.72*10**(-3)*float(signals[i]['Center']) + 4.71*10**(-7)*float(signals[i]['Center'])**2
            distances.append({'North':north_distance, 'East':east_distance, 'South':south_distance, 'West':west_distance, 'Center':center_distance})
    return distances

def get_position(distances, type):
    '''
    Parameter 1: distances = distance from nose/ear to corresponding pad electrodes (list[time slice][dictionary{str:float}])
    Parameter 2: signal type (nose or ear)
    Returns: position = x, y, and z position (list[time slice](x,y,z))
    '''
    positions = []
    if type == 'nose':
        for i in range(0, len(distances)):
            fn = lambda x,y,z : (NOSE_NORTH['x']-x)**2 + (NOSE_NORTH['y']-y)**2 + (NOSE_NORTH['z']-z)**2 - distances[i]['North']**2
            fe = lambda x,y,z : (NOSE_EAST['x']-x)**2 + (NOSE_EAST['y']-y)**2 + (NOSE_EAST['z']-z)**2 - distances[i]['East']**2
            fs = lambda x,y,z : (NOSE_SOUTH['x']-x)**2 + (NOSE_SOUTH['y']-y)**2 + (NOSE_SOUTH['z']-z)**2 - distances[i]['South']**2
            fw = lambda x,y,z : (NOSE_WEST['x']-x)**2 + (NOSE_WEST['y']-y)**2 + (NOSE_WEST['z']-z)**2 - distances[i]['West']**2
            fc = lambda x,y,z : (NOSE_CENTER['x']-x)**2 + (NOSE_CENTER['y']-y)**2 + (NOSE_CENTER['z']-z)**2 - distances[i]['Center']**2
            x1, y1, z1 = solve(fn,fe,fc,0,15,2)
            x2, y2, z2 = solve(fe,fs,fc,0,15,2)
            x3, y3, z3 = solve(fs,fw,fc,0,15,2)
            x4, y4, z4 = solve(fw,fn,fc,0,15,2)
            if z1<0: z1=z1*(-1)
            if z2<0: z2=z2*(-1)
            if z3<0: z3=z3*(-1)
            if z4<0: z4=z4*(-1)
            x = (x1+x2+x3+x4)/4
            y = (y1+y2+y3+y4)/4
            z = (z1+z2+z3+z4)/4
            positions.append((x,y,z))
    elif type == 'ear':
        for i in range(0, len(distances)):
            fn = lambda x,y,z : (EAR_NORTH['x']-x)**2 + (EAR_NORTH['y']-y)**2 + (EAR_NORTH['z']-z)**2 - distances[i]['North']**2
            fe = lambda x,y,z : (EAR_EAST['x']-x)**2 + (EAR_EAST['y']-y)**2 + (EAR_EAST['z']-z)**2 - distances[i]['East']**2
            fs = lambda x,y,z : (EAR_SOUTH['x']-x)**2 + (EAR_SOUTH['y']-y)**2 + (EAR_SOUTH['z']-z)**2 - distances[i]['South']**2
            fw = lambda x,y,z : (EAR_WEST['x']-x)**2 + (EAR_WEST['y']-y)**2 + (EAR_WEST['z']-z)**2 - distances[i]['West']**2
            fc = lambda x,y,z : (EAR_CENTER['x']-x)**2 + (EAR_CENTER['y']-y)**2 + (EAR_CENTER['z']-z)**2 - distances[i]['Center']**2
            x1, y1, z1 = solve(fn,fe,fc,10,14,12)
            x2, y2, z2 = solve(fe,fs,fc,10,14,12)
            x3, y3, z3 = solve(fs,fw,fc,10,14,12)
            x4, y4, z4 = solve(fw,fn,fc,10,14,12)
            if z1<0: z1=z1*(-1)
            if z2<0: z2=z2*(-1)
            if z3<0: z3=z3*(-1)
            if z4<0: z4=z4*(-1)
            x = (x1+x2+x3+x4)/4
            y = (y1+y2+y3+y4)/4
            z = (z1+z2+z3+z4)/4
            positions.append((x,y,z))
    return positions

# Get signals
nose_signals = get_signals('nose')
#ear_signals = get_signals('ear')

# Convert signals to distances
nose_distances = get_distances(nose_signals, 'nose')
#ear_distances = get_distances(ear_signals, 'ear')

# Convert distances to position
nose_positions = get_position(nose_distances, 'nose')
#ear_postition = get_position(ear_distances, 'ear')

# Write output to a file
f = open("output.txt","w+")
for i in range(0, len(nose_positions)):
    f.write('(%f, %f, %f)\n' % (nose_positions[i][0], nose_positions[i][1], nose_positions[i][2]))
f.close()