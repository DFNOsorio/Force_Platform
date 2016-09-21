#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.segmentator import Segment
import matplotlib.pylab as plt


def RGM2COP(Segment, smooth=True):
    if smooth:
        temp_EMG = Segment.EMGs_SmoothData
    else:
        temp_EMG = Segment.EMGs

    FL = temp_EMG[:, 0]
    FR = normalize(temp_EMG[:, 1])
    BR = normalize(temp_EMG[:, 2])
    BL = normalize(temp_EMG[:, 3])

    Segment.COPx_EMG = (FR + BR - (FL + BL)) / (FL + BL + FR + BR)
    Segment.COPy_EMG = (FR + FL - (BR + BL)) / (FL + BL + FR + BR)

    return Segment


    # ### MAXIMOS E MINIMOS DOS SEGMENTOS PARA CONSEGUIR VER AS MANCHAS DE TAMANHOS DIFERENTE

def normalize(data):

    return (data - min(data)) / (max(data) - min(data))


