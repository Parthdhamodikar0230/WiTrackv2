\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=1in}
\title{WiTrackv2: Wi-Fi Based Tracking System}
\author{Parthdhamodikar0230}
\date{September 2025}
\begin{document}
\maketitle

\section*{Abstract}
WiTrackv2 is an open-source, low-cost real-time tracking solution using ESP8266/ESP32 microcontrollers and Python. It scans nearby Wi-Fi devices, collects signal data, and visualizes results through a web dashboard.

\section*{Features}
\begin{itemize}
  \item Passive scanning of Wi-Fi networks and clients using ESP8266/ESP32
  \item Collection of BSSID, SSID, RSSI, MAC addresses, and timestamps
  \item UDP data transmission to a Python dashboard server
  \item Real-time visualization of device locations and signal strength
  \item Configurable scanning intervals and filtering by SSID/BSSID
  \item Extensible Python server for data storage and analysis
\end{itemize}

\section*{Prerequisites}
\subsection*{Hardware}
\begin{itemize}
  \item ESP8266 or ESP32 development board
  \item USB cable for programming
\end{itemize}
\subsection*{Software}
\begin{itemize}
  \item Arduino IDE (v1.8.x or later)
  \item Python 3.7+ and \texttt{pip}
  \item Arduino libraries:
    \begin{itemize}
      \item \texttt{ESP8266WiFi} (for ESP8266)
      \item \texttt{WiFi} (for ESP32)
      \item \texttt{WebSocketsServer}
    \end{itemize}
  \item Python packages:
    \begin{itemize}
      \item \texttt{flask}
      \item \texttt{flask-socketio}
      \item \texttt{pandas}
      \item \texttt{plotly}
    \end{itemize}
\end{itemize}

\section*{Installation}
\begin{enumerate}
  \item Clone the repository:
  \begin{verbatim}
    git clone https://github.com/Parthdhamodikar0230/WiTrackv2.git
    cd WiTrackv2
  \end{verbatim}
  \item Set up the Arduino code:
    \begin{itemize}
      \item Open \texttt{WiTrack.ino} in Arduino IDE
      \item Install missing libraries via Sketch $\rightarrow$ Include Library $\rightarrow$ Manage Libraries
      \item Update Wi-Fi credentials and UDP server IP/port in the sketch
      \item Select the correct board and port, then upload
    \end{itemize}
  \item Install Python dependencies:
  \begin{verbatim}
    pip install -r requirements.txt
  \end{verbatim}
  \item Configure the Python server:
    \begin{itemize}
      \item Edit \texttt{server.py} for UDP port and dashboard parameters
      \item (Optional) Adjust dashboard refresh rate and database path
    \end{itemize}
  \item Run the Python server:
  \begin{verbatim}
    python server.py
  \end{verbatim}
  \item Access the dashboard at \url{http://localhost:5000}
\end{enumerate}

\section*{Usage}
Ensure the ESP device is powered and connected to Wi-Fi. The device broadcasts scan data via UDP, and the dashboard visualizes detected devices on a live-updating plot and table.

\section*{Troubleshooting}
\begin{itemize}
  \item \textbf{ESP not connecting to Wi-Fi}: Verify SSID, password, and signal strength.
  \item \textbf{Server not receiving data}: Match UDP port between sketch and \texttt{server.py}.
  \item \textbf{Dashboard not loading}: Check Flask logs and ensure port 5000 is open.
\end{itemize}

\section*{Contributing}
Contributions are welcome! Fork the repository, submit issues or pull requests, improve documentation, tests, and functionality.

\section*{License}
This project is licensed under the MIT License. See the \texttt{LICENSE} file for details.

\end{document}
