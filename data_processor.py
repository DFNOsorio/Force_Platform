from code import *
import matplotlib.pyplot as plt
import numpy as np

patient = 'Equilibrio/Paulo'


EMG_data, EMG_time, EMG_labels, EMG_def, ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def = load_data_h5(patient)

EMG = [EMG_data, EMG_time, EMG_labels, EMG_def]
Platform = [ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def]

S1, S2, S3_d, S3_e, S4_d, S4_e = segment_data(patient, EMG, Platform)

for i in [S1, S2, S3_d, S3_e, S4_d, S4_e]:
    i = add_smooth_data(i)
    i = add_COPS_data(i)
    i = RGM2COP(i)

plt.figure()
plt.plot(S1.COPx, S1.COPy)
plt.plot(S2.COPx, S2.COPy)
plt.plot(S3_d.COPx, S3_d.COPy)
plt.plot(S3_e.COPx, S3_e.COPy)
plt.plot(S4_d.COPx, S4_d.COPy)
plt.plot(S4_e.COPx, S4_e.COPy)

plt.xlim([-(225+12), (225+12)])
plt.ylim([-(225+12), (225+12)])
plt.legend([S1.Segment_Name, S2.Segment_Name, S3_d.Segment_Name, S3_e.Segment_Name, S4_d.Segment_Name, S4_e.Segment_Name], fontsize=10)


plt.show()
