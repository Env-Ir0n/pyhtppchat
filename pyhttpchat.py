from http.server import HTTPServer, BaseHTTPRequestHandler
from submodules.authhandler import generate_key as genkey
import submodules.jsonhandler as json
import os
from submodules.encryptor import *

if os.path.exists('messages.json') == False:
    with open('messages.json'):
        pass
msg = json.retrieve('messages.json')
for keys in msg:
    del msg[keys]

json.commit('messages.json',msg)

class ReqestHandler(BaseHTTPRequestHandler):
    
    # called when a

    def do_GET(self):
        if self.path == '/init':
            info = json.retrieve('server.json')
            if info['auth']['open'] == False:
                if self.headers['Password'] == info['auth']['pass']:
                    pass
                else:
                    self.send_response(401)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    self.wfile.write('401: Incorrect/Missing password header'.encode())
                    return None
            key = genkey()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('Auth',key)
            self.end_headers()
            self.wfile.write(f'Your AUTH key is : {key}'.encode())

        if self.path == '':
            if self.headers['Encrypted?'] == 'False':
                info = json.retrieve('server.json')
                if json.isthere(self.headers['Auth'],info['auth']) == False:
                    self.send_response(401)
                    self.send_header('Content-type','text/html')
                    self.send_header('Auth','<authkey>')
                    self.end_headers()
                    self.wfile.write('401: No/Incorrect Auth header, check it or generate a new one at <serverip>/init'.encode())
                    return None
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()               
                servername = info['basic']['servername']
                open = info['auth']['open?']
                send = {"Servername":servername,"serverisopen":open}
                self.wfile.write(json.dumps(send))
            
        if self.path == '/messages':
            if self.headers['Encrypted?'] == 'False':
                self.send_response(401)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write('Message is not flagged as encrypted!'.encode())
                return None
            msg = json.retrieve('messages.json')
            info = json.retrieve('server.json')
            
            if json.isthere(self.headers['Auth'],info['auth']) == False:
                self.send_response(401)
                self.send_header('Content-type','text/html')
                self.send_header('Encrypted?','False')
                with open('public.asc') as f:
                    publickey = f.read()
                self.send_header('PGP:',publickey)
                self.send_header('Auth','<authkey>')
                self.end_headers()
                self.wfile.write('401: No/Incorrect Auth header, check it or generate a new one at <serverip>/init'.encode())
                return None
            
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Encrypted?','True')
            with open('public.asc') as f:
                publickey = f.read()
            self.send_header('PGP:',publickey)
            self.end_headers()
            if 'PGP' in self.headers:
                pass
            else:
                return None
            public = self.headers['PGP:']
            sendit = {}
            for keys in msg:
                newkey = encrypt(keys,public)
                content = msg[keys]['content']
                user = msg[keys]['user']
                time = msg[keys]['time']
                newcontent = encrypt(content,public)
                newuser = encrypt(user,public)
                newtime = encrypt(time,public)
                label1 = encrypt('content',public)
                label2 = encrypt('user',public)
                label3 = encrypt('time',public)
                sendit[newkey][label1] = newcontent
                sendit[newkey][label2] = newuser
                sendit[newkey][label3] = newtime
            self.wfile.write(json.dumps(sendit))
            
def run():
    addr = '',8000
    server = HTTPServer(addr,ReqestHandler)
    try:
        server.serve_forever()
        print(f'Serving on: {addr}')
    except KeyboardInterrupt():
        print('Adios')