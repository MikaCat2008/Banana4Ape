from requests import Session
from threading import Event
from collections import deque

from b4a_i384 import b4a_i384_get, b4a_i384_set, b4a_i384_decode, b4a_i384_encode

mtSTART_DATA_TRANSFER = 0
mtSEND_DATA = 1
mtSTOP_DATA_TRANSFER = 2
mtREADY_FOR_DATA_TRANSFER = 3
mtGOT_DATA = 4

rtSET_CLIENT_ID = 0
rtSTART_DATA_TRANSFER = 1
rtSEND_DATA = 2
rtSTOP_DATA_TRANSFER = 3

ports_session: dict[int, Session] = {}
ports_client_id: dict[int, int] = {}
ports_recv_event: dict[int, Event] = {}
ports_recv_status: dict[int, bool] = {}
ports_send_event: dict[int, Event] = {} 
ports_data_transfer_event: dict[int, Event] = {}
accept_event = Event()
accept_queue: deque[int] = deque()
clients_port_id: dict[int, int] = {}
clients_b4a_i384_list: dict[int, list[int]] = {}


class b4as_ClientDisconnection(BaseException):
    ...


def b4as_create_ports(ports: dict[str, str]) -> None:
    for i, (email, password) in enumerate(ports.items()):
        session = Session()
        session.get("https://apes.io/signin")
        session.post(
            "https://apes.io/api/user/signin",
            json={
                "email": email,
                "password": password
            }
        )

        ports_session[i] = session
        ports_recv_event[i] = Event()
        ports_recv_status[i] = False
        ports_send_event[i] = Event()
        ports_data_transfer_event[i] = Event()


def b4as_set_port_b4a_i384(port_id: int, b4a_i384: int) -> None:
    while 1:
        session = ports_session[port_id]
        response = session.post(
            "https://apes.io/api/user/rename",
            json={
                "username": b4a_i384_encode(b4a_i384)
            }
        )

        if response.content == b"{}":
            break
        else:
            i = b4a_i384_get(b4a_i384, 0, 2)
            b4a_i384 = b4a_i384_set(b4a_i384, 0, 2, (i + 1) % 4)


def b4as_accept(port_id: int) -> int:
    if len(accept_queue) == 0:
        accept_event.wait()
        accept_event.clear()

    client_hook = accept_queue.pop()

    for client_id in range(256):
        if client_id not in clients_b4a_i384_list:            
            break

    ports_client_id[port_id] = client_id
    clients_port_id[client_id] = port_id
    clients_b4a_i384_list[client_id] = []

    b4a_i384 = b4a_i384_set(0, 2, 3, rtSET_CLIENT_ID)
    b4a_i384 = b4a_i384_set(b4a_i384, 5, 32, client_hook)
    b4a_i384 = b4a_i384_set(b4a_i384, 37, 8, client_id)
    b4as_set_port_b4a_i384(port_id, b4a_i384)

    return client_id


def b4as_disconnect_client(client_id: int) -> None:
    del clients_port_id[client_id]


def b4as_wait_for_client_answer(event: Event, client_id: int) -> None:
    if event.wait(5):
        event.clear()
    else:
        b4as_disconnect_client(client_id)

        raise b4as_ClientDisconnection()


def b4as_recv(port_id: int) -> list[int]:
    client_id = ports_client_id[port_id]

    while not ports_recv_status[port_id]:
        b4as_wait_for_client_answer(ports_recv_event[port_id], client_id)

    ports_recv_status[port_id] = False

    b4a_i384_list = clients_b4a_i384_list[client_id]
    clients_b4a_i384_list[client_id] = []

    return b4a_i384_list


def b4as_send(port_id: int, b4a_i384_list: list[int]) -> None:
    client_id = ports_client_id[port_id]

    b4a_i384 = b4a_i384_set(0, 2, 3, rtSTART_DATA_TRANSFER)
    b4a_i384 = b4a_i384_set(b4a_i384, 5, 8, client_id)
    b4as_set_port_b4a_i384(port_id, b4a_i384)

    b4as_wait_for_client_answer(ports_data_transfer_event[port_id], client_id)

    for b4a_i384 in b4a_i384_list:
        b4as_set_port_b4a_i384(port_id, b4a_i384)

        print(f"[PORT {port_id}] sent b4a_i384 to client_id={client_id}")

        b4as_wait_for_client_answer(ports_send_event[port_id], client_id)

    b4a_i384 = b4a_i384_set(0, 2, 3, rtSTOP_DATA_TRANSFER)
    b4a_i384 = b4a_i384_set(b4a_i384, 5, 8, client_id)
    b4as_set_port_b4a_i384(port_id, b4a_i384)

    b4as_disconnect_client(client_id)


from pyrogram import Client
from pyrogram.types import Message

app = Client(
    "b4a_bot", 
    api_id=22697385, 
    api_hash="bde422be808ee23d61529420687efa36", 
    phone_number="+380939505096"
)


@app.on_message()
def message_handler(client: Client, message: Message) -> None:
    if message.chat.id != 7575372807:
        return

    message.delete()
    b4a_i384 = b4a_i384_decode(message.text)

    method_type = b4a_i384_get(b4a_i384, 0, 3)

    if method_type == mtSTART_DATA_TRANSFER:
        client_hook = b4a_i384_get(b4a_i384, 3, 32)

        accept_queue.append(client_hook)
        accept_event.set()
    else:
        client_id = b4a_i384_get(b4a_i384, 3, 8)
        port_id = clients_port_id[client_id]
        
        if method_type == mtSEND_DATA:
            clients_b4a_i384_list[client_id].append(b4a_i384)
            ports_recv_event[port_id].set()

            print(f"[PORT {port_id}] received b4a_i384 from client_id={client_id}")
        elif method_type == mtSTOP_DATA_TRANSFER:
            ports_recv_status[port_id] = True
            ports_recv_event[port_id].set()

            print(f"[PORT {port_id}] stop data transfer from client_id={client_id}")
        elif method_type == mtREADY_FOR_DATA_TRANSFER:
            ports_data_transfer_event[port_id].set()
            
            print(f"[PORT {port_id}] ready for data transfer client_id={client_id}")
        elif method_type == mtGOT_DATA:
            ports_send_event[port_id].set()

            print(f"[PORT {port_id}] got data client_id={client_id}")
