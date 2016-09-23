import numpy as np


def sync_time_vectors(Wii_Time_Vector, Wii_Event, File_Delay_index, Initial_Delay, EMG_Time_Vector):

    delay = Wii_Time_Vector[Wii_Event] - Initial_Delay - EMG_Time_Vector[File_Delay_index]

    new_time_vector = Wii_Time_Vector - delay

    return new_time_vector, delay
