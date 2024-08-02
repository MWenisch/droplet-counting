import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import MaxNLocator

def plotting(filename, directory, specified_name=False):
    data = {}
    data['slice'] = []
    data['time'] = []
    data['drop_num'] = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                data['slice'].append(int(row[0]))
                data['time'].append(float(row[1])/60)
                data['drop_num'].append(int(row[2]))
            line_count+=1

    #Set polt Parameters like ticks, scale, linewidth etc.
    fig = plt.figure(figsize=(3, 3))
    plt.xlabel('Time [min]', fontsize=12)
    plt.ylabel('Droplet Number', fontsize=12)
    # Remove the top and right spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Change the line width of the bottom and left spines
    linewidth = 1.5  # You can adjust this value as needed
    ax.spines['bottom'].set_linewidth(linewidth)
    ax.spines['left'].set_linewidth(linewidth)

    # Set the number of ticks on both axes
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    # Move ticks inside the plot area
    ax.tick_params(axis='both', direction='in', width=linewidth, labelsize=12)

    # Set x-axis limits to include zero
    #ax.set_ylim(bottom=0, top = 10)
    fig.tight_layout()

    plt.plot (data['time'], data['drop_num'], 'kx-', markersize=5, markeredgewidth=1.5, linewidth=0.7, markerfacecolor='none')
    if specified_name:
        plot_name = '/' + specified_name + '_droplet_count_plot.png'
        plt.savefig(directory + plot_name, dpi=300, transparent=True)
        plt.show()
    else:
        plot_name = '/droplet_count_plot.png'
        plt.savefig(directory + plot_name, dpi=300, transparent=True)
        plt.show()
