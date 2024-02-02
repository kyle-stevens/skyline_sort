from skyline import *

class Person:
    def __init__(self, name, age, score, rand1, rand2, rand3, rand4) -> None:
        self.name = name 
        self.age = age 
        self.score = score
        self.random_val1 = rand1
        self.random_val2 = rand2
        self.random_val3 = rand3
        self.random_val4 = rand4

def dprint(input : str):
    print(input)
    open(f'./sys_log.log', '+a').write(input + '\n')

if __name__ == '__main__':
    import random 
    import time

    num_tests       = 0xFFF
    num_persons     = 0xFF
    times = []
    total_iterations = []
    sort_parameters_test = ["age", "score", "random_val1", "random_val2", "random_val3", "random_val4"]
    skyline_sort_orders_test = [SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE, SkylineType.MINSKYLINE, SkylineType.MAXSKYLINE]
    for t in range(0, num_tests):
        iterations = 0
        people = []
        for i in range(0,num_persons):
            people.append(Person(str(i), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)))
        start = time.time_ns()
        skyline = SkylineSort(
            _data=people, 
            presort=True, 
            sort_parameters=sort_parameters_test, 
            sort_orders=skyline_sort_orders_test
            )
        end = time.time_ns()
        duration = (end - start) / (10 ** 9)
        times.append(duration)
        
        print(f'Iteration {t:10}/{num_tests} skyline sort on {num_persons:10}: {duration:15} seconds.')
    dprint(f'Average Time on {num_persons:10} elements with {len(sort_parameters_test):10} parameters: {(sum(times) / num_tests):15} seconds - {time.time()}.')
    
    
