import socket
import json
import time
from threading import Thread
import signal


class EthernetPC:
    def __init__(self, host, port):
        self.run_flag = True
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        self.listener_thr = Thread(name='listener', target=self.listener, args=(), daemon=True)
        self.listener_thr.start()

        self.sender_thr = Thread(name='sender', target=self.sender, args=(), daemon=True)
        self.sender_thr.start()

    def stop(self):
        self.run_flag = False
        self.sock.close()
        self.listener_thr.join(timeout=5)
        self.sender_thr.join(timeout=5)

    def start(self):
        def signalHandler(signum, frame):
            print("Stopping driver pc")
            self.stop()
            exit(0)
        signal.signal(signal.SIGINT, signalHandler)
        while self.run_flag:
            time.sleep(0.1)

    def connect(self):
        self.sock.connect((self.host, self.port))

    def listener(self):
        while self.run_flag:
            try:
                response = self.sock.recv(1024)
                if response:
                    data = json.loads(response.decode())
                    print('received data pc', data)
            except Exception as e:
                print(f"Got following error in listener pc: {e}")

            time.sleep(0.1)

    def sender(self):
        while self.run_flag:
            data_to_send = {'data1': 'msg1',
                            'data2': 'msg2'}
            self.send_data(data_to_send)
            print(f'sent data pc: {data_to_send}')
            time.sleep(5)

    def send_data(self, data):
        message = json.dumps(data)
        self.sock.sendall(message.encode())


if __name__ == "__main__":
    ethernet_pc = EthernetPC(host='127.0.0.1', port=12345)
    ethernet_pc.start()
