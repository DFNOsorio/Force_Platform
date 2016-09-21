#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.segmentator import Segment
import matplotlib.pylab as plt
import novainstrumentation as ni
import numpy as np


def RGM2COP(Segment, smooth=True):
    if smooth:
        temp_EMG = Segment.EMGs_SmoothData
    else:
        temp_EMG = Segment.EMGs

    FL = temp_EMG[:, 0]
    FR = temp_EMG[:, 1]
    BR = temp_EMG[:, 2]
    BL = temp_EMG[:, 3]

    Segment.Front    = (FR + FL)
    Segment.Back     = (BR + BL)

    Segment.Left     = (FL + BL)
    Segment.Right    = (FR + BR)

    Segment.COPx_EMG = (Segment.Right - Segment.Left) / (FL + BL + FR + BR) - Segment.EMG_COP_Tare[0]
    Segment.COPy_EMG = (Segment.Front - Segment.Back) / (FL + BL + FR + BR) - Segment.EMG_COP_Tare[1]

    return Segment

def normalize(data):

    return (data - min(data)) / (max(data) - min(data))


def Tare_EMG(Segment, indexes=(500, 1500), win_len=500):

    temp_EMG = Segment.EMGs

    FL = ni.smooth(temp_EMG[:, 0], window_len=win_len)[indexes[0]:indexes[1]]
    FR = ni.smooth(temp_EMG[:, 1], window_len=win_len)[indexes[0]:indexes[1]]
    BR = ni.smooth(temp_EMG[:, 2], window_len=win_len)[indexes[0]:indexes[1]]
    BL = ni.smooth(temp_EMG[:, 3], window_len=win_len)[indexes[0]:indexes[1]]

    COPx_EMG = ((FR + BR) - (FL + BL)) / (FL + BL + FR + BR)
    COPy_EMG = ((FR + FL) - (BR + BL)) / (FL + BL + FR + BR)

    return [np.mean(FL), np.mean(FR), np.mean(BR), np.mean(BL)], [np.mean(COPx_EMG), np.mean(COPy_EMG)]
