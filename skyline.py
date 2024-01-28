from operator import attrgetter, lt, gt, le, ge

from enum import Enum

import matplotlib.pyplot as plt

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    unsorted_objects : list = None
    skyline_getter_1 : str
    skyline_getter_2 : str
    skyline_type_1 : SkylineType
    skyline_type_2 : SkylineType
    skyline_objs : list = []

    def dominates(self, object, operator_1, operator_2):
        comp_1 = lt if operator_1 == SkylineType.MINSKYLINE else gt
        comp_1_ = le if operator_1 == SkylineType.MINSKYLINE else ge
        comp_2 = lt if operator_2 == SkylineType.MINSKYLINE else gt
        comp_2_ = le if operator_2 == SkylineType.MINSKYLINE else ge
        
        for obj in self.unsorted_objects:
            if obj == object:
                continue
            if not (
                (
                    comp_1_(self.skyline_getter_1(obj), self.skyline_getter_1(object)) and \
                    comp_2_(self.skyline_getter_2(obj), self.skyline_getter_2(object))
                ) and \
                (
                    comp_1(self.skyline_getter_1(obj), self.skyline_getter_1(object)) or \
                    comp_2(self.skyline_getter_2(obj), self.skyline_getter_2(object))
                )
                ):
                continue
            else:
                return False
        return True
    
    def sort_skyline(self):
        for obj in self.unsorted_objects:
            if self.dominates(obj, self.skyline_type_1, self.skyline_type_2):
                self.skyline_objs.append(obj)
    def __init__(
        self, unsorted_objects : list, 
        skyline_param_1 : str, 
        operator_1 : SkylineType,
        skyline_param_2 : str,
        operator_2 : SkylineType
        ) -> None:
        self.unsorted_objects = unsorted_objects
        self.skyline_getter_1 = attrgetter(skyline_param_1)
        self.skyline_getter_2 = attrgetter(skyline_param_2)
        self.skyline_type_1 = operator_1
        self.skyline_type_2 = operator_2

        self.sort_skyline()

class Person:
    def __init__(self, name, age, score) -> None:
        self.name = name 
        self.age = age 
        self.score = score

if __name__ == '__main__':
    import random 
    import time

    num_tests       = 0xFF
    num_persons     = 0xFFFFF
    times = []
    for t in range(0, num_tests):
        people = []
        for i in range(0,num_persons):
            people.append(Person(str(i), random.randint(0,100), random.randint(0,100)))
        start = time.time_ns()
        skyline = SkylineSort(people, "age", SkylineType.MINSKYLINE, "score", SkylineType.MAXSKYLINE)
        end = time.time_ns()
        duration = (end - start) / (10 ** 9)
        times.append(duration)
        print(f'Iteration {t}/{num_tests} skyline sort on {num_persons}: {duration} seconds.')
    print(f'\n\nAverage Time on {num_persons} elements: {sum(times) / num_tests} seconds')
    # [print(x.name) for x in skyline.skyline_objs]


    # x_values = [obj.age for obj in people]
    # y_values = [obj.score for obj in people]

    # plt.figure(figsize=(8,6))
    # plt.scatter(x_values, y_values)
    # for i in range(0, len(people)):
    #     plt.annotate(people[i].name, (people[i].age, people[i].score))


    # x_line = []
    # y_line = []
    # skyline_objs = skyline.skyline_objs
    # skyline_objs.sort(key=attrgetter('age'))
    # for skyline_obj in skyline_objs:
    #     x_line.append(skyline_obj.age)
    #     y_line.append(skyline_obj.score)
    # plt.plot(x_line, y_line, color='blue', linestyle='--')
    # plt.show()
    
