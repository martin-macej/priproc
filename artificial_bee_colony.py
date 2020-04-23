import math
import random
import utils
import sys

class Bee:
    def __init__(self, cities):
        self.role = ''
        self.cities_list = list(cities)
        self.distance = 0
        self.cycle = 0

def make_distance_table(cities):
    length = len(cities)
    table = [[utils.get_distance((cities[i][0], cities[i][1]), (cities[j][0], cities[j][1])) for i in range(0, length)] for j in range(0, length)]
    return table

def get_total_distance_of_path(path, table):
    new_path = list(path)
    new_path.insert(len(path), path[0])
    new_path = new_path[1:len(new_path)]
    coordinates = zip(path, new_path)
    distance = sum([table[i[0]][i[1]] for i in coordinates])
    return round(distance, 3)

def initialize_hive(population, data):
    path = [x[0] for x in enumerate(data)]
    hive = [Bee(path) for i in range(0, population)]
    return hive

def assign_roles(hive, role_percentiles, table):
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'

    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
        random.shuffle(hive[i].cities_list)
        hive[i].distance = get_total_distance_of_path(hive[i].cities_list, table)

    return hive

def mutate_path(path):
    random_idx = random.randint(0, len(path) - 2)
    new_path = list(path)
    new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    return new_path

def forage(bee, table, limit):
    old_path = bee.cities_list
    old_distance = get_total_distance_of_path(old_path, table)
    best_new_path = []
    best_new_dist = -1
    for i in range(5):
        new_path = mutate_path(bee.cities_list)
        new_distance = get_total_distance_of_path(new_path, table)
        if best_new_dist == -1 or new_distance < best_new_dist:
            best_new_path = list(new_path)
            best_new_dist = new_distance

    if best_new_dist < bee.distance:
        bee.cities_list = list(best_new_path)
        bee.distance = best_new_dist
        bee.cycle = 0
    else:
        bee.cycle += 1
    if bee.cycle >= limit:
        bee.role = 'S'
    return bee.distance, list(bee.cities_list)

def scout(bee, table):
    new_path = list(bee.cities_list)
    random.shuffle(new_path)
    bee.cities_list = new_path
    bee.distance = get_total_distance_of_path(new_path, table)
    bee.role = 'F'
    bee.cycle = 0

def waggle(hive, best_distance, table, forager_limit, scout_count):
    best_path = []
    results = []

    for i in range(0, len(hive)):
        if hive[i].role == 'F':
            distance, path = forage(hive[i], table, forager_limit)
            if distance < best_distance:
                best_distance = distance
                best_path = list(hive[i].cities_list)
            results.append((i, distance))

        elif hive[i].role == 'S':
            scout(hive[i], table)

    results.sort(reverse=True, key=lambda tup: tup[1])
    scouts = [tup[0] for tup in results[0:int(scout_count)]]
    for new_scout in scouts:
        hive[new_scout].role = 'S'
    return best_distance, best_path

def recruit(hive, best_distance, best_path, table):
    for i in range(0, len(hive)):
        if hive[i].role == 'O':
            new_path = mutate_path(best_path)
            new_distance = get_total_distance_of_path(new_path, table)
            if new_distance < best_distance:
                best_distance = new_distance
                best_path = new_path
    return best_distance, best_path

def main(cities_count, population, forager_percent, scout_percent, cycle_limit, forager_limit):
    onlooker_percent = 1 - forager_percent
    scout_count = math.ceil(population * scout_percent)
    cycle = 1

    cities = utils.loadCities(cities_count)

    best_distance = sys.maxsize
    best_path = []

    table = make_distance_table(cities)
    hive = initialize_hive(population, cities)
    assign_roles(hive, [onlooker_percent, forager_percent], table)

    while cycle < cycle_limit:
        waggle_distance, waggle_path = waggle(hive, best_distance, table, forager_limit, scout_count)
        if waggle_distance < best_distance:
            best_distance = waggle_distance
            best_path = list(waggle_path)

        recruit_distance, recruit_path = recruit(hive, best_distance, best_path, table)
        if recruit_distance < best_distance:
            best_distance = recruit_distance
            best_path = list(recruit_path)

        cycle += 1

    cities_points = []
    for i in best_path:
        cities_points += [cities[i]]
    utils.plot(cities_points)





# import math
# import random
# import utils
# import sys

