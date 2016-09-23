import numpy as np
from code.platform_functions import convert2mass, getCops


class Segment:

    tare         = [0, 0]
    EMG_Tare     = [0, 0, 0, 0]
    EMG_COP_Tare = [0, 0]
    wii          = False

    def __init__(self, initial_time, final_time, EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, title, delay):

        self.initial_time         =   initial_time
        self.final_time           =   final_time

        self.EMGs                 =   EMG_data[initial_time*EMG_def[0]:final_time*EMG_def[0], 0:4]
        self.EMGs_Time            =   EMG_times[initial_time*EMG_def[0]:final_time*EMG_def[0]]
        self.EMGs_Labels          =   EMG_labels[0:4]
        self.EMGs_Resolution      =   EMG_def[1]
        self.EMGs_Fs              =   EMG_def[0]

        self.ACCs                 =   EMG_data[initial_time*EMG_def[0]:final_time*EMG_def[0], 4:7]
        self.ACCs_Time            =   EMG_times[initial_time*EMG_def[0]:final_time*EMG_def[0]]
        self.ACCs_Labels          =   EMG_labels[4:7]
        self.ACCs_Resolution      =   EMG_def[1]
        self.ACCs_Fs              =   EMG_def[0]

        self.Platform             =   Platform_data[(initial_time - delay)*Platform_def[0]:(final_time - delay)*Platform_def[0], :]
        self.Platform_Time        =   Platform_times[(initial_time - delay)*Platform_def[0]:(final_time - delay)*Platform_def[0]]
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
        if(current_line[0] == "Tare"):
            info[current_line[0]] = [int(current_line[1]), int(current_line[2])]
        elif(len(current_line) == 3):
            info[current_line[0]] =  {current_line[2]: int(current_line[1])}
        elif(len(current_line) == 5):
            info[current_line[0]] = {current_line[2]: int(current_line[1]), current_line[4]: int(current_line[3])}
        else:
            info[current_line[0]] = int(current_line[1])
    return info


def segment_data(dataset, EMG, Platform, time_delta = 0, event_index=0):

    EMG_data        = EMG[0]
    EMG_times       = EMG[1]
    EMG_labels      = EMG[2]
    EMG_def         = EMG[3]

    Platform_data   = Platform[0]
    Platform_times  = Platform[1]
    Platform_labels = Platform[2]
    Platform_def    = Platform[3]

    time_data = read_config(dataset)
    print time_data
    segments = {}

    delay = 0

    if 'Sync_Wii' in time_data:
        Segment.wii = True

        Platform_times, delay = sync_time_vectors(Platform_times, event_index, time_data['Sync_Wii'], time_delta, EMG_times)

    if 'Tare' in time_data:
        tare_COPx, tare_COPy = tare(time_data['Tare'], Platform_data, Platform_def[1], Platform_def[0])
        Segment.tare = [tare_COPx, tare_COPy]

    if 'S1' in time_data:
        S1 = Segment(time_data['S1'], (time_data['S1'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'Two feet, eyes open', delay)
        segments["S1"] = S1

    if 'S2' in time_data:
        S2 = Segment(time_data['S2'], (time_data['S2'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'Two feet, eyes closed', delay)
        segments["S2"] = S2

    if "S3" in time_data:
        if 'd' in time_data['S3']:
            S3_d = Segment(time_data['S3']['d'], (time_data['S3']['d'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (left on platform), eyes open', delay)
            segments["S3_d"] = S3_d

        if 'e' in time_data['S3']:
            S3_e = Segment(time_data['S3']['e'], (time_data['S3']['e'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (right on platform), eyes open', delay)
            segments["S3_e"] = S3_e

    if "S4" in time_data:
        if 'd' in time_data['S4']:
            S4_d = Segment(time_data['S4']['d'], (time_data['S4']['d'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (left on platform), eyes closed', delay)
            segments["S4_d"] = S4_d

        if 'e' in time_data['S4']:
            S4_e = Segment(time_data['S4']['e'], (time_data['S4']['e'] + 30), EMG_data, EMG_labels, EMG_times, EMG_def, Platform_data, Platform_labels, Platform_times, Platform_def, 'One feet (right on platform), eyes closed', delay)
            segments["S4_e"] = S4_e

    return segments


def tare(indexes, Platform_data, resolution, fs):
    converted_mass = convert2mass(Platform_data[indexes[0]*fs:indexes[1]*fs, :], [9, 2, 32, 30], resolution, Segment.wii)
    tare_COPx, tare_COPy = getCops(converted_mass, 0, [0, 0])
    return np.mean(tare_COPx), np.mean(tare_COPy)
