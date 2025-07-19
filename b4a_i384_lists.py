from b4a_i384 import b4a_i384_get, b4a_i384_set


def b4a_i384_get_list(b4a_i384: int, index: int, size: int, length: int) -> int:
    return [
        b4a_i384_get(b4a_i384, index + i * size, size)
        for i in range(length)
    ]


def b4a_i384_set_list(b4a_i384: int, index: int, size: int, i_list: list[int]) -> int:
    for i, value in enumerate(i_list):
        b4a_i384 = b4a_i384_set(b4a_i384, index + i * size, size, value)

    return b4a_i384
