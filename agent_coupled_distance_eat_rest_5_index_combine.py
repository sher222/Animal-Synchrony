# http://www.pnas.org/content/109/1/227.abstract

import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from matplotlib.patches import Patch

import os
agents = []
V0 = 20
K1 = 2
K2 = 0.5
F = 50
M = 50
R = 0.5
N = F+M
# print(N)
a_arr = np.full((N, N), 0.5)
a_arr_new = np.full((N, N), 0.5)
desire_food = 0
desire_rest = math.pi
m_times = [400, 1000, 1300, 1500, 1600]
names = ["eat", "rest", "travel", "groom", "social"]
areas = [0, 2 * math.pi/5, 4 * math.pi/5, 6 * math.pi/5, 8 * math.pi/5, 2 * math.pi]
formated_nice = ["0", r"$\frac{2\pi}{5}$", r"$\frac{4\pi}{5}$", r"$\frac{6\pi}{5}$", r"$\frac{8\pi}{5}$"]
f_times = [300, 1000, 1400, 1700, 1900]
current_state = [0, 0]
class Agent:
    def __init__(self, cAngle, wAngle, g, i, gender):
        self.current_angle = cAngle
        self.angle_wanted = wAngle
        self.group = g
        self.index = i
        self.new_angle = self.current_angle
        self.gender = gender

    def compute(self):
            new_angle = 0.0

            if self.group != 3:
                new_angle = math.sin(self.angle_wanted - self.current_angle)
            for i in range(0, len(agents)):
                if i == self.index:
                    continue
                new_angle += K1/N * a_arr[self.index][i] * math.sin(agents[i].current_angle - self.current_angle)
                # print(agents[i].current_angle, self.current_angle, K/N * math.sin(agents[i].current_angle - self.current_angle), new_angle)

            self.new_angle = new_angle
    def updateAngle(self):
        self.current_angle += self.new_angle

def updateA(i, j):
    # print(i, j)
    # print("a_arr", a_arr[i][j])
    diff = K2 * (1 - a_arr[i][j]) * a_arr[i][j] * (abs(math.cos(0.5 * (agents[i].current_angle - agents[j].current_angle))) - R)
    if abs(diff) < 0.00000000000001:
        diff = 0
    # print(diff)

    a_arr_new[i][j] = a_arr[i][j] + diff
    if abs(a_arr_new[i][j]) < 0.00000000000001:
        a_arr_new[i][j] = 0
    a_arr_new[j][i] = a_arr_new[i][j]
colors = ['#C6F5C6', '#FDECB9', '#8FA1FE', '#FFEC8A', '#CEBEE0']

def print_image(path,hour,index):
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
        ax.add_artist(Wedge((0, 0), 1, areas[i] * 180/math.pi, areas[i + 1] * 180/math.pi, fc=colors[i]))
        ax.text(1.1 * math.cos(areas[i]), 1.1 * math.sin(areas[i]), formated_nice[i])
        av_angle = (areas[i] + areas[(i + 1)])/2
        ax.text(0.5 * math.cos(av_angle) - 0.1, 0.5 * math.sin(av_angle), names[i])
    ax.scatter(x[:F], y[:F], s=10, c='r', marker="s")
    ax.scatter(x[F:F+M], y[F:F+M], s=10, c='b', marker="s")
    ax.text(0.5, -0.1, "Iteration="+str(hour), size=12, ha="center", transform=ax.transAxes)
    ax.text(0.5, -0.2, r"$SC_{spatial}$=" + str(index), size=12, ha="center", transform=ax.transAxes)
    ax.text(0.5, -0.3, "Female phase=" + names[current_state[0]], size=12, ha="center", transform=ax.transAxes)
    ax.text(0.5, -0.4, "Male phase=" + names[current_state[1]], size=12, ha="center", transform=ax.transAxes)

    plt.axis('off')
    plt.savefig(path+".pdf", bbox_inches="tight")
    plt.close(fig)
    # plt.show()
def cp_arr(array, toCopyFrom):
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            array[i][j] = toCopyFrom[i][j]
def computeSCSocial():
    xy_group = np.full((len(areas) - 1, 2), 0)
    for i in agents:
        angle = i.current_angle % (2 * math.pi)
        match = False
        for j in range(0, len(areas) - 1):
            coeff = 0
            if i.gender == 'F':
                coeff = 1
            if areas[j] < angle and angle <= areas[j + 1]:
                xy_group[j][coeff] += 1
                match = True
        if match is False:
            print("FALSE", angle)
    sum = 0
    X = 0
    Y = 0
    for i in range(0, len(xy_group)):
        if xy_group[i][0] + xy_group[i][1] < 2:
            continue
        X += xy_group[i][0]
        Y += xy_group[i][1]
        sum += (xy_group[i][0] * xy_group[i][1])/(xy_group[i][0] +  xy_group[i][1] - 1)
    index = 1 - (X + Y)/(X * Y) * sum
    return index

