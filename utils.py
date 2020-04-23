import matplotlib.pyplot as plt
from scipy.spatial import distance
import math
import time

def plot(cities):
    x = []
    y = []
    for city in cities:
        x.append(city[0])
        y.append(city[1])
    plt.plot(x, y, 'co')
    distance = 0.0
    for _ in range(0, len(cities) - 1):
        x_len = x[_+1] - x[_]
        y_len = y[_+1] - y[_]
        distance = distance + math.hypot(x_len, y_len)
        plt.arrow(x[_], y[_], x_len, y_len, color='r', length_includes_head=True)

    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()

    print('Distance: ', distance)

def loadCities(citiesCount):
    cities = []
    with open('./cities/' + str(citiesCount) + 'cities.txt') as f:
        for line in f.readlines():
            city_array = line.split(' ')
            if len(city_array) == 2:
                cities.append([int(city_array[0]), int(city_array[1])])
            else:
                cities.append([int(city_array[1]), int(city_array[2])])
    return cities

def get_distance(a, b):
    return distance.euclidean(a, b)

def start_timer():
    return time.time()

def end_timer():
    return time.time()

def get_total_time(a, b):
    return b - a