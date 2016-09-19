import novainstrumentation as ni
import numpy as np
from code import *

class Segment:

    def __init__(self, initial_index, final_index, EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def):

        self.initial_index        =   initial_index
        self.final_index          =   final_index

        self.EMGs                 =   EMG_data[initial_index:final_index, 0:4]
        self.EMG_Time             =   EMG_times[initial_index:final_index]
        self.EMG_Labels           =   EMG_labels[0:4]
        self.EMG_Resolution       =   EMG_def[1]
        self.EMG_Fs               =   EMG_def[0]

        self.ACCs                 =   EMG_data[initial_index:final_index, 4:7]
        self.ACCs_Time            =   EMG_times[initial_index:final_index]
        self.ACCs_Labels          =   EMG_labels[4:7]
        self.ACCs_Resolution      =   EMG_def[1]
        self.ACCs_Fs              =   EMG_def[0]

        self.Platform             =   Platform_data[initial_index:final_index, :]
        self.Platform_Time        =   Platform_times[initial_index:final_index]
        self.Platform_Labels      =   Platform_labels
        self.Platform_Resolution  =   Platform_def[1]
        self.Platform_Fs          =   Platform_def[0]


def read_config(dataset):
    info = {}
    config_file = file(dataset+'_Sync.txt', 'r')
    lines = config_file.readlines()
    for i in range(1, len(lines)):
        current_line = lines[i].strip().split(';')
        if(len(current_line) == 3):
            info[current_line[0]] = [int(current_line[1]), int(current_line[2])]
        elif(len(current_line) == 5):
            info[current_line[0]] = {current_line[2]: current_line[1], current_line[4]: current_line[3]}
        else:
            info[current_line[0]] = int(current_line[1])

    return info



def segment_data(dataset, EMG_data, EMG_labels, EMG_times, Platform_data, Platform_labels, Platform_times):

        print 'hey'

def tare(indexes, Platform_data, resolution, fs):

    converted_mass = convert2mass(Platform_data[indexes[0]*fs:indexes[1]*fs, :], [9, 2, 32, 30], resolution)

    print converted_mass
