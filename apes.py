from threading import Thread
from b4as import app, b4as_create_ports, b4as_accept, b4as_recv, b4as_send, b4as_ClientDisconnection, rtSEND_DATA
from b4a_i384 import b4a_i384_get, b4a_i384_set

b4as_create_ports({
    "yokika4932@mobilesm.com": "GMH_COMMUNITY"
})

print(f"server started!")


def main() -> None:
    while 1:
        try:
            client_id = b4as_accept(0)

            print(f"[PORT {0}] start recv from client_id={client_id}")

            b4a_i384_list = b4as_recv(0)

            print(f"[PORT {0}] received {len(b4a_i384_list)} b4a_i384 blocks from client_id={client_id}")

            for i in range(8):
                print(str(i + 1), b4a_i384_get(b4a_i384_list[i], 11, 32))

            b4a_i384_send_list = [0] * 8
            
            for i in range(8):
                value = b4a_i384_get(b4a_i384_list[i], 11, 32)
                
                b4a_i384 = b4a_i384_set(0, 2, 3, rtSEND_DATA) 
                b4a_i384 = b4a_i384_set(b4a_i384, 5, 8, client_id) 
                b4a_i384 = b4a_i384_set(b4a_i384, 13, 32, value + 1) 
                b4a_i384_send_list[i] = b4a_i384

            b4as_send(0, b4a_i384_send_list)

            print(f"[PORT {0}] sent {len(b4a_i384_list)} b4a_i384 blocks to client_id={client_id}")
        except b4as_ClientDisconnection:
            print(f"[PORT {0}] client disconnection client_id={client_id}")


Thread(target=main).start(),
app.run()
