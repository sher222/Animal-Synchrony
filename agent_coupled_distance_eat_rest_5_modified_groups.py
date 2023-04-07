# http://www.pnas.org/content/109/1/227.abstract

import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from matplotlib.patches import Patch

import os
import statistics
agents = []
V0 = 20
K1 = 0.1
K2 = 0.1
F = 20
K0 = 0.2
M = 20
R = 0.85
group_boost = 40
group_starting = 1
N = F+M
# print(N)
iteration = 0
verbose = True
a_arr = np.full((N, N), 0.5)
a_arr_new = np.full((N, N), 0.5)
desire_food = 0
desire_rest = math.pi
m_times = [40, 100, 130, 150, 160]
names = ["eat", "rest", "travel", "groom", "social"]
areas = [0, 2 * math.pi/5, 4 * math.pi/5, 6 * math.pi/5, 8 * math.pi/5, 2 * math.pi]
formated_nice = ["0", r"$\frac{2\pi}{5}$", r"$\frac{4\pi}{5}$", r"$\frac{6\pi}{5}$", r"$\frac{8\pi}{5}$"]
f_times = [30, 100, 140, 170, 190]
MF_sum = 0
MF_num = 0
MM_sum = 0
MM_num = 0
FF_sum = 0
FF_num = 0
G_sum = 0
G_num = 0
NG_sum = 0
NG_num = 0
STD_av = 0
current_state = [0, 0]
# small_groups = [[0, 9], [10, 19], [20, 29], [30, 39], [40, 49], [50, 59], [60, 69], [70, 79], [80, 89], [90, 99]]
small_groups = [[0, 4], [5, 9], [10, 14], [15, 19], [20, 24], [25, 29], [30, 34], [35, 39]]
group_average = []
class Agent:
    def __init__(self, cAngle, wAngle, g, i, sg):
        self.current_angle = cAngle
        self.angle_wanted = wAngle
        self.group = g
        self.index = i
        self.new_angle = self.current_angle
        self.small_group = sg
    def compute(self):
            new_angle = K0 * math.sin(self.angle_wanted - self.current_angle)
            for i in range(0, len(agents)):
                if i == self.index:
                    continue
                boosted = 0
                if agents[i].small_group == self.small_group:
                    boosted = group_boost

                new_angle += K1/N * (a_arr[self.index][i] + boosted) * math.sin(agents[i].current_angle - self.current_angle)
                # print(agents[i].current_angle, self.current_angle, K/N * math.sin(agents[i].current_angle - self.current_angle), new_angle)

            self.new_angle = new_angle
    def updateAngle(self):
        self.current_angle = (self.current_angle + self.new_angle) % (2 * math.pi)

def updateA(i, j):
    # print(i, j)
    # print("a_arr", a_arr[i][j])

    diff = K2 * (1 - a_arr[i][j]) * a_arr[i][j] * (abs(math.cos(0.5 * (agents[i].current_angle - agents[j].current_angle))) - R)
    if abs(diff) < 0.00001:
        diff = 0

    global FF_sum, FF_num, MM_sum, MM_num, MF_sum, MF_num, G_sum, G_num, NG_sum, NG_num, STD_av

    a_arr_new[i][j] = a_arr[i][j] + diff
    if agents[i].group == 1 and agents[j].group == 1:

        FF_sum += a_arr_new[i][j]
        FF_num += 1
    elif agents[i].group == 2 and agents[j].group == 2:
        MM_sum += a_arr_new[i][j]
        MM_num += 1
    else:
        MF_sum += a_arr_new[i][j]
        MF_num += 1
    if agents[i].small_group == agents[j].small_group:
        G_sum += a_arr_new[i][j]
        G_num += 1
    else:
        NG_sum += a_arr_new[i][j]
        NG_num += 1
    # if agents[i].group != agents[j].group:
    #     if verbose:
    #       print("iteration", iteration, "start", a_arr[i][j], "diff", diff, "new", a_arr_new[i][j], "p", abs(math.cos(0.5 * (agents[i].current_angle - agents[j].current_angle))))
    # if abs(a_arr_new[i][j]) < 0.00000000000001:
    #     a_arr_new[i][j] = 0
    a_arr_new[j][i] = a_arr_new[i][j]
