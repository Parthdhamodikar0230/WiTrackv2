"# WiTrackv2" 
WiTrackv2
WiTrackv2 is an open-source Wi-Fi based tracking system that leverages ESP microcontrollers (ESP8266/ESP32) and Python to scan, collect, and visualize the presence and signal strength of nearby Wi-Fi devices. This project aims to provide a low-cost, real-time tracking solution for IoT and cybersecurity enthusiasts.

Features
Passive scanning of Wi-Fi networks and clients using ESP8266/ESP32

Collects BSSID, SSID, RSSI, MAC addresses, and timestamps

Transmits scan data via UDP to a Python dashboard server

Real-time web dashboard for visualization of device locations and signal strength

Configurable scanning intervals and filtering by SSID/BSSID

Extensible Python server for data storage and analysis

Prerequisites
Hardware:

ESP8266 or ESP32 development board

USB cable for programming

Software:

Arduino IDE (v1.8.x or later)

Python 3.7+ and pip

Required Arduino libraries:

ESP8266WiFi (for ESP8266)

WiFi (for ESP32)

WebSocketsServer

Python packages:

flask

flask-socketio

pandas

plotly

Installation
Clone the repository

bash
git clone https://github.com/Parthdhamodikar0230/WiTrackv2.git
cd WiTrackv2
Set up the Arduino code

Open WiTrack.ino in the Arduino IDE.

Install any missing libraries via Sketch → Include Library → Manage Libraries.

Update the Wi-Fi credentials (SSID, PASSWORD) and the UDP server IP/port in the sketch.

Select the correct board (ESP8266 or ESP32) and port, then upload.

Install Python dependencies

bash
pip install -r requirements.txt
Configure the Python server

Edit server.py to match the UDP port and dashboard parameters if needed.

(Optional) Adjust the dashboard refresh rate and database file path in server.py.

Run the Python server

bash
python server.py
Access the dashboard

Open a web browser and navigate to http://localhost:5000.

Usage
Power on the ESP device and ensure it connects to your Wi-Fi network.

The ESP will broadcast scan data via UDP to the Python server.

The dashboard visualizes detected devices on a live-updating plot and table.

Use the dashboard controls to filter by SSID, adjust time windows, and export CSV data.

Troubleshooting
ESP not connecting to Wi-Fi: Verify SSID/password and signal strength.

Server not receiving data: Ensure UDP port matches between ESP sketch and server.py.

Dashboard not loading: Check Flask server logs for errors and confirm port 5000 is open.

Contributing
Contributions are welcome! Feel free to:

Report issues or feature requests on GitHub

Fork the repository and submit pull requests

Improve documentation, add tests, and enhance functionality

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Inspired by various Wi-Fi tracking projects and IoT dashboards

Thanks to the Arduino and ESP communities for open-source libraries and support


