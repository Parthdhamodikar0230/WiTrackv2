# 🚀 WiTrackv2 
### *Advanced Wi-Fi Device Tracking & Analysis System*

*Real-time Wi-Fi device tracking and signal analysis using ESP microcontrollers*

---

## 📋 **Table of Contents**
- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features) 
- [🛠️ Hardware Requirements](#️-hardware-requirements)
- [📦 Software Dependencies](#-software-dependencies)
- [🚀 Quick Start](#-quick-start)
- [📊 Dashboard Preview](#-dashboard-preview)
- [⚙️ Configuration](#️-configuration)
- [🔧 Troubleshooting](#-troubleshooting)

---

## 🎯 **Overview**

WiTrackv2 is a **cutting-edge IoT solution** that transforms ESP8266/ESP32 microcontrollers into powerful Wi-Fi monitoring stations. Perfect for **cybersecurity research**, **crowd analysis**, and **IoT prototyping**.

### 🏆 **Why WiTrackv2?**
- 📡 **Real-time monitoring** of nearby Wi-Fi devices
- 💰 **Cost-effective** hardware solution (< ₹500)
- 🌐 **Web-based dashboard** for live visualization
- 📈 **RSSI analysis** for distance estimation
- 🔒 **Passive scanning** - completely undetectable
- 📊 **Export capabilities** for further analysis

---

## ✨ **Key Features**

### 🔍 **Scanning Capabilities**
- ✅ Passive Wi-Fi network discovery
- ✅ Device MAC address collection
- ✅ Signal strength (RSSI) monitoring
- ✅ Timestamp logging
- ✅ BSSID/SSID filtering

### 📊 **Data Analysis**
- ✅ Real-time web dashboard
- ✅ Interactive data visualization
- ✅ CSV export functionality
- ✅ Distance estimation algorithms
- ✅ Device tracking over time

---

## 🛠️ **Hardware Requirements**

| Component | Specification | Price Range |
|-----------|---------------|-------------|
| **Microcontroller** | ESP8266 NodeMCU / ESP32 DevKit | ₹200-400 |
| **Power Supply** | USB Cable / 5V Adapter | ₹50-100 |
| **Optional: Antenna** | 2.4GHz External Antenna | ₹100-200 |

### 📋 **Recommended Setup**
```
ESP8266 NodeMCU v3 (Recommended for beginners)
• Built-in USB-to-Serial converter
• Onboard voltage regulator
• 4MB Flash memory
• Wi-Fi 802.11 b/g/n support
```

---

## 📦 **Software Dependencies**

### 🔧 **Arduino Environment**
```bash
# Required Libraries (Install via Library Manager)
ESP8266WiFi      # Wi-Fi functionality
WebSocketsServer # Real-time communication
ArduinoJson      # Data serialization
ESP8266WebServer # Web server capabilities
```

### 🐍 **Python Environment**
```bash
# Install dependencies
pip install flask flask-socketio pandas plotly dash
```

---

## 🚀 **Quick Start**

### **Step 1: Hardware Setup**
1. Connect ESP8266/ESP32 to your computer via USB
2. Ensure drivers are installed for your board

### **Step 2: Arduino Code**
```cpp
// 1. Open Arduino IDE
// 2. Load WiTrack.ino
// 3. Update these variables:
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* udpAddress = "192.168.1.100"; // Your computer's IP
```

### **Step 3: Python Server**
```bash
# Clone repository
git clone https://github.com/Parthdhamodikar0230/WiTrackv2.git
cd WiTrackv2

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

### **Step 4: Access Dashboard**
🌐 **Open browser:** `http://localhost:5000`

---

## 📊 **Dashboard Preview**

The WiTrackv2 dashboard provides:

🔴 **Live Device Map** - Real-time device positions based on signal strength  
📈 **RSSI Graphs** - Signal strength trends over time  
📋 **Device Table** - Comprehensive device information  
⚙️ **Control Panel** - Scanning parameters and filters  
📥 **Export Tools** - CSV download for analysis  

---

## ⚙️ **Configuration**

### **ESP8266 Settings**
```cpp
// Scanning Configuration
#define SCAN_INTERVAL 5000    // 5 second intervals
#define MAX_NETWORKS 20       // Maximum networks per scan
#define UDP_PORT 4210         // Communication port
```

### **Python Server Settings**
```python
# server.py Configuration
HOST = '0.0.0.0'              # Listen on all interfaces
PORT = 5000                   # Web dashboard port
UDP_PORT = 4210               # ESP communication port
DATA_FILE = 'scan_data.csv'   # Data storage file
```

---

## 🔧 **Troubleshooting**

### ❌ **Common Issues & Solutions**

| Problem | Solution |
|---------|----------|
| ESP won't connect to Wi-Fi | ✅ Check credentials and signal strength |
| No data on dashboard | ✅ Verify UDP port matches (4210) |
| Dashboard won't load | ✅ Check Flask server logs and port 5000 |
| Compilation errors | ✅ Install missing libraries via Library Manager |

### 🔍 **Debug Mode**
Enable debug output in Arduino IDE:
```cpp
#define DEBUG 1  // Add to top of sketch for debug info
```

---


### 🌟 **Star this repository if it helped you!**

**Built with ❤️ for the IoT and Cybersecurity Community**

