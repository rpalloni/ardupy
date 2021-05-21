"""
#!/usr/bin/env python3
Usage: ./server.py [<port>]
Browser: ip:port/index.html http://192.168.1.105:8085/index.html
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import os
import sys
import mimetypes # text/html; text/css

import datetime
from dbms import fetch_data, store_data

# ASCII color codes
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDCOL = '\033[0m'

class ArduinoWebServer(BaseHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        mimeType = mimetypes.guess_type(self.path)
        self.send_header('Content-type', mimeType)
        self.end_headers()

    def do_GET(self):
        # server log
        # logging.info(f"{bcolors.OKBLUE}GET request{bcolors.ENDCOL} \nPath: {str(self.path)}\nHeaders: {str(self.headers)}")
        logging.info(f"{bcolors.OKBLUE}GET request{bcolors.ENDCOL} - Path: {str(self.path)}")
        self._set_headers()
        if self.path == "/":
            self.path = "/index.html"
        fspath = self.directory + self.path # <-- translate url path to filesystem path
        if "/getdata.py" in fspath:
            content = fetch_data()
            response = bytes(content, 'utf-8')
            self.wfile.write(response)
        else:
            with open(fspath, 'rb') as f:
                cont = f.read()
            self.wfile.write(cont)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # server log
        # logging.info(f"{bcolors.OKGREEN}POST request{bcolors.ENDCOL} \nPath:{str(self.path)} \nHeaders: {str(self.headers)} \nBody: {post_data.decode('utf-8')}")
        logging.info(f"{bcolors.OKGREEN}POST request{bcolors.ENDCOL} - Body: {post_data.decode('utf-8')}")
        # response to Arduino
        self._set_headers()
        self.wfile.write("POST data: {}".format(post_data).encode('utf-8')) # client.responseBody();
        # write sensor data to file >> use file as a storage for get requests (do_GET)
        data = str(post_data, 'utf-8')
        store_data(data)


def run(server_class=HTTPServer, handler_class=ArduinoWebServer, port=8080):
    logging.basicConfig(level=logging.INFO)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'{bcolors.OKGREEN}Starting HTTP SERVER at PORT ' + str(port) + f'{bcolors.ENDCOL}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    logging.info(f'port '+str(port-1)+' is taken. Trying port ' + str(port))
    httpd.server_close()
    logging.info(f'{bcolors.OKGREEN}Stopping httpd...\n'+ f'{bcolors.ENDCOL}')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
