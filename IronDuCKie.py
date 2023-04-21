import hid
import paramiko
import socket
import threading
import time
from flask import Flask, request, render_template, Response, abort
from werkzeug.security import generate_password_hash, check_password_hash
import os

class USBHIDKeyboard:
    def __init__(self):
        self.vendor_id = 0x1a2b  # Reemplaza con el ID del fabricante de tu dispositivo USB
        self.product_id = 0x1a2b  # Reemplaza con el ID del producto de tu dispositivo USB
        self.interface_number = 0
        self.usage_page = 0x1
        self.usage = 0x6
        self.device = None

        self._connect()

    def _connect(self):
        for device in hid.enumerate():
            if (device['vendor_id'] == self.vendor_id and
                    device['product_id'] == self.product_id and
                    device['interface_number'] == self.interface_number and
                    device['usage_page'] == self.usage_page and
                    device['usage'] == self.usage):
                self.device = hid.device()
                self.device.open(device['vendor_id'], device['product_id'])

    def send_key(self, key):
        if self.device is None:
            print("Dispositivo no encontrado")
            return

        self.device.write([0x00, key])
        self.device.write([0x00, 0x00])


class SSHServer(paramiko.ServerInterface):
    def __init__(self, usb_hid_keyboard):
        self.usb_hid_keyboard = usb_hid_keyboard

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        motd = '''
Welcome to:
.___                     ________         _________  ____  __.__        
|   |______  ____   ____ \______ \  __ __ \_   ___ \|    |/ _|__| ____  
|   \_  __ \/  _ \ /    \ |    |  \|  |  \/    \  \/|      < |  |/ __ \ 
|   ||  | \(  <_> )   |  \|    `   \  |  /\     \___|    |  \|  \  ___/ 
|___||__|   \____/|___|  /_______  /____/  \______  /____|__ \__|\___  >
                       \/        \/               \/        \/       \/  
                                                        by Sons of Code
        '''
        channel.send(motd)
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def start_ssh_server(host, port, usb_hid_keyboard):
    server_key = paramiko.RSAKey.generate(1024)
    ssh_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssh_server.bind((host, port))
    ssh_server.listen(5)

    while True:
        client_socket, addr = ssh_server.accept()
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(server_key)
        server_interface = SSHServer(usb_hid_keyboard)
        transport.start_server(server=server_interface)

        channel = transport.accept()
        while True:
            try:
                key_code = channel.recv(256)
                if not key_code:
                    break
                usb_hid_keyboard.send_key(int(key_code))
            except Exception as e:
                print(f"Error sending key: {e}")
                break

        channel.close()
        transport.close()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
app.config['BASIC_AUTH_USERNAME'] = 'iron'
app.config['BASIC_AUTH_PASSWORD'] = generate_password_hash('duckie')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        if (username == app.config['BASIC_AUTH_USERNAME'] and
                check_password_hash(app.config['BASIC_AUTH_PASSWORD'], password)):
            if request.method == 'POST':
                file = request.files['file']
                if file and file.filename.endswith('.txt'):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.txt'))
                    return 'Archivo subido con éxito.', 200
                else:
                    return 'Only .txt files.', 400
            else:
                return render_template('upload.html')
        else:
            abort(401)
    else:
        return Response('Por favor, inicia sesión.', 401, {'WWW-Authenticate': 'Basic realm="Access restricted"'})

def main():
    host = '0.0.0.0'
    port = 2222
    app_host = '0.0.0.0'
    app_port = 5000

    usb_hid_keyboard = USBHIDKeyboard()

    ssh_server_thread = threading.Thread(target=start_ssh_server, args=(host, port, usb_hid_keyboard))
    ssh_server_thread.daemon = True
    ssh_server_thread.start()

    app.run(host=app_host, port=app_port)

if __name__ == '__main__':
    main()
