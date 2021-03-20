from websocket import WebSocketApp
from threading import Thread
import json
import time, datetime
import redis

start = 0
end = 0
# request='[{"ticket":"dantanamoo"},{"type":"ticker","codes":["KRW-BTC"]},{"format":"SIMPLE"}]'

try:
    conn = redis.StrictRedis(
        host='13.209.69.195',
        port=6379,
        db=0)
    # print("hmset", conn.set("curCoin", "hihhihihi"))
    # print("hgetall", conn.get("curCoin"))
    # print("hgetall", conn.delete("bitData"))
    # print("hgetall", conn.hgetall("bitData"))
except Exception as ex:
    print('Redis Error:', ex)


def on_message(ws, msg):
    msg = json.loads(msg.decode('utf-8'))
    result = dict()
    now = datetime.datetime.now()
    result['time'] = str(now)

    result = json.dumps(result)
    print(type(result))
    time.sleep(1)
    # conn.set("curCoin", result)
    print(msg)

def on_error(ws, msg):
    print(msg)

def on_close(ws):
    print("close")
    end = time.time()
    print('running time : ', (end - start))
    # print ("Reconnect...")
    # time.sleep(10)
    # connect_websocket() # retry per 10 seconds

def on_open(ws):
    def run(*args):
        # request1 = '[{"ticket":"dantanamoo"},{"type":"ticker","codes":["KRW-BTC"]},{"format":"SIMPLE"}]'
        request2 = '[{"ticket": "dantanamoo"}, {"type": "orderbook", "codes": ["KRW-MED.5"]}]'

        # ws.send(request1)
        ws.send(request2)
        ## time.sleep(5)
        ## ws.close()

    th = Thread(target=run, daemon=True)
    th.start()
    print('connection established')

def connect_websocket():
    ws = WebSocketApp("wss://api.upbit.com/websocket/v1",
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close,
                      on_open=on_open)
    start = time.time()
    ws.run_forever()

if __name__ == "__main__":
    try:
        connect_websocket()
    except Exception as err:
        print(err)
        print("connect failed")

#
# if __name__ == "__main__":
#     ws = WebSocketApp("wss://api.upbit.com/websocket/v1",
#                       on_message=on_message,
#                       on_error=on_error,
#                       on_close=on_close,
#                       on_open=on_open)
#     start = time.time()
#     ws.run_forever()