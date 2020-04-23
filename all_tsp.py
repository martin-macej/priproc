import bee_colony
import ant_colony
import artificial_bee_colony
import utils

def artificial_bee_colony_algo(cities, population, forager_percent, scout_percent, cycle_limit, forager_limit):
    print('Artificial bee colony algorithm')
    start = utils.start_timer()
    artificial_bee_colony.main(cities, population, forager_percent, scout_percent, cycle_limit, forager_limit)
    end = utils.end_timer()
    total_time = utils.get_total_time(start, end)
    print('Total time: ', total_time)
    print('\n\n\n')

def bee_colony_algo(cities, bee_count, move_count):
    print('Bee colony algorithm')
    start = utils.start_timer()
    bee_colony.main(bee_count, move_count, cities)
    end = utils.end_timer()
    total_time = utils.get_total_time(start, end)
    print('Total time: ', total_time)
    print('\n\n\n')

def ant_colony_algo(cities, ant_count, generations, alpha, beta, rho, q, strategy):
    print('Ant colony algorithm v', strategy)
    start = utils.start_timer()
    ant_colony.main(cities, ant_count, generations, alpha, beta, rho, q, strategy)
    end = utils.end_timer()
    total_time = utils.get_total_time(start, end)
    print('Total time: ', total_time)
    print('\n\n\n')

bee_colony_algo(50, 100, 4)
ant_colony_algo(50, 100, 10, 1.0, 10.0, 0.5, 10, 1)
ant_colony_algo(50, 100, 10, 1.0, 10.0, 0.5, 10, 2)
ant_colony_algo(50, 100, 10, 1.0, 10.0, 0.5, 10, 3)
artificial_bee_colony_algo(50, 100, 0.5, 0.1, 100, 20)

