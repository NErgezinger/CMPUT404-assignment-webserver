#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data.decode('utf-8'))
        # self.request.sendall(bytearray("OK",'utf-8'))

        data_split = self.data.decode('utf-8').split()

        print("Split request: \n", self.data.decode('utf-8').split())

        if data_split[0] == 'GET':
            requested_path = data_split[1]
            if requested_path[-1] != '/' and '.' not in requested_path[-5:]:
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanantly\r\nLocation:http://127.0.0.1:8080"+ requested_path + "/\r\n\r\n", "utf-8"))
            else:
                if '.' not in requested_path[-5:]:
                    requested_path = 'www' + requested_path + 'index.html'
                else:
                    requested_path = 'www' + requested_path
                requested_dir = os.path.dirname(requested_path)
                if os.path.exists(requested_path) and requested_dir[:3] == "www":
                    with open(requested_path) as f:
                        requested_file = f.read()
                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + requested_file + "\r\n\r\n", "utf-8"))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))
        elif data_split[0] != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n", "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
