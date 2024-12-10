import signal
import time
from threading import Thread

import RPi.GPIO as GPIO
import socket
import json


class EthernetRPB:
    def __init__(self, host, port):
        self.run_flag = True
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = None

        self.setup_gpio()

        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.listener_thr = Thread(target=self.listener, daemon=True)
        self.listener_thr.start()

        self.sender_thr = Thread(target=self.sender, daemon=True)
        self.sender_thr.start()


    @staticmethod
    def setup_gpio():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.OUT)  # TX1
        GPIO.setup(15, GPIO.OUT)  # TX-EN
        GPIO.setup(18, GPIO.IN)   # RX0
        GPIO.setup(24, GPIO.IN)   # nINT/RETCLK
        GPIO.setup(23, GPIO.OUT)  # TX0
        GPIO.setup(25, GPIO.IN)   # RX1
        GPIO.setup(8, GPIO.IN)    # CRS
        GPIO.setup(11, GPIO.OUT)  # MDC
        GPIO.setup(9, GPIO.IN)    # MD10

    def stop(self):
        self.run_flag = False
        if self.client_sock:
            self.client_sock.close()
        self.sock.close()
        GPIO.cleanup()
        self.listener_thr.join(timeout=5)
        self.sender_thr.join(timeout=5)

    def start(self):
        def signalHandler(signum, frame):
            print("Stopping driver rpb")
            self.stop()
            exit(0)
        signal.signal(signal.SIGINT, signalHandler)
        while True:
            time.sleep(0.1)

    def listener(self):
        while self.run_flag:
            if not self.client_sock:
                print("Waiting for client connection")
                self.client_sock, _ = self.sock.accept()
                print("Client connected.")
            try:
                response = self.client_sock.recv(1024)
                if response:
                    data = json.loads(response.decode())
                    print('received data rpb', data)
                else:
                    print("Client disconnected.")
                    self.client_sock.close()
                    self.client_sock = None
                    continue

            except Exception as e:
                print(f"Got following error in rpb listener: {e}")
                self.client_sock.close()
                self.client_sock = None
                continue

            time.sleep(0.1)

    def sender(self):
        while self.run_flag:
            if self.client_sock:
                data_to_send = {'data3': 'msg3',
                                'data4': 'msg4'}
                self.send_data(data_to_send)
                print(f"sent data rpb: {data_to_send}")
            time.sleep(5)

    def send_data(self, data):
        if self.client_sock:
            try:
                message = json.dumps(data)
                self.client_sock.sendall(message.encode())
            except Exception as e:
                print(f"Error in sending data rpb: {e}")


if __name__ == "__main__":
    ethernet_pc = EthernetRPB(host='0.0.0.0', port=12345)
    ethernet_pc.start()
