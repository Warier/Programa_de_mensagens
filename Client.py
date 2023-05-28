#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback

chave = ""
ack = 0

class Server(threading.Thread):

    def initialise(self, receive):
        self.receive = receive

    def run(self):
        global chave
        global ack
        lis = []
        lis.append(self.receive)
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        chunk = s
                        if ack == 0 or chave == "":
                            info = chunk.decode()
                            info = info.split(":")
                            if info[1] == "abcde":
                                chave = info[1]
                                print(info[0])
                                ack = int(info[0])
                                continue
                        else:
                            print(time.strftime("%X", time.gmtime()) + " | " + chunk.decode() + '\n>>')
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    @property
    def run(self):
        global chave
        global ack
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP \n>>")
            port = int(input("Enter the server Destination Port\n>>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        while 1:
            recebido = ack
            if (chave != ""):
                recebido = 1
            mandarChave = str(recebido) + ":abcde"
            self.client(host, port, mandarChave.encode())
            print("enviando chaves\n")

            if(ack == 1):
                self.client(host, port, mandarChave.encode())
                break
            time.sleep(2)

        time.sleep(5)
        print("Conversa\n")
        while 1:
            # print "Waiting for message\n"
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg
            data = msg.encode()
            self.client(host, port, data)
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()