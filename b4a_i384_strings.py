from b4a_i384 import b4a_i384_get, b4a_i384_set
from b4a_i384_lists import b4a_i384_get_list, b4a_i384_set_list

stI5 = 0
stI6 = 1
stI7 = 2
stI8 = 3

stI5_symbols = {}
stI5_inv_symbols = {}

stI6_symbols = {
    1: 'а', 2: 'б', 3: 'в', 4: 'г', 5: 'д', 
    6: 'е', 7: 'ё', 8: 'ж', 9: 'з', 10: 'и', 
    11: 'й', 12: 'к', 13: 'л', 14: 'м', 15: 'н', 
    16: 'о', 17: 'п', 18: 'р', 19: 'с', 20: 'т', 
    21: 'у', 22: 'ф', 23: 'х', 24: 'ц', 25: 'ч', 
    26: 'ш', 27: 'щ', 28: 'ъ', 29: 'ы', 30: 'ь',
    31: 'э', 32: 'ю', 33: 'я', 34: ' ', 35: ',',
    36: '.', 37: '?', 38: 'a', 39: 'b', 40: 'c', 
    41: 'd', 42: 'e', 43: 'f', 44: 'g', 45: 'h', 
    46: 'i', 47: 'j', 48: 'k', 49: 'l', 50: 'm', 
    51: 'n', 52: 'o', 53: 'p', 54: 'q', 55: 'r', 
    56: 's', 57: 't', 58: 'u', 59: 'v', 60: 'w', 
    61: 'x', 62: 'y', 63: 'z'
}
stI6_inv_symbols = {
    'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 
    'е': 6, 'ё': 7, 'ж': 8, 'з': 9, 'и': 10, 
    'й': 11, 'к': 12, 'л': 13, 'м': 14, 'н': 15, 
    'о': 16, 'п': 17, 'р': 18, 'с': 19, 'т': 20, 
    'у': 21, 'ф': 22, 'х': 23, 'ц': 24, 'ч': 25, 
    'ш': 26, 'щ': 27, 'ъ': 28, 'ы': 29, 'ь': 30, 
    'э': 31, 'ю': 32, 'я': 33, ' ': 34, ',': 35, 
    '.': 36, '?': 37, 'a': 38, 'b': 39, 'c': 40, 
    'd': 41, 'e': 42, 'f': 43, 'g': 44, 'h': 45, 
    'i': 46, 'j': 47, 'k': 48, 'l': 49, 'm': 50, 
    'n': 51, 'o': 52, 'p': 53, 'q': 54, 'r': 55, 
    's': 56, 't': 57, 'u': 58, 'v': 59, 'w': 60, 
    'x': 61, 'y': 62, 'z': 63
}

stI7_symbols = {}
stI7_inv_symbols = {}

stI8_symbols = {}
stI8_inv_symbols = {}


def b4a_i384_get_string(b4a_i384: int, index: int, length: int) -> str:
    st = b4a_i384_get(b4a_i384, index, 2)
    i_list = b4a_i384_get_list(b4a_i384, index + 2, 5 + st, length)

    if st == stI5:
        symbols = stI5_symbols
    elif st == stI6:
        symbols = stI6_symbols
    elif st == stI7:
        symbols = stI7_symbols
    elif st == stI8:
        symbols = stI8_symbols

    return "".join(symbols[i] for i in i_list)


def b4a_i384_set_string(b4a_i384: int, index: int, st: int, value: str) -> int:
    if st == stI5:
        inv_symbols = stI5_inv_symbols
    elif st == stI6:
        inv_symbols = stI6_inv_symbols
    elif st == stI7:
        inv_symbols = stI7_inv_symbols
    elif st == stI8:
        inv_symbols = stI8_inv_symbols
    
    i_list = [inv_symbols[s] for s in value]
    
    b4a_i384 = b4a_i384_set(b4a_i384, index, 2, st)
    b4a_i384 = b4a_i384_set_list(b4a_i384, index + 2, 5 + st, i_list)

    return b4a_i384
