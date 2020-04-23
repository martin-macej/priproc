import random as rand
import numpy as np
import utils

class Bee:
    def __init__(self):
        self.visited_cities = []
        self.recruiter = True
        self.dist = 0

    def move(self, move_count, all_cities):
        for i in range(move_count):
            if self.is_not_complete(all_cities):
                unvisited_cities = []
                for city_index in all_cities:
                    if self.visited_cities.count(city_index) == 0:
                        unvisited_cities.append(city_index)
                city = unvisited_cities[rand.randint(0, len(unvisited_cities) - 1)]
                self.visited_cities.append(city)
            else:
                break
            self.total_distance()

    def total_distance(self):
        distance = 0.0
        for i in range(len(self.visited_cities) - 1):
            current_city = self.visited_cities[i]
            next_city = self.visited_cities[i + 1]
            distance += utils.get_distance(current_city, next_city)
        distance += utils.get_distance(self.visited_cities[-1], self.visited_cities[0])
        self.distance = distance

    def change_role(self, role):
        self.recruiter = role

    def is_not_complete(self, all_cities):
        return len(self.visited_cities) < len(all_cities)

    def replace_cities(self, nods):
        self.choosen_nodes = nods
        self.total_distance()


def main(bee_count, move_count, cities_count):
    bees = []
    super_extra_ultra_special_intergalactic_bee = Bee()
    all_cities = utils.loadCities(cities_count)

    for i in range(bee_count):
        bees.append(Bee())

    while super_extra_ultra_special_intergalactic_bee.is_not_complete(all_cities):

        for bee in bees:
            bee.move(move_count, all_cities)

        bees = sorted(bees, key=lambda be: be.distance, reverse=False)
        super_extra_ultra_special_intergalactic_bee = bees[0]

        max_distance = max(bees, key=lambda b: b.distance).distance
        min_distance = min(bees, key=lambda b: b.distance).distance
        distance_difference = max_distance - min_distance

        recruiters = []
        for bee in bees:
            Ob = (max_distance - bee.distance) / distance_difference
            probs = np.e ** (-(1 - Ob) / (len(bee.visited_cities) * 0.01))

            if rand.uniform(0, 1) < probs:
                bee.change_role(True)
                recruiters.append(bee)
            else:
                bee.change_role(False)

        divider = sum([(max_distance - bee.distance) / distance_difference for bee in recruiters])
        probs = [((max_distance - bee.distance) / distance_difference) / divider for bee in recruiters]
        
        cumulative_probs = [sum(probs[:x + 1]) for x in range(len(probs))]
        
        for bee in bees:
            if not bee.recruiter:
                rndm = rand.uniform(0, 1)
                selected_bee = Bee()
                for i, cp in enumerate(cumulative_probs):
                    if rndm < cp:
                        selected_bee = recruiters[i]
                        break
                bee.replace_cities(selected_bee.visited_cities[:])

    utils.plot(super_extra_ultra_special_intergalactic_bee.visited_cities)
