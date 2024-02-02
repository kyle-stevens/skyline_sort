from operator import attrgetter, lt, gt, le, ge

from enum import Enum

import matplotlib.pyplot as plt

iterations = 0

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    _data : list = None
    _parameters : list[str]
    _sort_orders : list[SkylineType]
    _skyline : list = []

    def _dominates(self, object, sort_orders):
        global iterations
        as_good_as_checks = []
        better_than_checks = []
        for operator in sort_orders:
            better_than_checks.append(lt if operator == SkylineType.MINSKYLINE else gt)
            as_good_as_checks.append(le if operator == SkylineType.MINSKYLINE else ge)
        
        for obj in self._data:
            iterations += 1
            if obj == object:
                continue
            if not (
                (
                    all(
                        [as_good_as_checks[it](self._parameters[it](obj), self._parameters[it](object)) for it in range(len(self._sort_orders))]
                    )
                ) and \
                (
                    any(
                        [better_than_checks[it](self._parameters[it](obj), self._parameters[it](object)) for it in range(len(self._sort_orders))]
                    )
                )
                ):
                continue
            else:
                return False
        return True
    
    def sort_skyline(self):
        for obj in self._data:
            if self._dominates(obj, self._sort_orders):
                self._skyline.append(obj)

    def __init__(
        self, _data : list, 
        presort : bool, 
        sort_parameters : list[str], 
        sort_orders : list[SkylineType]
        ) -> None:
        if any(
            [
                (len(sort_parameters) < 2),
                (len(sort_orders) < 2),
                len(sort_orders) != len(sort_parameters)
            ]
        ):
            raise RuntimeError(f'Error: Skyline sort failed. Please ensure that your arguments pass the minimum requirements.' + \
                               f'\n\tSkyline Parameter count {len(sort_parameters)}>=2.' + \
                                f'\n\tSkyline sort_orders count {len(sort_orders)}>=2' + \
                                    f'\n\t{len(sort_parameters)} == {len(sort_orders)}')
        

        self._data = _data
        self._parameters = [attrgetter(param) for param in sort_parameters]
        self._sort_orders = sort_orders
        if presort:
            self._data.sort(key=self._parameters[0], reverse= (self._sort_orders[0] == SkylineType.MAXSKYLINE))

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
        total_iterations.append(iterations)
        print(f'Iteration {t:10}/{num_tests} skyline sort on {num_persons:10}: {duration:15} seconds. Took {iterations:10} iterations to complete.')
    dprint(f'Average Time on {num_persons:10} elements with {len(sort_parameters_test):10} parameters: {(sum(times) / num_tests):15} seconds - {time.time()}. Average Iterations: {sum(total_iterations) / len(total_iterations)}')
    
    
