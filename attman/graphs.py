from matplotlib import pyplot as plt
from matplotlib import *

def graph(dates, attended):
    save_results_to = 'attman/static/graphs/'
    plt.plot(dates, attended)
    plt.xlabel('Date')  
    plt.ylabel('Total Students Attended')
    plt.title('Analysis')
    plt.savefig(save_results_to + 'Analysis.png')