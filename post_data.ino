#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <DHT.h>

// sensor settings
int dhtPin = 2; // signal in pin 2 (digital)
#define DHT_TYPE DHT22
DHT dht(dhtPin, DHT_TYPE);

// Wifi settings
char ssid[] = "YourWiFiSSID";
char pass[] = "YourWiFiPWD";

// server settings
// LAN IP: hostname -I
char serverAddress[] = "192.168.1.105";
int serverPort = 8080;

// run server
// cd to server.py folder > python3 server.py 8080

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort);
int status = WL_IDLE_STATUS;

void setup() {
  Serial.begin(9600);
  while ( status != WL_CONNECTED) {
    Serial.print("Arduino attempting to connect to Network named: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
  }

  // print the SSID and IP
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  Serial.print("Arduino IP: ");
  Serial.println(ip);
  Serial.print("Server IP: ");
  Serial.println(serverAddress);
  Serial.print("Server PORT: ");
  Serial.println(serverPort);

  delay(2000);
  Serial.println("Reading temperature and humidity data...go to browser!");
  dht.begin();
}

void loop() {

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  float hic = dht.computeHeatIndex(temperature, humidity, false); // heat index Celsius

  // error if sensor values are empty
  if( isnan(humidity) || isnan(temperature) ) {
    Serial.println("DHT Sensor read Failed!");
    return;
  }

  // sending sensor data to server
  Serial.println("making POST request");
  String contentType = "application/x-www-form-urlencoded";
  String postData = "temperature="+String(temperature)+"&humidity="+String(humidity)+"&hic="+String(hic);

  client.post("/store/", contentType, postData); // django view

  // read the status code and body of the response from server
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  Serial.println("Wait a minute...");
  delay(60000);
}
