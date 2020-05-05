import random as rand
import numpy as np
import utils

class Bee:
    def __init__(self):
        self.visited_cities = []
        self.recruiter = True
        self.distance = float("inf")

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
    all_cities = utils.loadCities(cities_count)

    super_extra_ultra_special_intergalactic_bee = Bee()
    bees = []
    
    for i in range(bee_count):
        bees.append(Bee())

    while super_extra_ultra_special_intergalactic_bee.is_not_complete(all_cities):

        for bee in bees:
            bee.move(move_count, all_cities)

        bees = sorted(bees, key=lambda be: be.distance, reverse=False)
        super_extra_ultra_special_intergalactic_bee = bees[0]

        max_distance = max(bees, key=lambda b: b.distance).distance
        min_distance = min(bees, key=lambda b: b.distance).distance
        middle_distance_difference = (max_distance + min_distance) / 2

        recruiters = []
        for bee in bees:
            if bee.distance > middle_distance_difference:
                bee.change_role(True)
                recruiters.append(bee)
            else:
                bee.change_role(False)

        for bee in bees:
            if not bee.recruiter:
                rndm = rand.uniform(0, 1)
                selected_bee = Bee()
                if rndm < 0.5:
                    selected_bee = recruiters[rand.randrange(0, len(recruiters) - 1)]
                else:
                    selected_bee = super_extra_ultra_special_intergalactic_bee
                bee.replace_cities(selected_bee.visited_cities[:])

    utils.plot(super_extra_ultra_special_intergalactic_bee.visited_cities)
