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
        writer.write(f"0 {' '.join(l)}\n".encode())
        await writer.drain()
    else:
        writer.write(f"1 {exception}\n".encode())
        await writer.drain()

async def send_message(sender, receivers, text):
    for out in clients.values():
        if out.cow in receivers:
            await out.queue.put(f"2 {sender} {text}")

async def chat(reader, writer):
    global clients
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = Client()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    state = True
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:  
            if q is send:
                send = asyncio.create_task(reader.readline())
                match q.result().decode().split():
                    case ['who']:
                        await print_list(who(clients), "No users yet", writer)
                    case ['cows']:
                        await print_list(cows(clients), "No free names", writer)
                    case ['login', name]:
                        clients, ans = login(clients, me, name)
                        writer.write(f"1 {ans}\n".encode())
                        await writer.drain()
                    case (['say', *args] | ['yield', args]) if clients[me].cow is None:
                        writer.write("1 Login to send and receive messages.\n".encode())
                        await writer.drain()
                    case ['say', name, *args]:
                        await send_message(clients[me].cow, [name], ' '.join(args))
                    case ['yield', *args]:
                        await send_message(clients[me].cow, 
                                           [i.cow for i in clients.values() if i != clients[me]], 
                                           ' '.join(args))
                    case ['quit']:
                        state = False
                        break
                    case _:
                        writer.write("1 Invalid command.\n".encode())
                        await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                if clients[me].cow is not None: 
                    writer.write(f"{q.result()}\n".encode())
                    await writer.drain()
        if not state: break
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
