from operator import attrgetter, lt, gt, le, ge

from enum import Enum

class SkylineType(Enum):
    MAXSKYLINE = 1
    MINSKYLINE = 2

class SkylineSort:

    _data : list = None
    _parameters : list[str]
    _sort_orders : list[SkylineType]
    _skyline : list = []

    def _dominates(self, object, sort_orders):
        as_good_as_checks = []
        better_than_checks = []
        for operator in sort_orders:
            better_than_checks.append(lt if operator == SkylineType.MINSKYLINE else gt)
            as_good_as_checks.append(le if operator == SkylineType.MINSKYLINE else ge)
        
        for obj in self._data:
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