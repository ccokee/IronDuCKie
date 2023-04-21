# IronDuCKie

IronDuCKie is a project that allows you to control a USB HID keyboard device connected to a Raspberry Pi. The Raspberry Pi communicates with a microcontroller (e.g., Arduino Pro Micro or Teensy) acting as a USB HID keyboard device, using the UART protocol. You can send keycodes to the microcontroller either via SSH commands or by uploading a text file through the web interface.

This project is brought to you by Jorge Curbera & Sons Of Code, a group of hackers from León, Spain.

## Prerequisites

- Raspberry Pi
- Microcontroller (e.g., Arduino Pro Micro or Teensy)
- USB cable to connect the microcontroller to the target computer

## Installation

1. Clone this repository on your Raspberry Pi:

```bash
git clone https://github.com/ccokee/ironduckie.git
cd ironduckie
```

2. Install the required Python dependencies:

```bash
pip3 install -r requirements.txt
```

3. Upload the Arduino code provided in this repository to your microcontroller using the Arduino IDE or an alternative method.

4. Connect the microcontroller to the Raspberry Pi using the UART protocol. For example, with an Arduino Pro Micro:

   - Connect the Arduino Pro Micro's TX pin to the Raspberry Pi's RX pin (GPIO 15, UART0_RXD)
   - Connect the Arduino Pro Micro's RX pin to the Raspberry Pi's TX pin (GPIO 14, UART0_TXD)
   - Connect the GND pins of both devices together

5. Update the `users` dictionary in `usb_hid_ssh_server.py` with your desired username and password for Basic Auth.

6. Update the SSH username and password in the `check_auth_password` method in the `CustomSSHServer` class in `usb_hid_ssh_server.py`.

## Generating a Custom Signed Certificate for HTTPS

To enable HTTPS for the web interface using a custom signed certificate, you'll need to generate a certificate and private key. Follow these steps to create a self-signed certificate:

1. Install OpenSSL if you haven't already. You can download it from [https://www.openssl.org/source/](https://www.openssl.org/source/) or use your operating system's package manager to install it.

2. Open a terminal window and navigate to the project directory (`ironduckie`).

3. Run the following command to generate a 4096-bit RSA private key and a self-signed certificate that are valid for 365 days:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

You'll be prompted to enter some information for the certificate, such as country, state, and organization.

4. The generated `key.pem` (private key) and `cert.pem` (certificate) files should be placed in the same directory as the `usb_hid_ssh_server.py` file. If you wish to store them in a different location, make sure to update the file paths in the `ssl_context` variable in the `main` function of `usb_hid_ssh_server.py`.

Please note that since this is a self-signed certificate, most web browsers will display a warning indicating that the connection is not secure. To resolve this issue, consider obtaining a certificate from a trusted certificate authority (CA), or add an exception in your web browser for the self-signed certificate.

## Usage

1. Start the IronDuCKie server by running the following command:

```bash
python3 usb_hid_ssh_server.py
```

2. To send keycodes via SSH, connect to the SSH server using the following command (replace `your_username` and `your_password` with the SSH username and password you set earlier):

```bash
ssh your_username@your_raspberry_pi_ip -p 2222
```

When prompted, enter your SSH password. Once connected, you can send keycodes by typing them in the SSH session. The keycodes will be sent to the microcontroller, which will then send the corresponding keystrokes to the connected computer.

3. To send keycodes via the web interface, open your web browser and navigate to `https://your_raspberry_pi_ip:5000/upload`. You may receive a warning due to the self-signed certificate. If so, either add an exception in your web browser or use a certificate from a trusted certificate authority (CA).

When prompted, enter the username and password you set for Basic Auth. Once logged in, you can upload a text file containing the keycodes you want to send. The keycodes will be sent to the microcontroller, which will then send the corresponding keystrokes to the connected computer.

## IMPORTANT: Microcontroller Vendor ID and Device ID

To ensure that the microcontroller is recognized as a keyboard by the connected computer, make sure that it is programmed with the appropriate USB Vendor ID (VID) and Product ID (PID). For example, the Arduino Pro Micro and Teensy boards use the following IDs:

- Arduino Pro Micro: VID 0x2341, PID 0x8036 (Arduino Leonardo)
- Teensy: VID 0x16C0, PID 0x0486 (Teensyduino)

These IDs are used by default when programming the microcontroller using the Arduino IDE and the provided Arduino code. If you're using a different microcontroller or a custom USB HID keyboard library, you may need to set the VID and PID manually to ensure that the microcontroller is recognized as a keyboard by the connected computer.

## License

This project is licensed under the MIT License.