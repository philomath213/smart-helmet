#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// network credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

// API URL
const String URL = "http://192.168.1.164:5000/data/1";

#define DHTPIN D5
#define DHTTYPE DHT11

#define REMOVED_SENSOR D4
#define COLLISION_SENSOR D3

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Serial port for debugging purposes
  Serial.begin(9600);

  dht.begin();

  pinMode(REMOVED_SENSOR, INPUT);
  pinMode(COLLISION_SENSOR, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP32 Local IP Address
  Serial.println(WiFi.localIP());
  // Route for root / web page

}
void loop() {
  delay(3000);

  Serial.print("Requesting URL: ");

  int is_removed = !digitalRead(REMOVED_SENSOR);
  int collision = !digitalRead(COLLISION_SENSOR);
  
  // Data we like to post in json
  char postData[1024];
  sprintf(postData, "{\"is_removed\": %d, \"collision\": %d, \"temperature\": %d, \"humidity\": %d}", is_removed, collision, int(dht.readTemperature()) , int(dht.readHumidity()));

  HTTPClient http;
  http.begin(URL);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(postData);

  // Print HTTP return code
  Serial.println(httpCode);
  String payload = http.getString();

  // Print request response payload
  Serial.println(payload);
  http.end();

  // Close connection
  Serial.println("closing connection");
}
