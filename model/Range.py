from numbers import Number


def _findIndex(flist, func):
    for i, v in enumerate(flist):
        if func(v):
            return i
    return -1


class Range():
    '''
    Represents a range from one integer to a higher or equal integer. Primarily used for DMX ranges of capabilities.
    '''

    _rangeArray: 'list[Number]'

    def __init__(self, rangeArray: 'list[Number]') -> None:
        self._rangeArray = rangeArray

    def _get_start(self) -> Number:
        return self._rangeArray[0]

    def _get_end(self) -> Number:
        return self._rangeArray[1]

    def _get_center(self) -> Number:
        return int((self.start + self.end) / 2)

    start: Number = property(_get_start)
    end: Number = property(_get_end)
    center: Number = property(_get_center)

    def contains(self, value: Number) -> bool:
        return self.start <= value <= self.end

    def __contains__(self, value: Number) -> bool:
        return self.contains(value)

    def overlapsWith(self, range: 'Range') -> bool:
        return range.end > self.start and range.start < self.end

    def overlapsWithOneOf(self, ranges: 'list[Range]') -> bool:
        return any(self.overlapsWith(r) for r in ranges)

    def isAdjacentTo(self, range: 'Range') -> bool:
        return range.end + 1 == self.start or self.end + 1 == range.start

    def getRangeMergedWith(self, range: 'Range') -> 'Range':
        return Range([min(self.start, range.start), max(self.end, range.end)])

    def toString(self) -> str:
        return str(self.start) if self.start == self.end else f"{self.start}...{self.end}"

    def __str__(self) -> str:
        return self.toString()

    def __repr__(self) -> str:
        return self.toString()

    @staticmethod
    def getMergedRanges(ranges: 'list[Range]') -> 'list[Range]':
        '''Merge specified Range objects. Asserts that ranges don't overlap and that all ranges are valid (start<=end).'''
        mergedRanges = [Range([r.start, r.end]) for r in ranges]

        def mergeRange(ranges: 'list[Range]') -> 'list[Range]':
            could_merge = False
            for i, range_ in enumerate(ranges):
                mergableRangeIndex = _findIndex(
                    ranges, lambda o: o.isAdjacentTo(range_))

                if mergableRangeIndex != -1:
                    ranges[i] = ranges[mergableRangeIndex].getRangeMergedWith(
                        range_)
                    ranges.pop(mergableRangeIndex)
                    could_merge = True
            if could_merge:
                return mergeRange(ranges)
            else:
                return ranges

        return mergeRange(mergedRanges)