def print_image(path,hour, average):
    colors = ['#C6F5C6', '#FDECB9', '#8FA1FE', '#FFEC8A', '#CEBEE0']
    # group_colors = ['#FFA07A', '#FA8072', '#CD5C5C', '#DC143C', '#8B0000', '#ADD8E6', '#87CEFA', '#6495ED', '#4682B4', '#0000CD']
    group_colors = ['#FFA07A', '#FA8072','#CD5C5C', '#DC143C', '#ADD8E6', '#87CEFA', '#6495ED', '#4682B4']
    x = []
    y = []
    a = []
    for i in agents:
        a.append(i.current_angle)
        y.append(math.sin(i.current_angle))
        x.append(math.cos(i.current_angle))
    # print("angles", a)
    fig, ax = plt.subplots()
    plt.axis('square')
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    for i in range(0, len(areas) - 1):
        ax.add_artist(Wedge((0, 0), 0.98, areas[i] * 180/math.pi, areas[i + 1] * 180/math.pi, fc=colors[i]))
        ax.text(1.1 * math.cos(areas[i]), 1.1 * math.sin(areas[i]), formated_nice[i])
        av_angle = (areas[i] + areas[(i + 1)])/2
        ax.text(0.5 * math.cos(av_angle) - 0.1, 0.5 * math.sin(av_angle), names[i])
    for i, arr in enumerate(small_groups):
        ax.scatter(x[arr[0]: arr[1] + 1], y[arr[0]:arr[1] + 1], s = 1, c = group_colors[i], marker='o')
    # ax.scatter(x[:F], y[:F], s=10, c='r', marker="s", label='Female')
    # ax.scatter(x[F:F+M], y[F:F+M], s=10, c='b', marker="s", label='Male')
    handles, labels = ax.get_legend_handles_labels()
    # handles = []
    # labels = []
    handles.append(Patch(facecolor='r', edgecolor='r'))
    labels.append("Female")
    handles.append(Patch(facecolor='b', edgecolor='b'))
    labels.append("Male")

    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Iteration=" + str(hour))
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Female phase=" + names[current_state[0]])
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Male phase=" + names[current_state[1]])
    handles.append(Patch(facecolor='w', edgecolor='w'))
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("R=" + str(R))
    labels.append("MF average=" + str(average))
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Std dev average=" + str(STD_av))
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Group boosted="+str(group_boost))
    handles.append(Patch(facecolor='w', edgecolor='w'))
    labels.append("Group starting="+str(group_starting))
    plt.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=4)
    plt.axis('off')
    plt.savefig(path+".pdf", bbox_inches="tight")
    plt.close(fig)
    # plt.show()
