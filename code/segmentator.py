
import numpy as np
from code.platform_functions import convert2mass, getCops

class Segment:

    tare = [0, 0]
    EMG_Tare = [0, 0, 0, 0]
    EMG_COP_Tare = [0, 0]

    def __init__(self, initial_index, final_index, EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, title):

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

        self.Segment_Name         =   title


def read_config(dataset):
    info = {}
    config_file = file(dataset+'_Sync.txt', 'r')
    lines = config_file.readlines()
    for i in range(1, len(lines)):
        current_line = lines[i].strip().split(';')
        if(len(current_line) == 3):
            info[current_line[0]] = [int(current_line[1]), int(current_line[2])]
        elif(len(current_line) == 5):
            info[current_line[0]] = {current_line[2]: int(current_line[1]), current_line[4]: int(current_line[3])}
        else:
            info[current_line[0]] = int(current_line[1])
    return info


def segment_data(dataset, EMG, Platform):

    EMG_data        = EMG[0]
    EMG_times       = EMG[1]
    EMG_labels      = EMG[2]
    EMG_def         = EMG[3]

    Platform_data   = Platform[0]
    Platform_times  = Platform[1]
    Platform_labels = Platform[2]
    Platform_def    = Platform[3]

    time_data = read_config(dataset)

    tare_COPx, tare_COPy = tare(time_data['Tare'], Platform_data, Platform_def[1], Platform_def[0])

    Segment.tare = [tare_COPx, tare_COPy]

    S1 = Segment(time_data['S1'] * Platform_def[0], (time_data['S1'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'Two feet, eyes open')

    S2 = Segment(time_data['S2'] * Platform_def[0], (time_data['S2'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'Two feet, eyes closed')

    S3_d = Segment(time_data['S3']['d'] * Platform_def[0], (time_data['S3']['d'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (left on platform), eyes open')

    S3_e = Segment(time_data['S3']['e'] * Platform_def[0], (time_data['S3']['e'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (right on platform), eyes open')

    S4_d = Segment(time_data['S4']['d'] * Platform_def[0], (time_data['S4']['d'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (left on platform), eyes closed')

    S4_e = Segment(time_data['S4']['e'] * Platform_def[0], (time_data['S4']['e'] + 30) * Platform_def[0], EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (right on platform), eyes closed')

    return S1, S2, S3_d, S3_e, S4_d, S4_e


def tare(indexes, Platform_data, resolution, fs):
    converted_mass = convert2mass(Platform_data[indexes[0]*fs:indexes[1]*fs, :], [9, 2, 32, 30], resolution)
    tare_COPx, tare_COPy = getCops(converted_mass, 0, [0, 0])
    return np.mean(tare_COPx), np.mean(tare_COPy)
