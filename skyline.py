from operator import attrgetter, lt, gt, le, ge

from enum import Enum

import matplotlib.pyplot as plt

iterations = 0

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    unsorted_objects : list = None
    skyline_getters : list[str]
    skyline_types : list[SkylineType]
    skyline_objs : list = []

    def dominates(self, object, operators):
        global iterations
        as_good_as_checks = []
        better_than_checks = []
        for operator in operators:
            better_than_checks.append(lt if operator == SkylineType.MINSKYLINE else gt)
            as_good_as_checks.append(le if operator == SkylineType.MINSKYLINE else ge)
        
        for obj in self.unsorted_objects:
            iterations += 1
            if obj == object:
                continue
            if not ( #needs reworks for this portion and larger arrays of getters.
                (
                    all(
                        [as_good_as_checks[it](self.skyline_getters[it](obj), self.skyline_getters[it](object)) for it in range(len(self.skyline_types))]
                    )
                ) and \
                (
                    any(
                        [better_than_checks[it](self.skyline_getters[it](obj), self.skyline_getters[it](object)) for it in range(len(self.skyline_types))]
                    )
                )
                ):
                continue
            else:
                return False
        return True
    
    def dominates_dual_variate(self, object, operator_1, operator_2):
        global iterations
        comp_1 = lt if operator_1 == SkylineType.MINSKYLINE else gt
        comp_1_ = le if operator_1 == SkylineType.MINSKYLINE else ge
        comp_2 = lt if operator_2 == SkylineType.MINSKYLINE else gt
        comp_2_ = le if operator_2 == SkylineType.MINSKYLINE else ge
        
        for obj in self.unsorted_objects:
            iterations += 1
            if obj == object:
                continue
            if not (
                (
                    comp_1_(self.skyline_getters[0](obj), self.skyline_getters[0](object)) and \
                    comp_2_(self.skyline_getters[1](obj), self.skyline_getters[1](object))
                ) and \
                (
                    comp_1(self.skyline_getters[0](obj), self.skyline_getters[0](object)) or \
                    comp_2(self.skyline_getters[1](obj), self.skyline_getters[1](object))
                )
                ):
                continue
            else:
                return False
        return True
    
    def sort_skyline_multi_variate(self):
        for obj in self.skyline_candidates:
            if self.dominates(obj, self.skyline_types):
                self.skyline_objs.append(obj)
    
    def sort_skyline_dual_variate(self):
        for obj in self.skyline_candidates:
            if self.dominates_dual_variate(obj, self.skyline_types[0], self.skyline_types[1]):
                self.skyline_objs.append(obj)

    def __init__(
        self, unsorted_objects : list, 
        presort : bool, 
        skyline_params : list[str], 
        operators : list[SkylineType]
        ) -> None:
        if len(skyline_params) < 2:
            raise RuntimeError("Must perform skyline on at least 2 parameters")
        if len(operators) < 2:
            raise RuntimeError("Must perform skyline with at least 2 operators")
        if len(operators) != len(skyline_params):
            raise RuntimeError("Number of parameters and number of skyline types must be equal.")
        

        self.unsorted_objects = unsorted_objects
        self.skyline_getters = [attrgetter(param) for param in skyline_params]
        self.skyline_types = operators
        if presort:
            self.unsorted_objects.sort(key=self.skyline_getters[0], reverse= (self.skyline_types[0] == SkylineType.MAXSKYLINE))
        self.skyline_candidates = self.unsorted_objects

        if len(operators) == 2: # Use more efficient two variable algorithm
            self.sort_skyline_dual_variate()
        else:
            self.sort_skyline_multi_variate()

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

    num_tests       = 0xFF
    num_persons     = 0xFF
    times = []
    total_iterations = []
    skyline_params_test = ["age", "score", "random_val1"] #, "random_val2", "random_val3", "random_val4"]
    skyline_operators_test = [SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE] #, SkylineType.MAXSKYLINE, SkylineType.MINSKYLINE, SkylineType.MAXSKYLINE]
    for t in range(0, num_tests):
        iterations = 0
        people = []
        for i in range(0,num_persons):
            people.append(Person(str(i), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)))
        start = time.time_ns()
        skyline = SkylineSort(
            unsorted_objects=people, 
            presort=True, 
            skyline_params=skyline_params_test, 
            operators=skyline_operators_test
            )
        end = time.time_ns()
        duration = (end - start) / (10 ** 9)
        times.append(duration)
        total_iterations.append(iterations)
        print(f'Iteration {t}/{num_tests} skyline sort on {num_persons}: {duration} seconds. Took {iterations} iterations to complete.')
    dprint(f'Average Time on {num_persons} elements with {len(skyline_params_test)} parameters: {sum(times) / num_tests} seconds - {time.time()}. Average Iterations: {sum(total_iterations) / len(total_iterations)}')
    
    
