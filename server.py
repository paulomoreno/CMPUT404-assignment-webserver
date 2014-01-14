# coding: utf-8

# Copyright 2014 Paulo H. O. Moreno, Marcus V. A. da Silva
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

import SocketServer
import os
import re

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #Extract the headers parameters
        req = re.findall('[^ ]+',self.data)

        if (req[0] == 'GET') or (req[0] == 'POST'):
            self.http_response(req[1])
        else:
            response_html = "<html><body><font size=\"14\"><b>Error 501: Method not implemented</b></font></body></html>"
            self.send_response("501 Not Implemented",response_html,"text/html")

    def http_response(self, filename):
        '''
        Defines which will be the correct http response.
        '''
        
        #If The URL requested is not trying to access a different folder than www/
        if '/../' in filename:
            response_html = "<html><body><font size=\"14\"><b>Error 404: File not found</b></font></body></html>"
            self.send_response("404 Not Found",response_html,"text/html")
        else:

            #If the request didnt specify any files, use index.html as default
            if filename[-1] == '/':
                filename += 'index.html'   

             #If the file exists
            if os.path.isfile(os.getcwd()+"/www/" + filename):
                f = file(os.getcwd()+"/www/" + filename,"r")

                #Checks if the request is about a css or html file
                if filename[-3:].lower() == 'css':
                    content_type = 'text/css'
                #else if filename[-4:].lower() == 'html':
                #    content_type = 'text/html'
                else:
                    content_type = 'text/html'

                self.send_response("200 OK",f.read(),content_type)
            else:
                response_html = "<html><body><font size=\"14\"><b>Error 404: File not found</b></font></body></html>"
                self.send_response("404 Not Found",response_html,"text/html")

    def send_response(self, response_code, content, content_type):
        '''
        Sends an HTTP response according to the parameters.
        '''
        header  = "HTTP/1.1 " + response_code + "\r\n" 
        header += "Server: Paulo's Awesome Web Server\r\n" 
        header += "Content-Length: " + str(len(content)) + "\r\n" 
        header += "Connection: close\r\n" 
        header += "Content-Type: " + content_type + "\r\n\r\n"
        #print(header)
        self.request.sendall(header)
        self.request.sendall(content)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
