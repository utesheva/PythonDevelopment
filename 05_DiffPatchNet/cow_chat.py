import asyncio
import cowsay

class Client:
    def __init__(self):
        self.cow = None
        self.queue = asyncio.Queue() 

clients = {}

def who(clients):
    return [clients[i].cow for i in clients if clients[i].cow is not None]

def cows(clients):
    used = who(clients)
    return [i for i in cowsay.list_cows() if i not in used]

def login(clients, me, cow):
    if cow in cows(clients):
        clients[me].cow = cow
        return clients, 'Successful login'
    return clients, 'This cow cannot be used. Call cows to see free names.'

async def print_list(l, exception, writer):
    if l != []:
        writer.write(f"{'\n'.join(l)}\n".encode())
        await writer.drain()
    else:
        writer.write(f"{exception}\n".encode())
        await writer.drain()

async def chat(reader, writer):
    global clients
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = Client()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:  
            if q is send and clients[me].cow is not None:
                send = asyncio.create_task(reader.readline())
                for out in clients.values():
                    if out.queue is not clients[me].queue:
                        await out.queue.put(f"{me} {q.result().decode().strip()}")
            elif q is receive and clients[me].cow is not None:
                receive = asyncio.create_task(clients[me].queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
            elif q is send:
                send = asyncio.create_task(reader.readline())
                match q.result().decode().split():
                    case ['who']:
                        await print_list(who(clients), "No users yet", writer)
                    case ['cows']:
                        await print_list(cows(clients), "No free names", writer)
                    case ['login', name]:
                        clients, ans = login(clients, me, name)
                        writer.write(f"{ans}\n".encode())
                        await writer.drain()
                    case _:
                        writer.write("Login first\n".encode())
                        await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
