# import websocket
# import json
# try:
#     import thread
# except ImportError:
#     import _thread as thread
# import time, datetime
#
# result = dict()
# now = datetime.datetime.now()
#
# def on_message(ws, message):
#     get_message = json.loads(message.decode('utf-8'))
#
#     result['time'] = get_message['trade_time']
#     result['cur_price'] = get_message['trade_price']
#     result['acc_volume'] = get_message['acc_trade_volume']
#     print(result)
#
# def on_error(ws, error):
#     print(error)
#
# def on_close(ws):
#     print("close")
#
# def on_open(ws):
#     def run(*args):
#         sendData = '[{"ticket":"dantanamoo"},{"type":"ticker","codes":["KRW-BTC"]}]'
#         ws.send(sendData)
#         time.sleep(1)
#
#         # ws.close()
#         # if ()
#     thread.start_new_thread(run, ())
#
#
# if __name__ == "__main__":
#
#     ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
#                            on_message = on_message,
#                            on_error = on_error,
#                            on_close = on_close)
#     ws.on_open = on_open
#     ws.run_forever()

from websocket import WebSocketApp
from threading import Thread
import json
import time, datetime
import redis

try:
    conn = redis.StrictRedis(
        host='13.209.69.195',
        port=6379,
        db=1)
    # print("hmset", conn.hmset("bitData", {"time": "2021-03-19 16:17:29.934356", "cur_price": 67998000.0, "acc_volume": 3302.92540809}))
    # print("hgetall", conn.hgetall("bitData"))
    # print("hgetall", conn.delete("bitData"))
    # print("hgetall", conn.hgetall("bitData"))
except Exception as ex:
    print('Redis Error:', ex)


class UpbitReal:
    def __init__(self, request, callback=print):
        self.request = request
        self.callback = callback
        self.ws = WebSocketApp(
            url="wss://api.upbit.com/websocket/v1",
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws:     self.on_close(ws),
            on_open=lambda ws:     self.on_open(ws))
        self.running = False

    def on_message(self, ws, msg):
        msg = json.loads(msg.decode('utf-8'))
        # result = dict()
        now = datetime.datetime.now()
        # result['time'] = msg['tdt'] + msg['ttm']    -> UTC
        # result['time'] = str(now)
        # result['cur_price'] = msg['tp']
        # result['acc_volume'] = msg['atv']
        # result = json.dumps(result)
        # print(type(result))
        conn.hmset("bitData", {"time": str(now), "curPrice": msg['tp'], "accVolume": msg['atv']})
        # self.callback(msg)

    def on_error(self, ws, msg):
        self.callback(msg)

    def on_close(self, ws):
        self.callback("closed")
        self.running = False

    def on_open(self, ws):
        th = Thread(target=self.activate, daemon=True)
        th.start()

    def activate(self):
        self.ws.send(self.request)
        while self.running:
            time.sleep(1)
        self.ws.close()

    def start(self):
        self.running = True
        self.ws.run_forever()


if __name__ == "__main__":
    request='[{"ticket":"dantanamoo"},{"type":"ticker","codes":["KRW-BTC"]},{"format":"SIMPLE"}]'
    real = UpbitReal(request=request)
    real.start()