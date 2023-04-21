import os
import threading
import paramiko
import base64
import serial
from flask import Flask, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "password",  # Replace with your desired username and password for Basic Auth
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


class USBHIDKeyboard:

    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)
        self.ser.flush()

    def send_keycode(self, keycode):
        try:
            self.ser.write(bytes(keycode, 'utf-8'))
        except Exception as e:
            print(f"Error sending keycode: {e}")


class CustomSSHServer(paramiko.ServerInterface):

    def __init__(self, usb_hid_keyboard):
        self.usb_hid_keyboard = usb_hid_keyboard
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        if username == "sshuser" and password == "sshpassword":  # Replace with your desired SSH username and password
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command):
        self.usb_hid_keyboard.send_keycode(command.decode("utf-8"))
        self.event.set()
        return True


def start_ssh_server(host, port, usb_hid_keyboard):
    ssh_host_key = paramiko.RSAKey.generate(2048)
    ssh_server = paramiko.Transport((host, port))
    ssh_server.add_server_key(ssh_host_key)

    while True:
        ssh_server.start_server(server=CustomSSHServer(usb_hid_keyboard))
        channel = ssh_server.accept()
        ssh_server.stop()


@app.route("/upload", methods=["GET", "POST"])
@auth.login_required
def upload():
    if request.method == "POST":
        text_file = request.files["textfile"]
        content = text_file.read().decode("utf-8")
        usb_hid_keyboard.send_keycode(content)
        return redirect(url_for("upload"))
    return render_template("upload.html")


def main():
    host = '0.0.0.0'
    port = 2222
    app_host = '0.0.0.0'
    app_port = 5000

    usb_hid_keyboard = USBHIDKeyboard()

    ssh_server_thread = threading.Thread(target=start_ssh_server, args=(host, port, usb_hid_keyboard))
    ssh_server_thread.daemon = True
    ssh_server_thread.start()

    ssl_context = (os.path.join(os.path.dirname(__file__), 'cert.pem'),
                   os.path.join(os.path.dirname(__file__), 'key.pem'))
    app.run(host=app_host, port=app_port, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
