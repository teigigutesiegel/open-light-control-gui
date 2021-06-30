from typing import Any, Literal, Callable, Match
import locale
import re
from functools import cmp_to_key


class Matrix():
    '''
    Contains information of how the pixels in a 1-, 2- or 3-dimensional space are arranged and named.
    '''
    _jsonObject: 'dict[str, Any]'
    _cache: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}

    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject

    def _set_jsonObject(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}

    def _get_pixelCount(self) -> 'list[int]':
        if not "pixelCount" in self._cache.keys():
            if "pixelCount" in self._jsonObject.keys():
                self._cache["pixelCount"] = self._jsonObject["pixelCount"]
            elif "pixelKeys" in self._jsonObject.keys():
                xyz = [1, 1, len(self.pixelKeyStructure)]

                for yItems in self.pixelKeyStructure:
                    xyz[1] = max(xyz[1], len(yItems))

                    for xItems in yItems:
                        xyz[0] = max(xyz[0], len(xItems))
                
                self._cache["pixelCount"] = xyz
            else:
                raise ValueError('Either pixelCount or pixelKeys has to be specified in a fixture\'s matrix object.')
        
        return self._cache["pixelCount"]

    def _get_pixelCountX(self) -> int:
        return self.pixelCount[0]

    def _get_pixelCountY(self) -> int:
        return self.pixelCount[1]

    def _get_pixelCountZ(self) -> int:
        return self.pixelCount[2]

    def _get_definedAxes(self) -> 'list[str]':
        if not "definedAxes" in self._cache.keys():
            self._cache["definedAxes"] = []

            if self.pixelCountX > 1:
                self._cache["definedAxes"].append("X")
            if self.pixelCountY > 1:
                self._cache["definedAxes"].append("Y")
            if self.pixelCountZ > 1:
                self._cache["definedAxes"].append("Z")

        return self._cache["definedAxes"]

    def _get_pixelKeyStructure(self) -> 'list[list[list[str]]]':
        if not "pixelKeyStructure" in self._cache.keys():
            if "pixelKeys" in self._jsonObject.keys():
                self._cache["pixelKeyStructure"] = self._jsonObject["pixelKeys"]
            elif "pixelCount" in self._jsonObject.keys():
                self._cache["pixelKeyStructure"] = self._getPixelDefaultKeys()
            else:
                raise ReferenceError(
                    "Either pixelCount or pixelKeys has to be specified in a fixture's matrix object.")

        return self._cache["pixelKeyStructure"]

    def _getPixelDefaultKeys(self) -> 'list[list[list[str]]]':
        '''Generate default keys for all pixels.'''
        zItems = []

        for z in range(1, self.pixelCountZ + 1):
            yItems = []
            for y in range(1, self.pixelCountY + 1):
                xItems = []
                for x in range(1, self.pixelCountX + 1):
                    xItems.append(self._getPixelDefaultKey(x, y, z))
                yItems.append(xItems)
            zItems.append(yItems)

        return zItems

    def _getPixelDefaultKey(self, x: int = 0, y: int = 0, z: int = 0) -> str:
        '''
        Generate default name based on defined axes and given position if no custom names are set via `pixelKeys`.
        '''
        def sec(x, y, z):
            first = x if "X" in self.definedAxes else y
            last = y if "Y" in self.definedAxes else z
            return f"({first}, {last})"

        try:
            return {
                1: str(max(x, y, z)),
                2: sec(x, y, z),
                3: f"{x}, {y}, {z}"
            }.get(len(self.definedAxes))
        except:
            raise ValueError("Only 1, 2 or 3 axes can be defined.")

    def _get_pixelKeys(self) -> 'list[str]':
        if not "pixelKeys" in self._cache.keys():
            self._cache["pixelKeys"] = sorted(
                self.pixelKeyPositions, key=locale.strxfrm)

        return self._cache["pixelKeys"]

    def _get_pixelKeyPositions(self) -> 'dict[str, list[int]]':
        if not "pixelKeyPositions" in self._cache.keys():
            self._cache["pixelKeyPositions"] = {}

            for z in range(self.pixelCountZ):
                for y in range(self.pixelCountY):
                    for x in range(self.pixelCountX):
                        if self.pixelKeyStructure[z][y][x] != None:
                            self._cache["pixelKeyPositions"][self.pixelKeyStructure[z][y][x]] = [
                                x+1, y+1, z+1]

        return self._cache["pixelKeyPositions"]

    def _get_pixelGroupKeys(self) -> 'list[str]':
        if not "pixelGroupKeys" in self._cache.keys():
            self._cache["pixelGroupKeys"] = list(self.pixelGroups.keys())

        return self._cache["pixelGroupKeys"]

    def _get_pixelGroups(self) -> 'dict[str, list]':
        if not "pixelGroups" in self._cache.keys():
            def convertConstraintsToFunctions(constraints: 'dict[str, list[str]]') -> 'dict[str, Callable[[int, int], bool]]':
                constraintFunctions = {}

                for axis in ["x", "y", "z"]:
                    for constraint in constraints.get(axis, []):
                        constraintFunctions[axis] = []
                        if constraint.startswith("="):
                            eqPos = int(constraint[1:])
                            constraintFunctions[axis].append(
                                lambda pos, eqPos=eqPos: pos == eqPos)
                            continue
                        if constraint.startswith(">="):
                            minPos = int(constraint[2:])
                            constraintFunctions[axis].append(
                                lambda pos, minPos=minPos: pos >= minPos)
                            continue
                        if constraint.startswith("<="):
                            maxPos = int(constraint[2:])
                            constraintFunctions[axis].append(
                                lambda pos, maxPos=maxPos: pos <= maxPos)
                            continue
                        
                        constraint = "2n" if constraint == "even" else constraint
                        constraint = "2n+1" if constraint == "odd" else constraint

                        match = re.compile("^(\d+)n(?:\+(\d+)|)$").match(constraint)
                        if match:
                            divisor = int(match.groups()[0])
                            remainder = int(match.groups()[1]) if match.groups()[1] else 0
                            constraintFunctions[axis].append(
                                lambda pos, div=divisor, rem=remainder: pos % div == rem)
                            continue

                        raise ValueError(
                            f"Invalid pixel key constraint '{constraint}'.")

                constraintFunctions["name"] = []
                for pattern in constraints.get("name", []):
                    constraintFunctions["name"].append(
                        lambda name, pat=pattern: bool(re.match(pat, name)))

                return constraintFunctions

            self._cache["pixelGroups"] = {}

            if "pixelGroups" in self._jsonObject.keys():
                for groupKey, group in self._jsonObject["pixelGroups"].items():
                    if isinstance(group, list):
                        self._cache["pixelGroups"][groupKey] = group
                    elif group == "all":
                        self._cache["pixelGroups"][groupKey] = self.pixelKeys
                    else:
                        constraints = convertConstraintsToFunctions(group)
                        pixelKeys = self.pixelKeys if "name" in group else self.getPixelKeysByOrder(
                            "X", "Y", "Z")

                        self._cache["pixelGroups"][groupKey] = list(filter(
                            lambda key: self._pixelKeyFulfillsConstraints(key, constraints), pixelKeys))

        return self._cache["pixelGroups"]

    def _pixelKeyFulfillsConstraints(self, pixelKey: str, constraints: 'dict[str, Callable[[int, int], bool]]') -> bool:
        position = self.pixelKeyPositions[pixelKey]

        temp = []
        for axisIndex, axis in enumerate(["x", "y", "z"]):
            axisPos = position[axisIndex]
            temp.append(all(func(axisPos) for func in constraints.get(axis, [])))

        numberConstraintsFulfilled = all(temp)
        stringConstraintsFulfilled = all(
            func(pixelKey) for func in constraints["name"])

        return numberConstraintsFulfilled and stringConstraintsFulfilled

    jsonObject: 'dict[str, Any]' = property(_get_jsonObject, _set_jsonObject)
    pixelCount: 'list[int]' = property(_get_pixelCount)
    pixelCountX: int = property(_get_pixelCountX)
    pixelCountY: int = property(_get_pixelCountY)
    pixelCountZ: int = property(_get_pixelCountZ)
    definedAxes: 'list[str]' = property(_get_definedAxes)
    pixelKeyStructure: 'list[list[list[str]]]' = property(
        _get_pixelKeyStructure)
    pixelKeys: 'list[str]' = property(_get_pixelKeys)
    pixelKeyPositions: 'dict[str, list[int]]' = property(
        _get_pixelKeyPositions)
    pixelGroupKeys: 'list[str]' = property(_get_pixelGroupKeys)
    pixelGroups: 'dict[str, list]' = property(_get_pixelGroups)

    def getPixelKeysByOrder(self, firstAxis: 'Literal["X", "Y", "Z"]', secondAxis: 'Literal["X", "Y", "Z"]', thirdAxis: 'Literal["X", "Y", "Z"]') -> 'list[str]':
        axisToPosIndex = {"X": 0, "Y": 1, "Z": 2}
        firstPosIndex = axisToPosIndex[firstAxis]
        secondPosIndex = axisToPosIndex[secondAxis]
        thirdPosIndex = axisToPosIndex[thirdAxis]

        def sorter(keyA, keyB):
            posA = self.pixelKeyPositions[keyA]
            posB = self.pixelKeyPositions[keyB]

            if posA[thirdPosIndex] != posB[thirdPosIndex]:
                return posA[thirdPosIndex] - posB[thirdPosIndex]
            if posA[secondPosIndex] != posB[secondPosIndex]:
                return posA[secondPosIndex] - posB[secondPosIndex]
            return posA[firstPosIndex] - posB[firstPosIndex]

        return sorted(self.pixelKeys, key=cmp_to_key(sorter))
