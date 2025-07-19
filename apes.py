from threading import Thread

import b4as
from b4as import app, b4as_create_ports, b4as_accept, b4as_recv, b4as_send, b4as_ClientDisconnection, rtSEND_DATA
from b4a_i384 import b4a_i384_get, b4a_i384_set
from b4a_i384_lists import b4a_i384_get_list, b4a_i384_set_list
from b4a_i384_strings import b4a_i384_get_string, b4a_i384_set_string, stI6

b4as.logs = True

b4as_create_ports({
    "yokika4932@mobilesm.com": "GMH_COMMUNITY"
})


def main() -> None:
    while 1:
        try:
            b4as_accept(0)
            b4a_i384_list = b4as_recv(0)

            strings_list = [None] * len(b4a_i384_list)

            for i, b4a_i384 in enumerate(b4a_i384_list):
                b4a_i384_i_list = b4a_i384_get_list(b4a_i384, 13, 6, 60)
                
                try:
                    length = b4a_i384_i_list.index(0)
                    string = b4a_i384_get_string(b4a_i384, 11, length)
                except ValueError:
                    string = b4a_i384_get_string(b4a_i384, 11, 60)

                strings_list[i] = string

            print("".join(strings_list))

            text = "yes, xip is a cutie. dont ban mika pls"
            
            b4a_i384_list = [
                b4a_i384_set_string(0, 13, stI6, text)
            ]

            b4as_send(0, b4a_i384_list)
        except b4as_ClientDisconnection:
            ...


Thread(target=main).start(),
app.run()
