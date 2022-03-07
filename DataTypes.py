from __future__ import annotations
from math import ceil

def enum(*seq, **name):
    enums = dict(zip(seq, range(len(seq))), **name)
    return type('Enum', (), enums)

class int_32(int):
    __value__ = 0
    __signed__ = True

    def __init__(self, value = 0):
        self.__value__ = value
        self.__update__()

    def __getattr__(self, name):
        try:
            return self.__value__.__getattribute__(name)
        except:
            return self.__value__

    def __slice__(self, value) -> int:
        return value ^ (2 ** (value.bit_length() - 32)) - 1 << 32 if value.bit_length() > 32 else value

    def __sign__(self, value) -> int:
        if not self.__signed__ and value < 0: return value + 2 ** 32
        elif not self.__signed__ and value >= 0: return value
        t = value & 0xFFFFFFFF
        return t | (-(t & 0x80000000))

    def __update__(self, new = None) -> int:
        if new is None: new = self.__value__
        self.__value__ = self.__evaluate__(new)
        return self.__value__

    def __evaluate__(self, value) -> int:
        return self.__sign__(self.__slice__(value))

    def __package__(self, value, set = False) -> int_32:
        new = int_32(self.__update__(value) if set else self.__evaluate__(value))
        new.__signed__ = self.__signed__
        new.__update__()
        return new

    __pos__ = __round__ = __floor__ = __ceil__ = __trunc__ = __int__ = __hash__ = lambda s: s.__value__
    __neg__ = lambda s: s.__value__ * -1
    __invert__ = lambda s: s.__package__(~s.__value__)
    __abs__ = lambda s: s.__value__ * (1 if s.__value__ >= 0 else -1)
    __repr__ = __unicode__ = lambda s: s.__value__.__repr__()

    __iadd__ = lambda s, o: s.__package__(s.__value__ + o, set = True)
    __isub__ = lambda s, o: s.__iadd__(-o)
    __imul__ = lambda s, o: s.__package__(s.__value__ * o, set = True)
    __idiv__ = __ifloordiv__ = __itruediv__ = lambda s, o: s.__package__(s.__value__ // o, set = True)
    __imod__ = lambda s, o: s.__package__(s.__value__ % o, set = True)
    __ipow__ = lambda s, o: s.__package__(s.__value__ ** o, set = True)
    __ilshift__ = lambda s, o: s.__package__(s.__value__ >> o, set = True)
    __irshift__ = lambda s, o: s.__package__(s.__value__ << o, set = True)
    __iand__ = lambda s, o: s.__package__(s.__value__ & o, set = True)
    __ior__ = lambda s, o: s.__package__(s.__value__ | o, set = True)
    __ixor__ = lambda s, o: s.__package__(s.__value__ ^ o, set = True)

    __add__ = lambda s, o: s.__package__(s.__value__ + o)
    __sub__ = lambda s, o: s.__add__(-o)
    __mul__ = lambda s, o: s.__package__(s.__value__ * o)
    __floordiv__ = __truediv__ = __div__ = lambda s, o: s.__package__(s.__value__ // o)
    __mod__ = lambda s, o: s.__package__(s.__value__ % o)
    __pow__ = lambda s, o: s.__package__(s.__value__ ** o)
    
    __eq__ = lambda s, o: s.__value__ == s.__evaluate__(o)
    __le__ = lambda s, o: s.__value__ <= s.__evaluate__(o)
    __ge__ = lambda s, o: s.__value__ >= s.__evaluate__(o)
    __ne__ = lambda s, o: not s.__eq__(o)
    __lt__ = lambda s, o: not s.__ge__(o)
    __gt__ = lambda s, o: not s.__le__(o)

    def to_bytes(self, pad = False):
        return self.__value__.to_bytes(4 if pad else ceil(self.__value__.bit_length()/8), 'little')

    def from_bytes(self, bytes):
        return self.__package__(int.from_bytes(bytes, 'little'), set = True)

    def to_signed(self):
        self.__signed__ = True
        return self.__package__(self.__value__, set = True)

    def to_unsigned(self):
        self.__signed__ = False
        return self.__package__(self.__value__, set = True)