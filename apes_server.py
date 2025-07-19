app = Client(
    "b4a_bot", 
    api_id=22697385, 
    api_hash="bde422be808ee23d61529420687efa36", 
    phone_number="+380939505096"
)
next_client_id = 0
clients_status: dict[int, int] = {}
clients_bod_list: dict[int, list[int]] = {}

SYMBOLS = {
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
ISYMBOLS = {
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

mtREQUEST_CLIENT_ID = 0
mtSEND_MESSAGE = 1
mtCONTINUE_BOD = 2

rtRET_CLIENT_ID = 0
rtNEW_MESSAGE = 1
rtCONTINUE_BOD = 2

csNONE = 0
csSEND_MESSAGE = 1


def bod_to_list_i6(bod: int) -> list[int]:
    i = 0
    list_i6 = []
    
    while 1:
        i6 = (bod >> 6 * i) % 64

        if i6 == 0:
            return list_i6
        
        list_i6.append(i6)

        i += 1
    

def on_bod_finish(client_id: int) -> None:
    status = clients_status[client_id]
    
    if status == csSEND_MESSAGE:
        print("".join(SYMBOLS[i6] for bod in clients_bod_list[client_id] for i6 in bod_to_list_i6(bod)))

        clients_status[client_id] = csNONE


@app.on_message()
def message_handler(client: Client, message: Message) -> None:
    global next_client_id
    
    if message.chat.id != 7575372807:
        return
    
    message.delete()
    b4a = b4a_decode(message.text)

    method_type = b4a_get(b4a, 0, 3)

    if method_type == mtREQUEST_CLIENT_ID:
        client_id = next_client_id
        next_client_id += 1
        client_hook = b4a_get(b4a, 3, 32)

        clients_status[client_id] = csNONE

        new_b4a = b4a_set(0, 2, 3, rtRET_CLIENT_ID)
        new_b4a = b4a_set(new_b4a, 5, 32, client_hook)
        new_b4a = b4a_set(new_b4a, 37, 8, client_id)
        
        update_b4a(new_b4a)
    elif method_type == mtSEND_MESSAGE:
        client_id = b4a_get(b4a, 3, 8)
        is_finished = b4a_get(b4a, 11, 1)
        bod = b4a_get(b4a, 12, 114)

        clients_status[client_id] = csSEND_MESSAGE
        clients_bod_list[client_id] = [bod]

        if is_finished:
            on_bod_finish(client_id)
        else:
            new_b4a = b4a_set(0, 2, 3, rtCONTINUE_BOD)
            new_b4a = b4a_set(new_b4a, 5, 8, client_id)
            new_b4a = b4a_set(new_b4a, 13, 1, 0)

            update_b4a(new_b4a)
    elif method_type == mtCONTINUE_BOD:
        client_id = b4a_get(b4a, 3, 8)
        is_finished = b4a_get(b4a, 11, 1)
        bod = b4a_get(b4a, 12, 114)

        clients_bod_list[client_id].append(bod)

        if is_finished:
            on_bod_finish(client_id)
        else:
            new_b4a = b4a_set(0, 2, 3, rtCONTINUE_BOD)
            new_b4a = b4a_set(new_b4a, 5, 8, client_id)
            new_b4a = b4a_set(new_b4a, 13, 1, len(clients_bod_list[client_id]) % 2 == 0)

            update_b4a(new_b4a)


app.run()
