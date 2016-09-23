import seaborn
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from code.segmentator import Segment
from code.processing_functions import normalize
import numpy as np


def raw_dump_grid(segment_name):
    f = plt.figure()
    plt.figtext(0.08, 0.95, segment_name, fontsize=20)

    gs1 = GridSpec(2, 1)
    gs1.update(left=0.04, right=0.32, hspace=0.15)
    gs1_ax1 = plt.subplot(gs1[0, :])
    gs1_ax2 = plt.subplot(gs1[1, :])

    gs1_ax = [gs1_ax1, gs1_ax2]

    gs2 = GridSpec(3, 1)
    gs2.update(left=0.36, right=0.65, wspace=0.3, hspace=0.15)
    gs2_ax1 = plt.subplot(gs2[0, :])
    gs2_ax2 = plt.subplot(gs2[1, :])
    gs2_ax3 = plt.subplot(gs2[2, :])

    gs2_ax = [gs2_ax1, gs2_ax2, gs2_ax3]

    gs3 = GridSpec(4, 1)
    gs3.update(left=0.69, right=0.98, wspace=0.3, hspace=0.30)

    gs3_ax1 = plt.subplot(gs3[0, :])
    gs3_ax2 = plt.subplot(gs3[1, :])
    gs3_ax3 = plt.subplot(gs3[2, :])
    gs3_ax4 = plt.subplot(gs3[3, :])

    gs3_ax = [gs3_ax1, gs3_ax2, gs3_ax3, gs3_ax4]

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, gs1_ax, gs2_ax, gs3_ax


def raw_dump_normalization(Segment):
    f, gs1_ax, gs2_ax, gs3_ax = raw_dump_grid(Segment.Segment_Name)

    ##

    gs1_ax[0] = axis_populator(gs1_ax[0], normalize(Segment.COPx), normalize(Segment.COPy), "Platform COPs", "COPx", "COPy")
    gs1_ax[0].set_ylim([-0.1, 1.1])
    gs1_ax[0].set_xlim([-0.1, 1.1])
    gs1_ax[1] = axis_populator(gs1_ax[1], normalize(Segment.COPx_EMG), normalize(Segment.COPy_EMG), "EMG COPs", "COPx", "COPy")
    gs1_ax[1].set_ylim([-0.1, 1.1])
    gs1_ax[1].set_xlim([-0.1, 1.1])
    ##

    gs2_ax[0] = axis_populator(gs2_ax[0], Segment.Platform_Time, normalize(Segment.COPx), "COPx", "Time", "COPx")
    gs2_ax[0] = axis_populator(gs2_ax[0], Segment.Platform_Time, normalize(Segment.COPx_EMG), "COPx", "Time", "COPx (EMG)", color='r')
    gs2_ax[0].set_ylim([-1, 2.5])
    gs2_ax[0].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs2_ax[0].legend(["Force Platform", "EMG"], fontsize=8)

    gs2_ax[1] = axis_populator(gs2_ax[1], Segment.Platform_Time, normalize(Segment.COPy), "COPy", "Time", "COPy")
    gs2_ax[1] = axis_populator(gs2_ax[1], Segment.Platform_Time, normalize(Segment.COPy_EMG), "COPy", "Time", "COPy (EMG)", color='r')
    gs2_ax[1].set_ylim([-1, 2.5])
    gs2_ax[1].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs2_ax[1].legend(["Force Platform", "EMG"], fontsize=8)

    gs2_ax[2] = axis_populator(gs2_ax[2], Segment.Platform_Time, Segment.EMGs, "Raw EMG", "Time", "Raw EMG")
    gs2_ax[2].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs2_ax[2].legend(Segment.EMGs_Labels, fontsize=8, loc='best')

    ##

    gs3_ax[0] = axis_populator(gs3_ax[0], Segment.Platform_Time, normalize(Segment.EMGs[:, 0]), "Front Left", "Time", "Raw EMG")
    gs3_ax[0].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs3_ax[0].set_ylim([-0.1, 1.1])
    gs3_ax[1] = axis_populator(gs3_ax[1], Segment.Platform_Time, normalize(Segment.EMGs[:, 1]), "Front Right", "Time", "Raw EMG")
    gs3_ax[1].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs3_ax[1].set_ylim([-0.1, 1.1])
    gs3_ax[2] = axis_populator(gs3_ax[2], Segment.Platform_Time, normalize(Segment.EMGs[:, 2]), "Back Right", "Time", "Raw EMG")
    gs3_ax[2].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs3_ax[2].set_ylim([-0.1, 1.1])
    gs3_ax[3] = axis_populator(gs3_ax[3], Segment.Platform_Time, normalize(Segment.EMGs[:, 3]), "Back Left", "Time", "Raw EMG")
    gs3_ax[3].set_xlim([min(Segment.Platform_Time)-1, max(Segment.Platform_Time)+1])
    gs3_ax[3].set_ylim([-0.1, 1.1])
    ## COP_COMPONENTS

    return f, gs1_ax, gs2_ax, gs3_ax

def axis_populator(axis, x, y, title="", xlabel="", ylabel="", color='k', fontsize=10):

    if(len(np.shape(y)) != 1):
        axis.plot(x, y)
    else:
        axis.plot(x, y, color=color)
    axis.set_xlabel(xlabel, fontsize=fontsize)
    axis.set_ylabel(ylabel, fontsize=fontsize)
    axis.set_title(title, fontsize=fontsize)
    return axis

