MOD_i128 = 2 ** 128
KEY_i128 = 0xCD0FAA49C38296EC82E9A6D25003F831
IKEY_i128 = pow(KEY_i128, -1, MOD_i128)


def b4a_i128_encode(b4a_i128: int) -> str:
    i128 = ((b4a_i128 + 1) * KEY_i128) % MOD_i128
    data_list = [""] * 32
        
    for i in range(32):
        i4 = i128 >> 4 * i & 0xF
        data_list[i] = chr(97 + i4)
        
    data = "".join(data_list)

    return f"b4a_{data[0:8]}_{data[8:14]}_{data[14:16]}_{data[16:18]}_{data[18:24]}_{data[24:32]}"


def b4a_i128_decode(encoded_b4a_i128: str) -> int:
    i128 = 0
    data_list = []

    for i, s in enumerate(encoded_b4a_i128):
        if i > 3 and s != "_":
            data_list.append(s)

    for i in range(32):
        i4 = ord(data_list[i]) - 97
        i128 |= i4 << 4 * i

    return (i128 * IKEY_i128) % MOD_i128 - 1


def b4a_i128_get(b4a_i128: int, index: int, size: int) -> int:
    return (b4a_i128 >> index) % 2 ** size


def b4a_i128_set(b4a_i128: int, index: int, size: int, value: int) -> int:
    b4a_i128 &= ((((1 << (128 - index - size)) - 1) << (index + size)) | ((1 << index) - 1))
    
    return b4a_i128 | (value % 2 ** size) << index
