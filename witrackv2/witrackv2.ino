// enhanced_esp8266_client.ino
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

const char* ssid = "Your wifi";
const char* password = "wifi password";
const char* serverIP = "your IP address";
const int serverPort = 4210;

WiFiUDP Udp;
unsigned long lastScan = 0;
const unsigned long scanInterval = 2000; // Scan every 2 seconds

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  
  WiFi.mode(WIFI_STA);
}

void loop() {
  if (millis() - lastScan > scanInterval) {
    performScanAndSend();
    lastScan = millis();
  }
  delay(100);
}

void performScanAndSend() {
  Serial.println("Scanning WiFi networks...");
  
  int n = WiFi.scanNetworks(false, true);
  
  if (n == 0) {
    Serial.println("No networks found");
    return;
  }
  
  // Create JSON document
  DynamicJsonDocument doc(2048);
  JsonArray devices = doc.createNestedArray("devices");
  
  Serial.printf("Found %d networks:\n", n);
  
  for (int i = 0; i < n; i++) {
    JsonObject device = devices.createNestedObject();
    
    String bssid = WiFi.BSSIDstr(i);
    int rssi = WiFi.RSSI(i);
    String ssid_name = WiFi.SSID(i);
    
    device["bssid"] = bssid;
    device["rssi"] = rssi;
    device["ssid"] = ssid_name;
    
    Serial.printf("  %d: %s (%s) %d dBm\n", i+1, ssid_name.c_str(), bssid.c_str(), rssi);
  }
  
  // Send UDP packet
  String jsonString;
  serializeJson(doc, jsonString);
  
  Udp.beginPacket(serverIP, serverPort);
  Udp.print(jsonString);
  Udp.endPacket();
  
  Serial.println("Data sent to server");
  Serial.println("---");
}
