from operator import attrgetter

from enum import Enum

import matplotlib.pyplot as plt

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    unsorted_objects : list = None
    skyline_param_1 : str
    skyline_param_2 : str
    skyline_objs : list = []

    def dominates_min(self, object):
        for obj in self.unsorted_objects:
            if obj == object:
                continue
            if (self.skyline_getter_1(obj) <= self.skyline_getter_1(object) and \
                self.skyline_getter_2(obj) <= self.skyline_getter_2(object)):
                if (self.skyline_getter_1(obj) < self.skyline_getter_1(object) or \
                    self.skyline_getter_2(obj) < self.skyline_getter_2(object)):
                    return False
        return True
    def dominates_max(self, object):
        for obj in self.unsorted_objects:
            if obj == object:
                continue
            if (self.skyline_getter_1(obj) >= self.skyline_getter_1(object) and \
                self.skyline_getter_2(obj) >= self.skyline_getter_2(object)):
                if (self.skyline_getter_1(obj) > self.skyline_getter_1(object) or \
                    self.skyline_getter_2(obj) > self.skyline_getter_2(object)):
                    return False
        return True
    def sort_skyline(self):
        for obj in self.unsorted_objects:
            if (self.skyline_type == SkylineType.MAXSKYLINE):
                if self.dominates_max(obj):
                    self.skyline_objs.append(obj)
            elif (self.skyline_type == SkylineType.MINSKYLINE):
                if self.dominates_min(obj):
                    self.skyline_objs.append(obj)
    def __init__(
        self, unsorted_objects : list, 
        skyline_param_1 : str, 
        skyline_param_2 : str,
        operator : SkylineType
        ) -> None:
        self.unsorted_objects = unsorted_objects
        self.skyline_param_1 = skyline_param_1
        self.skyline_getter_1 = attrgetter(self.skyline_param_1)
        self.skyline_param_2 = skyline_param_2
        self.skyline_getter_2 = attrgetter(self.skyline_param_2)
        self.skyline_type = operator

        self.sort_skyline()

class Person:
    def __init__(self, name, age, score) -> None:
        self.name = name 
        self.age = age 
        self.score = score

if __name__ == '__main__':
    people = [Person("Alice", 25,30),Person("Bob", 28,40),Person("Charlie", 26,25),
              Person("David", 45,59),Person("Edgar", 65,16),Person("Francine", 25,60),
              Person("Gordon", 15,98),Person("Harriet", 92,30),Person("Isobel", 25,30)]
    
    skyline = SkylineSort(people, "age", "score", SkylineType.MINSKYLINE)
    [print(x.name) for x in skyline.skyline_objs]


    x_values = [obj.age for obj in people]
    y_values = [obj.score for obj in people]

    plt.figure(figsize=(8,6))
    plt.scatter(x_values, y_values)
    for i in range(0, len(people)):
        plt.annotate(people[i].name, (people[i].age, people[i].score))


    x_line = []
    y_line = []
    skyline_objs = skyline.skyline_objs
    skyline_objs.sort(key=attrgetter('age'))
    for skyline_obj in skyline_objs:
        x_line.append(skyline_obj.age)
        y_line.append(skyline_obj.score)
    plt.plot(x_line, y_line, color='blue', linestyle='--')
    plt.show()
    
