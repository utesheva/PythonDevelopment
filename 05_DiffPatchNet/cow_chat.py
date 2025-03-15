import asyncio

class Client:
    def __init__(self):
        self.cow = None
        self.queue = asyncio.Queue() 

clients = {}

async def chat(reader, writer):
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
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
            elif q is send:
                writer.write("Login first\n".encode())
                await writer.drain()
                send = asyncio.create_task(reader.readline())
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