def distance_sqr (x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
def standard_dev(group_index):
    x_sum = 0
    y_sum = 0
    length = small_groups[group_index][1] - small_groups[group_index][0] + 1
    for i in range(small_groups[group_index][0], small_groups[group_index][1] + 1):
        x_sum += math.cos(agents[i].current_angle)
        y_sum += math.sin(agents[i].current_angle)
    midpoint_x = x_sum/length
    midpoint_y = y_sum/length
    # print("(", midpoint_x,",",midpoint_y,")")
    var = 0
    for i in range(small_groups[group_index][0], small_groups[group_index][1] + 1):
        var += distance_sqr(midpoint_x, midpoint_y, math.cos(agents[i].current_angle), math.sin(agents[i].current_angle))
    stdev = math.sqrt(var/length)
    return stdev
def cp_arr(array, toCopyFrom):
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            array[i][j] = toCopyFrom[i][j]
if __name__ == '__main__':
    # path = /Users/sherylhsu/PycharmProjects/synchrony/agent_coupled.py
    myseed = int(random.random() * 10000000)
    # myseed = 4830332
    print("SEED:", myseed)
    random.seed(myseed)
    path = "images/agent_coupled_distance_eat_rest_5_modified_groups/1/"
    index = 2
    while os.path.isdir(path):

        path = "images/agent_coupled_distance_eat_rest_5_modified_groups/"+str(index)+"/"
        index += 1
    print(path)
    os.makedirs(path)
    f = open(path+"data_param.txt", 'w')
    f.write("F:"+str(F)+"\n")
    f.write("M: "+str(M) + "\n")
    f.write('Seed: '+str(myseed) +"\n")
    f.write("Names: "+str(names) + "\n")
    f.write("M parameters: "+str(m_times)+"\n")
    f.write("F parameters: "+str(f_times)+"\n")
    f.write("K0: "+str(K0)+"\n")
    f.write("K1: "+str(K1)+"\n")
    f.write("K2: "+str(K2)+"\n")
    f.write("R: "+str(R)+"\n")
    f.write("Groups: "+str(small_groups)+"\n")
    f.write("Group boosted: "+str(group_boost)+"\n")
    f.write("Group starting: "+str(group_starting)+"\n")

    f.close()
    f = open(path+"a_values.csv", 'w')
    f.write("Iteration, FF_average, MM_average, FM_average, G_average, NG_average, STD_average \n")
    group_index = 0
    for arr in small_groups:
        for i in range(arr[0], arr[1] + 1):
            for j in range(arr[0], arr[1] + 1):
                a_arr[i][j] = group_starting
    print(a_arr)
    print("M", M, "N", N, "F", F)
    for i in range(0, F):
        if i > small_groups[group_index][1]:
            group_index += 1
        agents.append(Agent(random.random()*2*math.pi, desire_rest, 1, i, group_index))
    for i in range(F, N):
        print(i, group_index, small_groups[group_index])
        if i > small_groups[group_index][1]:
            group_index += 1
        agents.append(Agent(random.random()*2*math.pi, desire_rest, 2, i, group_index))
    # print(len(agents))
    for j in range(0, 1000000):

        iteration = j

        for i in agents:
            i.compute()
        group_average = []
        for count, i in enumerate(small_groups):
            sum = 0
            for k in range(i[0], i[1] + 1):
                sum += agents[k].current_angle
            group_average.append(sum/(i[1] - i[0] + 1))
        print("iteration", j)
        # for i in a_arr:
        #     print(i)
        for i in a_arr[5:10]:
            print(i[5:10])
        for i in agents:

            print("group_average:", group_average[i.small_group], "angle_wanted:", i.angle_wanted, "current_angle:", i.current_angle, "adding to angle:", i.new_angle)
            i.updateAngle()
        for i in range(0, N):
            for k in range(i + 1, N):
                updateA(i, k)

        for i in range(0, len(f_times)):
            if j % f_times[-1] == f_times[i] % f_times[-1]:
                bounds = [areas[(i + 1) % len(f_times)], areas[(i + 1) % len(f_times) + 1]]
                if verbose:
                    print(bounds)
                current_state[0] = (i + 1) % len(f_times)
                for i in agents[:F]:
                    i.angle_wanted = random.random()  * (bounds[1] - bounds[0]) + bounds[0]
        for i in range(0, len(m_times)):
            if j % m_times[-1] == m_times[i] % m_times[-1]:
                bounds = [areas[(i + 1) % len(f_times)], areas[(i + 1) % len(f_times) + 1]]
                if verbose:
                    print(bounds)
                current_state[1] = (i + 1) % len(f_times)
                for i in agents[F:]:
                    i.angle_wanted = random.random() * (bounds[1] - bounds[0]) + bounds[0]
        std_sum = 0
        for i in range(0, len(small_groups)):
            std_sum += standard_dev(i)
        STD_av = std_sum/len(small_groups)
        f.write(str(iteration)+","+str(FF_sum/FF_num)+","+str(MM_sum/MM_num)+","+str(MF_sum/MF_num)+","+str(G_sum/G_num)+","+str(NG_sum/NG_num)+","+str(STD_av)+"\n")
        if j % 5 == 0 and verbose:
            print_image(path + "image_" + str(j), j, MF_sum/MF_num)
            print(j, "female phase", names[current_state[0]], "male phase", names[current_state[1]])
        MF_sum = 0
        MF_num = 0
        MM_sum = 0
        MM_num = 0
        FF_sum = 0
        FF_num = 0
        G_sum = 0
        G_num = 0
        NG_sum = 0
        NG_num = 0
        cp_arr(a_arr, a_arr_new)
        if not verbose and j % 100 == 0:
            print("iterations", j)
    f.close()
    # print_image(path+"image_final", iteratio)
