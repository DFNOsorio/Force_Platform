from code import *
import matplotlib.pyplot as plt
import numpy as np

patient = 'Equilibrio/Paulo'

EMG_data, EMG_time, EMG_labels, EMG_def, ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def = load_data_h5(patient)

time_data = read_config(patient)

tare(time_data['Tare'], ForcePlatform_data, ForcePlatform_def[1], ForcePlatform_def[0])

plt.plot(ForcePlatform_time, ForcePlatform_data[:, 0:4])

plt.show()
