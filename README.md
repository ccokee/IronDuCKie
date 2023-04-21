# USB HID SSH Server

This project was developed by Sons Of Code, a group of hackers from León, Spain. The USB HID SSH Server application allows users to control a USB HID keyboard remotely through an SSH connection or via a web interface. The main purpose of this project is to provide a simple and efficient way to send keystrokes from remote devices to a USB HID keyboard connected to a Raspberry Pi.

## Features

- SSH server for remote control of a USB HID keyboard
- Web interface with HTTP Basic Authentication for uploading text files containing keycodes
- Customizable MOTD for the SSH server

## Requirements

To run this application, you'll need the following dependencies:

- Python 3.6 or higher
- `hid` (0.10.1)
- `paramiko` (2.7.2)
- `Flask` (2.1.1)
- `pyudev` (0.22.0)

## Installation

1. Clone the repository or download the source code.

```bash
git clone https://github.com/ccokee/IronDuCKie.git
```

2. Change to the project directory.

```bash
cd usb-hid-ssh-server
```

3. Install the required dependencies.

```bash
pip3 install -r requirements.txt
```

4. Edit the `usb_hid_ssh_server.py` file and replace the `app.config['BASIC_AUTH_USERNAME']` and `app.config['BASIC_AUTH_PASSWORD']` with your desired credentials.

## IMPORTANT: Configuring Vendor ID and Product ID

Before using the USB HID SSH Server application, it is essential to properly configure the Vendor ID (`vendor_id`) and Product ID (`product_id`) of your USB HID device. This information is required to establish a connection with the device and ensure the application works as expected.

To find the Vendor ID and Product ID of your USB HID device, follow these steps:

### On Linux

1. Connect the USB HID device to your computer.
2. Open a terminal window and run the following command:

```bash
lsusb
```

This command lists all connected USB devices and their information, including the Vendor ID and Product ID.

Example output:

```
Bus 001 Device 002: ID 1a2b:1a2b USB Keyboard Manufacturer
```

In this example, the Vendor ID is `1a2b`, and the Product ID is `1a2b`.

### On Windows

1. Connect the USB HID device to your computer.
2. Open Device Manager by right-clicking on the Start button and selecting Device Manager.
3. Expand the "Human Interface Devices" category.
4. Locate your USB HID device, right-click on it, and select Properties.
5. Navigate to the Details tab.
6. Select "Hardware Ids" from the Property drop-down menu.

You should see a list of Hardware Ids for the connected device. The Vendor ID and Product ID are displayed after "VID_" and "PID_" respectively.

Example:

```
HID\VID_1A2B&PID_1A2B
```

In this example, the Vendor ID is `1A2B`, and the Product ID is `1A2B`.

### Update the Application

Once you have obtained the Vendor ID and Product ID, update the `usb_hid_ssh_server.py` file with the appropriate values:

```python
self.vendor_id = 0x1a2b  # Replace with your device's Vendor ID
self.product_id = 0x1a2b  # Replace with your device's Product ID
```

After updating the values, save the file and run the application. The USB HID SSH Server should now connect to your device and function correctly.

5. Run the application.

```bash
python3 usb_hid_ssh_server.py
```

## Usage


### SSH Connection

To connect to the SSH server and send keycodes, use the following command:

```bash
ssh <username>@<raspberry_pi_ip> -p 2222
```

Replace `<username>` with the username set in `app.config['BASIC_AUTH_USERNAME']` and `<raspberry_pi_ip>` with the IP address of your Raspberry Pi. After connecting, you can send keycodes as plain text through the SSH connection.

### Web Interface

To access the web interface, open a web browser and navigate to:

```
http://<raspberry_pi_ip>:5000/upload
```

Replace `<raspberry_pi_ip>` with the IP address of your Raspberry Pi. Log in with the credentials set in `app.config['BASIC_AUTH_USERNAME']` and `app.config['BASIC_AUTH_PASSWORD']`. You can then upload a text file containing keycodes, and the application will send the keycodes to the USB HID keyboard.

## License

This project is open-source and is released under the [MIT License](LICENSE).

## Acknowledgments

A big thanks to the Sons Of Code team for their dedication and hard work on this project. Their commitment to creating innovative and secure solutions has made this application possible.