MOD_i384 = 2 ** 384
KEY_i384 = 0xFF9594D0AF596B4CD9AF4D7BB0FD5D75BB4385394C89D7A657A1F7CE34522B7AAE68F22B8AD89C66BAB0FF39522126E7
IKEY_i384 = pow(KEY_i384, -1, MOD_i384)

symbols = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',
    5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
    10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
    15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't',
    20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y',
    25: 'z', 26: 'A', 27: 'B', 28: 'C', 29: 'D',
    30: 'E', 31: 'F', 32: 'G', 33: 'H', 34: 'I',
    35: 'J', 36: 'K', 37: 'L', 38: 'M', 39: 'N',
    40: 'O', 41: 'P', 42: 'Q', 43: 'R', 44: 'S',
    45: 'T', 46: 'U', 47: 'V', 48: 'W', 49: 'X',
    50: 'Y', 51: 'Z', 52: '0', 53: '1', 54: '2',
    55: '3', 56: '4', 57: '5', 58: '6', 59: '7',
    60: '8', 61: '9', 62: '(', 63: ')'
}
inv_symbols = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
    'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
    'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29,
    'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34,
    'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39,
    'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44,
    'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49,
    'Y': 50, 'Z': 51, '0': 52, '1': 53, '2': 54,
    '3': 55, '4': 56, '5': 57, '6': 58, '7': 59,
    '8': 60, '9': 61, '(': 62, ')': 63
}


def b4a_i384_encode(b4a_i384: int) -> str:
    i384 = ((b4a_i384 + 1) * KEY_i384) % MOD_i384
    s_list = []
        
    for i in range(64):
        i6 = i384 >> 6 * i & (2 ** 6 - 1)
        s_list.append(symbols[i6])
        
    return f"b4a_{''.join(s_list)}"


def b4a_i384_decode(b4a_i384_encoded: str) -> int:
    i384 = 0

    for i, s in enumerate(b4a_i384_encoded[4:]):
        i6 = inv_symbols[s]
        i384 |= i6 << 6 * i

    return (i384 * IKEY_i384) % MOD_i384 - 1


def b4a_i384_get(b4a_i384: int, index: int, size: int) -> int:
    return (b4a_i384 >> index) % 2 ** size


def b4a_i384_set(b4a_i384: int, index: int, size: int, value: int) -> int:
    b4a_i384 &= ((((1 << (384 - index - size)) - 1) << (index + size)) | ((1 << index) - 1))
    
    return b4a_i384 | (value % 2 ** size) << index
