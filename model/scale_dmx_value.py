class DmxScaler():
    @staticmethod
    def getBytes(dmxValue: int, resolution: int) -> 'list[int]':
        bytes_ = []

        while resolution > 0:
            byte = dmxValue % 256
            bytes_.append(byte)
            dmxValue = (dmxValue - byte) / 256
            resolution -= 1

        if dmxValue > 0:
            raise ValueError(
                "Given DMX value was outside the given resolution")

        return list(reversed(bytes_))

    @staticmethod
    def bytesToDmxValue(bytes_: 'list[int]') -> int:
        dmxValue = 0

        for index, byte in enumerate(bytes_):
            dmxValue += byte * 256**(len(bytes_) - index - 1)

        return dmxValue

    @classmethod
    def scaleDmxRangeIndividually(cls, dmxRangeStart: int, startResolution: int, dmxRangeEnd: int, endResolution: int, desiredResolution: int) -> 'tuple[int, int]':
        startBytes = cls.getBytes(dmxRangeStart, startResolution)
        endBytes = cls.getBytes(dmxRangeEnd, endResolution)

        while endResolution < desiredResolution:
            endBytes.append(255)
            endResolution += 1

        while startResolution < desiredResolution:
            startBytes.append(0)
            startResolution += 1

        while endResolution > desiredResolution:
            endBytes.pop()
            endResolution -= 1

        while startResolution > desiredResolution:
            deletedStartByte = startBytes.pop()
            startResolution -= 1

            if deletedStartByte > 0 and cls.bytesToDmxValue(startBytes) < cls.bytesToDmxValue(endBytes):
                startBytes = cls.getBytes(cls.bytesToDmxValue(
                    startBytes) + 1, startResolution)

        return (cls.bytesToDmxValue(startBytes), cls.bytesToDmxValue(endBytes))

    @classmethod
    def scaleDmxRange(cls, dmxRangeStart: int, dmxRangeEnd: int, currentResolution: int, desiredResolution: int) -> 'tuple[int, int]':
        return cls.scaleDmxRangeIndividually(dmxRangeStart, currentResolution, dmxRangeEnd, currentResolution, desiredResolution)

    @classmethod
    def scaleDmxValue(cls, dmxValue: int, currentResolution: int, desiredResolution: int) -> int:
        bytes_ = cls.getBytes(dmxValue, currentResolution)

        while currentResolution < desiredResolution:
            bytes_.append(bytes_[currentResolution - 1])
            currentResolution += 1

        while currentResolution > desiredResolution:
            bytes_.pop()
            currentResolution -= 1

        return cls.bytesToDmxValue(bytes_)
