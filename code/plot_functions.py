import seaborn
import matplotlib.pyplot as plt

def raw_dump_grid(segment_name):
    f = plt.figure()
    plt.figtext(0.08, 0.95, segment_name, fontsize=20)
    gs1 = GridSpec(2, 1)
    gs1.update(left=0.04, right=0.48, hspace=0.25)

    gs1_ax1 = plt.subplot(gs1[0, :])
    gs1_ax2 = plt.subplot(gs1[1, :])

    gs1_ax = [gs1_ax1, gs1_ax2]

    gs2 = GridSpec(4, 1)
    gs2.update(left=0.52, right=0.98, wspace=0.3, hspace=0.25)

    gs2_ax1 = plt.subplot(gs2[0, :])
    gs2_ax2 = plt.subplot(gs2[1, :])
    gs2_ax3 = plt.subplot(gs2[2, :])
    gs2_ax4 = plt.subplot(gs2[3, :])

    gs2_ax = [gs2_ax1, gs2_ax2, gs2_ax3, gs2_ax4]

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, gs1_ax, gs2_ax
