import argparse
import json
import traceback
import websockets
from lia.api import Api
from lia.constants import load_constants


async def connect(bot):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="specify port", required=False)
    parser.add_argument("-i", "--id", help="unique identifier", required=False)
    args = parser.parse_args()

    if args.port is None:
        args.port = "8887"
    if args.id is None:
        args.id = ""

    async with websockets.connect("ws://localhost:" + args.port, extra_headers={'Id': args.id}) as websocket:
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)

                response = Api(data['uid'])
                try:
                    if data['type'] == 'GAME_SETUP':
                        load_constants(data["constants"])

                    elif data['type'] == 'GAME_STATE':
                        bot.update(data, response)

                    await websocket.send(json.dumps(response.__dict__))
                except Exception as e:
                    traceback.print_exc()

        except websockets.ConnectionClosed:
            print("Connection closed. Exiting...")
        except Exception:
            traceback.print_exc()
