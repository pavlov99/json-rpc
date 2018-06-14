""" Example of json-rpc usage with asyncio and raw tcp server.
"""

import asyncio
from jsonrpc import AsyncJSONRPCResponseManager,dispatcher


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


async def process_request(request_data, client_writer): 
    response = await AsyncJSONRPCResponseManager.handle(request_data, dispatcher)
    client_writer.write(response.json.encode())
    client_writer.write("\r\n".encode())

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))

async def handle_client(client_reader, client_writer):
    tasks = {}

    while True:
        data = await asyncio.wait_for(client_reader.readline(), timeout=60.0)
        if len(data)==0 or data is None:
            break
        asyncio.Task(process_request(data.decode(), client_writer))

    client_writer.close()


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL) #to make ctrl+c work on windows

    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=4000)
    loop.run_until_complete(f)
    loop.run_forever()
