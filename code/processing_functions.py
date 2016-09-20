import novainstrumentation as ni
import numpy as np
from code.segmentator import Segment
from code.platform_functions import convert2mass, getCops, convex_hull, area_calc


def add_smooth_data(Segment, win_len=(500, 500, 500), delay=500):
    smooth_data_EMG = np.zeros(np.shape(Segment.EMGs))

    for i in range(0, np.shape(Segment.EMGs)[1]):
        smooth_data_EMG[:, i] = ni.smooth(Segment.EMGs[:, i], window_len=win_len[0])

    Segment.EMGs_SmoothData = smooth_data_EMG[delay:-delay]

    smooth_data_ACC = np.zeros(np.shape(Segment.ACCs))

    for i in range(0, np.shape(Segment.ACCs)[1]):
        smooth_data_ACC[:, i] = ni.smooth(Segment.ACCs[:, i], window_len=win_len[1])

    Segment.ACCs_SmoothData = smooth_data_ACC[delay:-delay]

    smooth_data_Platform = np.zeros(np.shape(Segment.Platform))

    for i in range(0, np.shape(Segment.Platform)[1]):
        smooth_data_Platform[:, i] = ni.smooth(Segment.Platform[:, i], window_len=win_len[2])

    Segment.Platform_SmoothData = smooth_data_Platform[delay:-delay]

    return Segment


def add_COPS_data(Segment, offsets=[9, 2, 32, 30], weighThr=0, smooth=True):
    if smooth:
        Segment.converted_mass = convert2mass(Segment.Platform_SmoothData, offsets, Segment.Platform_Resolution)
    else:
        Segment.converted_mass = convert2mass(Segment.Platform, offsets, Segment.Platform_Resolution)

    Segment.COPx, Segment.COPy = getCops(Segment.converted_mass, weighThr, Segment.tare)
    Segment.hull = convex_hull(Segment.COPx, Segment.COPy)
    Segment.area = area_calc(Segment.hull)

    return Segment

