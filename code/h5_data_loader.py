import h5py
import numpy as np

def load_data_h5(filename):
    f = h5py.File(filename + '.h5','r')


    EMG_Macs = '00:07:80:3B:46:38'

    ForcePlatform_Macs = '00:07:80:B3:83:D5'


    EMG_data_group = f[EMG_Macs + "/raw"]

    ForcePlatform_data_group = f[ForcePlatform_Macs + "/raw"]

    ForcePlatform_def = [f[ForcePlatform_Macs].attrs["sampling rate"], f[ForcePlatform_Macs].attrs["resolution"]]
    EMG_def = [f[EMG_Macs].attrs["sampling rate"], f[EMG_Macs].attrs["resolution"]]

    EMG_data = np.zeros((f[EMG_Macs].attrs["nsamples"], len(EMG_data_group)-1))
    EMG_time = np.linspace(0, f[EMG_Macs].attrs["nsamples"]/f[EMG_Macs].attrs["sampling rate"], f[EMG_Macs].attrs["nsamples"])

    ForcePlatform_data = np.zeros((f[ForcePlatform_Macs].attrs["nsamples"], len(ForcePlatform_data_group)-1))
    ForcePlatform_time = np.linspace(0, f[ForcePlatform_Macs].attrs["nsamples"]/f[ForcePlatform_Macs].attrs["sampling rate"], f[ForcePlatform_Macs].attrs["nsamples"])

    EMG_labels = []
    ForcePlatform_labels = []

    for i in range(0, len(EMG_data_group)-1):

        EMG_labels.append(EMG_data_group['channel_' + str(i+1)].attrs['label'])
        EMG_data[:, i] = EMG_data_group['channel_' + str(i+1)][:, 0]

    for i in range(0, len(ForcePlatform_data_group)-1):

        ForcePlatform_labels.append(ForcePlatform_data_group['channel_' + str(i+1)].attrs['label'])
        ForcePlatform_data[:, i] = ForcePlatform_data_group['channel_' + str(i+1)][:, 0]

    return EMG_data, EMG_time, EMG_labels, EMG_def, ForcePlatform_data, ForcePlatform_time, ForcePlatform_labels, ForcePlatform_def


def load_data_h5_wii(filename):
    h5_file  = h5py.File(filename + '.h5','r')

    EMG_Macs = '00:07:80:3B:46:38'
    EMG_data_group = h5_file[EMG_Macs + "/raw"]

    EMG_data = np.zeros((h5_file[EMG_Macs].attrs["nsamples"], len(EMG_data_group)-1))
    EMG_time = np.linspace(0, h5_file[EMG_Macs].attrs["nsamples"]/h5_file[EMG_Macs].attrs["sampling rate"], h5_file[EMG_Macs].attrs["nsamples"])

    EMG_labels = []

    for i in range(0, len(EMG_data_group)-1):
        EMG_labels.append(EMG_data_group['channel_' + str(i+1)].attrs['label'])
        EMG_data[:, i] = EMG_data_group['channel_' + str(i+1)][:, 0]

    txt_file = file(filename + '_Wii.txt','r')

    lines = txt_file.readlines()
    first_line = lines[0].strip().split(',')
    Wii_labels = first_line[0:4]

    Wii_data = np.zeros((len(lines)-1, 4))
    Wii_time = np.zeros((len(lines)-1, 1))

    for i in range(1, len(lines)):
        temp_ = lines[i].strip().split(';')
        Wii_data[i, :] = temp_[0:4]
        Wii_time[i, :] = temp_[4]

    print Wii_labels, Wii_time



