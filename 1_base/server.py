"""
#!/usr/bin/env python3
Usage: ./server.py [<port>]
Browser: ip:port/index.html http://192.168.1.105:8085/index.html
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import mimetypes # text/html; text/css
import time

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

    def _set_fspath(self):
        if self.path == "/" or self.path == "/store/":
            self.path = "/index.html" # set index.html as file to read (get) and write (post)
        fspath = self.directory + self.path # <-- translate url path to filesystem path
        return fspath

    def _file_builder(self,sensordata):
        data = str(sensordata, 'utf-8')
        d = dict(param.split('=') for param in data.split('&'))
        file = "<!DOCTYPE html><html>"
        header = "<head><meta charset='utf-8' name='viewport' content='width=device-width, initial-scale=1'> <link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.7.2/css/all.css'> <link href='style.css' rel='stylesheet' type='text/css'/> <link rel='icon' href='favicon.ico' type='image/x-icon'> <title>Arduino - DHT22</title> </head>"
        body = "<body><div><h1>DHT22 sensor data</h1>"
        temperature = f"<p><i class='fas fa-thermometer-half' style='color:#059e8a;'></i> <span class='dht-labels'>Temperature: {d['temperature']}&deg;C</p>"
        humidity = f"<p><i class='fas fa-tint' style='color:#00add6;'></i> <span class='dht-labels'>Humidity: {d['humidity']}%</p>"
        hic_index = f"<p><i class='fas fa-sun' style='color:#ffbf00;'></i> <span class='dht-labels'>Heat index: {d['hic']}&deg;C</p>"
        time = f"<br><p>Time: {datetime.now()}</p>"
        footer = "</div></body></html>"
        output = file + header + body + temperature + humidity + hic_index + time + footer
        with open(self._set_fspath(), 'w') as f:
            f.write(output)

    def do_GET(self):
        # logging.info(f"{bcolors.OKBLUE}GET request{bcolors.ENDCOL} \nPath: {str(self.path)}\nHeaders: {str(self.headers)}")
        logging.info(f"{bcolors.OKBLUE}GET request{bcolors.ENDCOL} - Path: {str(self.path)}")
        self._set_headers()
        with open(self._set_fspath(), 'rb') as f:
            cont = f.read()
        self.wfile.write(cont) # output stream for writing a response back to the client

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # server log
        # logging.info(f"{bcolors.OKGREEN}POST request{bcolors.ENDCOL} \nPath:{str(self.path)} \nHeaders: {str(self.headers)} \nBody: {post_data.decode('utf-8')}")
        logging.info(f"{bcolors.OKGREEN}POST request{bcolors.ENDCOL} - Body: {post_data.decode('utf-8')}")
        self._set_headers()
        # response to Arduino
        self.wfile.write("POST data: {}".format(post_data).encode('utf-8')) # client.responseBody();
        # write sensor data to html file >> use file as a storage for get requests (do_GET)
        self._file_builder(post_data)


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