# class Bee:
#     def __init__(self, cities):
#         self.role = ''
#         self.cities_list = list(cities)
#         self.distance = 0
#         self.cycle = 0

# def make_distance_table(cities):
#     length = len(cities)
#     table = [[utils.get_distance((cities[i][0], cities[i][1]), (cities[j][0], cities[j][1])) for i in range(0, length)] for j in range(0, length)]
#     return table

# def get_total_distance_of_path(path, table):
#     new_path = list(path)
#     new_path.insert(len(path), path[0])
#     new_path = new_path[1:len(new_path)]
#     coordinates = zip(path, new_path)
#     distance = sum([table[i[0]][i[1]] for i in coordinates])
#     return round(distance, 3)

# def initialize_hive(population, data):
#     path = [x[0] for x in enumerate(data)]
#     hive = [Bee(path) for i in range(0, population)]
#     return hive

# def assign_roles(hive, role_percentiles, table):
#     population = len(hive)
#     onlooker_count = math.floor(population * role_percentiles[0])
#     forager_count = math.floor(population * role_percentiles[1])

#     for i in range(0, onlooker_count):
#         hive[i].role = 'O'

#     for i in range(onlooker_count, (onlooker_count + forager_count)):
#         hive[i].role = 'F'
#         random.shuffle(hive[i].cities_list)
#         hive[i].distance = get_total_distance_of_path(hive[i].cities_list, table)

#     return hive

# def mutate_path(path):
#     random_idx = random.randint(0, len(path) - 2)
#     new_path = list(path)
#     new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
#     return new_path

# def forage(bee, table, limit):
#     new_path = mutate_path(bee.cities_list)
#     new_distance = get_total_distance_of_path(new_path, table)

#     if new_distance < bee.distance:
#         bee.cities_list = new_path
#         bee.distance = new_distance
#         bee.cycle = 0
#     else:
#         bee.cycle += 1
#     if bee.cycle >= limit:
#         bee.role = 'S'
#     return bee.distance, list(bee.cities_list)

# def scout(bee, table):
#     new_path = list(bee.cities_list)
#     random.shuffle(new_path)
#     bee.cities_list = new_path
#     bee.distance = get_total_distance_of_path(new_path, table)
#     bee.role = 'F'
#     bee.cycle = 0

# def waggle(hive, best_distance, table, forager_limit, scout_count):
#     best_path = []
#     results = []

#     for i in range(0, len(hive)):
#         if hive[i].role == 'F':
#             distance, path = forage(hive[i], table, forager_limit)
#             if distance < best_distance:
#                 best_distance = distance
#                 best_path = list(hive[i].cities_list)
#             results.append((i, distance))

#         elif hive[i].role == 'S':
#             scout(hive[i], table)

#     results.sort(reverse=True, key=lambda tup: tup[1])
#     scouts = [tup[0] for tup in results[0:int(scout_count)]]
#     for new_scout in scouts:
#         hive[new_scout].role = 'S'
#     return best_distance, best_path

# def recruit(hive, best_distance, best_path, table):
#     for i in range(0, len(hive)):
#         if hive[i].role == 'O':
#             new_path = mutate_path(best_path)
#             new_distance = get_total_distance_of_path(new_path, table)
#             if new_distance < best_distance:
#                 best_distance = new_distance
#                 best_path = new_path
#     return best_distance, best_path

# def main(cities_count, population, forager_percent, scout_percent, cycle_limit, forager_limit):
#     onlooker_percent = 1 - forager_percent
#     scout_count = math.ceil(population * scout_percent)
#     cycle = 1

#     cities = utils.loadCities(cities_count)

#     best_distance = sys.maxsize
#     best_path = []

#     table = make_distance_table(cities)
#     hive = initialize_hive(population, cities)
#     assign_roles(hive, [onlooker_percent, forager_percent], table)

#     while cycle < cycle_limit:
#         waggle_distance, waggle_path = waggle(hive, best_distance, table, forager_limit, scout_count)
#         if waggle_distance < best_distance:
#             best_distance = waggle_distance
#             best_path = list(waggle_path)

#         recruit_distance, recruit_path = recruit(hive, best_distance, best_path, table)
#         if recruit_distance < best_distance:
#             best_distance = recruit_distance
#             best_path = list(recruit_path)

#         cycle += 1
        
#     cities_points = []
#     for i in best_path:
#         cities_points += [cities[i]]
#     utils.plot(cities_points)