from __future__ import annotations

import math
from typing import ClassVar


class i32struct:
    size: int
    i32_list: list[int]

    def __init__(self, size: int) -> None:
        self.size = size
        self.i32_list = [0] * math.ceil(size / 32)
    
    def get(self, index: int, size: int) -> i32struct:
        i = 0

        for i32 in self.i32_list:
            ...
        
        print()

    def set(self, index: int, size: int) -> None:
        ...

    def to_bin(self) -> str:
        s_list = []

        for i, i32 in enumerate(self.i32_list):
            if i + 1 == len(self.i32_list):
                size = self.size % 32
            else:
                size = 32

            s_list.append(format(i32, f'0{size}b'))

        return ''.join(s_list)

    def __str__(self) -> str:
        return f"i32struct{{ { self.to_bin() } }}"

    def __repr__(self) -> str:
        return f"i32struct[{self.size}]"


class i32s_field_meta(type):
    def __getitem__(self, size: int) -> i32s_field:
        return i32s_field(size)

class i32s_field(metaclass=i32s_field_meta):
    size: int

    def __init__(self, size: int) -> None:
        self.size = size


class i32packet:
    i32s: i32struct
    i32s_size: ClassVar[int]
    i32s_fields: ClassVar[dict[str, int]]

    def __init_subclass__(cls) -> i32packet:
        cls.i32s_size = 0
        cls.i32s_fields = {}

        for fname, ftype in cls.__annotations__.items():
            if type(ftype) is str:
                if not ftype.startswith("i32s_field"): 
                    continue

                length = len(ftype)
                digit = ftype[11:length - 1]

                if not digit.isdigit():
                    continue

                fsize = int(digit)
            elif type(ftype) is i32s_field:
                fsize = i32s_field.size
            else:
                continue 
            
            cls.i32s_size += fsize
            cls.i32s_fields[fname] = fsize
        
        return cls

    def __init__(self) -> None:
        self.i32s = i32struct(self.__class__.i32s_size)

    def to_bin(self) -> str:
        s_list = []
        offset = 0

        for fname, fsize in self.__class__.i32s_fields.items():
            field_bin = self.i32s.get(offset, fsize).to_bin()
            
            s_list.append(fname)
            s_list.append("=")
            s_list.append(field_bin)

            offset += fsize

        return ''.join(s_list)

    def __str__(self) -> str:
        return f"i32packet{{ { self.to_bin() } }}"

    def __repr__(self) -> str:
        return f"i32packet[{self.i32s.size}]"


class B4AC_packet(i32packet):
    mt: i32s_field[3]
    client_id: i32s_field[8]
    body: i32s_field[373]


class B4AS_packet(i32packet):
    rt: i32s_field[3]
    client_id: i32s_field[8]
    body: i32s_field[373]


body = i32struct(373)
# body.set()

b4ac_packet = B4AC_packet()
b4ac_packet.mt = 1
b4ac_packet.client_id = 123
b4ac_packet.body = body

print(b4ac_packet)
