from operator import attrgetter, lt, gt, le, ge

from enum import Enum

import matplotlib.pyplot as plt

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    unsorted_objects : list = None
    skyline_getters : list[str]
    skyline_types : list[SkylineType]
    skyline_objs : list = []

    def dominates(self, object, operators):
        # comp_1 = lt if operator_1 == SkylineType.MINSKYLINE else gt
        # comp_1_ = le if operator_1 == SkylineType.MINSKYLINE else ge
        # comp_2 = lt if operator_2 == SkylineType.MINSKYLINE else gt
        # comp_2_ = le if operator_2 == SkylineType.MINSKYLINE else ge

        as_good_as_checks = []
        better_than_checks = []
        for operator in operators:
            better_than_checks.append(lt if operator == SkylineType.MINSKYLINE else gt)
            as_good_as_checks.append(le if operator == SkylineType.MINSKYLINE else ge)
        
        for obj in self.unsorted_objects:
            if obj == object:
                continue
            if not ( #needs reworks for this portion and larger arrays of getters.
                (
                    all(
                        [as_good_as_checks[it](self.skyline_getters[it](obj), self.skyline_getters[it](object)) for it in range(len(self.skyline_types))]
                    )
                    # as_good_as_checks[0](self.skyline_getters[0](obj), self.skyline_getters[0](object)) and \
                    # as_good_as_checks[1](self.skyline_getters[1](obj), self.skyline_getters[1](object))
                ) and \
                (
                    any(
                        [better_than_checks[it](self.skyline_getters[it](obj), self.skyline_getters[it](object)) for it in range(len(self.skyline_types))]
                    )
                    # better_than_checks[0](self.skyline_getters[0](obj), self.skyline_getters[0](object)) or \
                    # better_than_checks[1](self.skyline_getters[1](obj), self.skyline_getters[1](object))
                )
                ):
                continue
            else:
                return False
        return True
    
    def sort_skyline(self):
        for obj in self.sorted_objects:
            if self.dominates(obj, self.skyline_types):
                self.skyline_objs.append(obj)
    def __init__(
        self, unsorted_objects : list, 
        skyline_params : str, 
        operators : SkylineType
        ) -> None:
        self.unsorted_objects = unsorted_objects
        self.skyline_getters = [attrgetter(param) for param in skyline_params]
        self.skyline_types = operators
        self.unsorted_objects.sort(key=self.skyline_getters[0], reverse= (self.skyline_types[0] == SkylineType.MAXSKYLINE))
        self.sorted_objects = self.unsorted_objects

        self.sort_skyline()

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
    for t in range(0, num_tests):
        people = []
        for i in range(0,num_persons):
            people.append(Person(str(i), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)))
        start = time.time_ns()
        skyline = SkylineSort(people, ["age", "score", "random_val1", "random_val2", "random_val3", "random_val4"], [SkylineType.MAXSKYLINE, SkylineType.MAXSKYLINE, SkylineType.MINSKYLINE, SkylineType.MAXSKYLINE])
        end = time.time_ns()
        duration = (end - start) / (10 ** 9)
        times.append(duration)
        print(f'Iteration {t}/{num_tests} skyline sort on {num_persons}: {duration} seconds.')
    dprint(f'Average Time on {num_persons} elements: {sum(times) / num_tests} seconds - {time.time()}')
    
    
