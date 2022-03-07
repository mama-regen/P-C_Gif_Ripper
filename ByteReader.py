from math import ceil
from DataTypes import enum, int_32

SeekOrigin = enum('Begin', 'Current', 'End')

class Reader:
    _p: int = 0
    _pointer = lambda s, v = None: s._p if v is None else s.seek(v)
    _data: bytes

    def __init__(self, file_path):
        self._data = open(file_path, "rb").read()

    def __normalize__(self, value):
        return max(0, min(len(self._data), value))

    def seek(self, offset: int, origin: int = 1) -> int:
        self._p = self.__normalize__((self._p * (origin % 2)) + (len(self._data) * (origin == 2)) + offset)
        return self._p

    def read_int32(self) -> int_32:
        val = int_32().from_bytes(self._data[self._pointer():self._pointer(4)])
        return val

    def read_bytes(self, length: int) -> bytes:
        val = self._data[self._pointer():self._pointer(length)]
        return val