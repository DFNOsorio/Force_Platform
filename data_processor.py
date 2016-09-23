from code import *
import matplotlib.pyplot as plt
import numpy as np

Plux_Paulo = 'Equilibrio/Plux_Platform/Paulo'

Wii_Paulo = 'Equilibrio/Wii_Board/Paulo'

EMG_data, EMG_time, EMG_labels, EMG_def, ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def = load_data_h5(Plux_Paulo)

#EMG_data, EMG_time, EMG_labels, EMG_def, ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def, delay, event_index = load_data_h5_wii(Wii_Paulo)

EMG = [EMG_data, EMG_time, EMG_labels, EMG_def]
Platform = [ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def]

segments = segment_data(Plux_Paulo, EMG, Platform)

Segment.EMG_Tare, Segment.EMG_COP_Tare = Tare_EMG(segments["S1"])

#plt.figure(1)
counter = 1

for i in segments.values():
    i = add_smooth_data(i)
    i = add_COPS_data(i, smooth=False)
    i = RGM2COP(i, smooth=False)
#    plt.figure(1)
#    plt.subplot(3,2,counter)
#    plt.plot(i.COPx_EMG, i.COPy_EMG)
#    plt.title(i.Segment_Name, fontsize=10)
#    plt.xlim([-0.0003, 0.0003])
#    plt.ylim([-0.0003, 0.0003])
#    plt.figure()
#    plt.subplot(221)
#    plt.plot(i.COPx_EMG)
#    plt.subplot(222)
#    plt.plot(i.COPx)
#    plt.subplot(223)
#    plt.plot(i.COPy_EMG)
#    plt.subplot(224)
#    plt.plot(i.COPy)
#    plt.title(i.Segment_Name, fontsize=10)
#    plt.figure()
#    plt.subplot(211)
#    plt.plot(i.Right)
#    plt.plot(i.Left)
#    plt.legend(["Right", "Left"])
#
#    plt.subplot(212)
#    plt.plot(i.Front)
#    plt.plot(i.Back)
#    plt.legend(["Front", "Back"])
    counter+=1

raw_dump_normalization(segments["S4_d"])

plt.show()