if __name__ == '__main__':
    # wanted = [500, 7350, 13100, 18950]
    wanted = [50, 750, 4550, 9700, 13100]
    # wanted = [50, 4050, 6300, 7150, 12100]
    #wanted = [1950, 2850, 6400, 7100, 7650]
    # wanted = [1, 2, 3, 4, 5]
    path = "images/agent_coupled_distance_eat_rest_multiple_5/11/"
    f = open(path+"data_param.txt", 'r')
    for i in range(0, 2):
        f.readline()
    myseed = int(f.readline().split(": ")[1])
    for i in range(0, 3):
        f.readline()
    K1 = float(f.readline().split(": ")[1])
    K2 = float(f.readline().split(": ")[1])

    # myseed = 7512064
    print(myseed)
    print("SEED:", myseed)
    random.seed(myseed)

    for i in range(0, F):
        agents.append(Agent(random.random()*2*math.pi, desire_rest, 1, i, 'F'))
    for i in range(F, N):
        agents.append(Agent(random.random()*2*math.pi, desire_rest, 2, i, 'M'))
    # print(len(agents))
    wanted_index = 0

    # fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
    # ax = [fig.add_subplot(2, 2, i + 1) for i in range(4)]
    fig, axs = plt.subplots(int((len(wanted) + 1)/2), 2)
    fig.set_size_inches(6, 6)
    font_size = 5
    under_font_size = 3
    for j in range(0, wanted[-1] + 1):
        if j % 50 == 0:
            print(j)
        sc_social = computeSCSocial()
        if j == wanted[wanted_index]:
            print("found", j)
            x = []
            y = []
            a = []
            for i in agents:
                a.append(i.current_angle)
                y.append(math.sin(i.current_angle))
                x.append(math.cos(i.current_angle))
            # print("angles", a)
            x_index = int(wanted_index/2)
            y_index = wanted_index % 2
            axs[x_index, y_index].axis(xmin=-1.1, xmax=1.1)
            axs[x_index, y_index].axis(ymin=-1.1, ymax=1.1)
            axs[x_index, y_index].set_aspect('equal')
            axs[x_index, y_index].set_xticklabels([])
            axs[x_index, y_index].set_yticklabels([])

            for i in range(0, len(areas) - 1):
                axs[x_index, y_index].add_artist(Wedge((0, 0), 1, areas[i] * 180 / math.pi, areas[i + 1] * 180 / math.pi, fc=colors[i]))
                axs[x_index, y_index].text(1.1 * math.cos(areas[i]), 1.1 * math.sin(areas[i]), formated_nice[i], size=font_size)
                av_angle = (areas[i] + areas[(i + 1)]) / 2
                axs[x_index, y_index].text(0.5 * math.cos(av_angle) - 0.1, 0.5 * math.sin(av_angle), names[i], size=font_size)
            axs[x_index, y_index].scatter(x[:F], y[:F], s=2, c='r', marker="s", label='Female')
            axs[x_index, y_index].scatter(x[F:F + M], y[F:F + M], s=2, c='b', marker="s", label='Male')
            axs[x_index, y_index].text(0.5, -0, "Iteration=" + str(j), size=under_font_size, ha="center", transform=axs[x_index, y_index].transAxes)
            axs[x_index, y_index].text(0.5, -0.05, r"$SC_{spatial}$=" + str(sc_social), size=under_font_size, ha="center", transform=axs[x_index, y_index].transAxes)
            axs[x_index, y_index].text(0.5, -0.1, "Female phase=" + names[current_state[0]], size=under_font_size, ha="center", transform=axs[x_index, y_index].transAxes)
            axs[x_index, y_index].text(0.5, -0.15, "Male phase=" + names[current_state[1]], size=under_font_size, ha="center", transform=axs[x_index, y_index].transAxes)
            axs[x_index, y_index].text(0.5, -0.2, "("+chr(ord('a') + wanted_index)+")", size=under_font_size, ha="center", transform=axs[x_index, y_index].transAxes, weight='bold')

            if wanted_index == len(wanted) - 1:
                handles, labels = axs[x_index, y_index].get_legend_handles_labels()
                fig.legend(handles, labels, loc='center', prop={'size':font_size})
            axs[x_index, y_index].axis("off")
            # axs[x_index, y_index].set_xticklabels([])
            # axs[x_index, y_index].set_yticklabels([])
            # plt.subplots_adjust(wspace=0, hspace=0)

            wanted_index += 1
        for i in agents:
            i.compute()
        for i in agents:
            i.updateAngle()
        for i in range(0, N):
            for k in range(i + 1, N):
                updateA(i, k)
        for i in range(0, len(f_times)):
            if j % f_times[-1] == f_times[i] % f_times[-1]:
                bounds = [areas[(i + 1) % len(f_times)], areas[(i + 1) % len(f_times) + 1]]
                # print(bounds)
                current_state[0] = (i + 1) % len(f_times)
                for i in agents[:F]:
                    i.angle_wanted = random.random()  * (bounds[1] - bounds[0]) + bounds[0]
        for i in range(0, len(m_times)):
            if j % m_times[-1] == m_times[i] % m_times[-1]:
                bounds = [areas[(i + 1) % len(f_times)], areas[(i + 1) % len(f_times) + 1]]
                # print(bounds)
                current_state[1] = (i + 1) % len(f_times)
                for i in agents[F:]:
                    i.angle_wanted = random.random() * (bounds[1] - bounds[0]) + bounds[0]

        cp_arr(a_arr, a_arr_new)
    print(path)
    axs[-1, -1].set_aspect('equal')

    axs[-1, -1].axis("off")
    # axs[-1,-1].set_xticklabels([])
    # axs[-1,-1].set_yticklabels([])

    plt.subplots_adjust(wspace=0, hspace=0.2)
    plt.savefig(path + "combined.pdf", bbox_inches="tight")
    plt.close(fig)
    # print_image(path+"image_final", iteratio)
