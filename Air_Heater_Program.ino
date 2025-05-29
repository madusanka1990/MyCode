#include <AirHeaterModel.h>
#include <PI_Controller.h>
#include <LowPassFilter.h>
#include <WiFiS3.h>
#include "ThingSpeak.h"

AirHeaterModel AirHeater; //ahm(float u, float Tout_prev, float Tenv, float Ts)
PI_Controller cv; //PI_Control_Voltage(float yf, float ref, float kp, float Ts, float u_prev,  float err_prev, float Ti) and u = u_prev + kp*(err - err_prev) + (kp/Ti)*Ts*err;
LowPassFilter LPF; //lf(float y, float yf_prev, float Ts, float Tf)
WiFiClient client;


#define SECRET_SSID "NIROSHAN 1622"
#define SECRET_PASS "27}9jO65"
#define SECRET_CH_ID 2628614
#define SECRET_WRITE_APIKEY "CDHNE6ZW7NFC16CD"

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;

float Ts = 0.1;
float Tf = 5*Ts;
float kp = 2;
float Ti = 16;
float u, u_prev, y, y_prev, yf, yf_prev, err, err_prev;
float ref = 30;
float Tenv = 21;

void setup() {
  Serial.begin(9600);
  ConnectWiFi();
  ThingSpeak.begin(client);

  u = 0;
  u_prev = 0;
  y = 0;
  y_prev = 0;
  yf = 0;
  yf_prev = 0;
  err_prev = 0;
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data as a string
    String input = Serial.readString();
    // Convert the string to an integer
    ref = input.toInt();

    
  }
  err = ref - yf;
  u = cv.PI_Control_Voltage(yf, ref, kp, Ts, u_prev, err_prev, Ti);
  y = AirHeater.ahm(u, y_prev, Tenv, Ts);
  yf = LPF.lf(y, yf_prev, Ts, Tf);
  Serial.print(u);      
  Serial.print(","); 
  Serial.print(ref);      
  Serial.print(",");              
  Serial.println(yf);
  ThingSpeakWrite(yf, ref);
  u_prev = u;
  y_prev = y;
  yf_prev = yf;
  err_prev = err;
  delay(100);
}

void ConnectWiFi()
{
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // Attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(10000);
  }

  // You're connected now, so print out the data:
  Serial.println("You're connected to Wifi");
  PrintNetwork();
}

void PrintNetwork()
{
  Serial.print("WiFi Status: ");
  Serial.println(WiFi.status());
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void ThingSpeakWrite(float yf, float ref)
{
  char server[] = "api.thingspeak.com";
  unsigned long channelNumber = SECRET_CH_ID;
  String writeAPIKey = SECRET_WRITE_APIKEY;
  int channelField = 1;
  if (client.connect(server, 80))
  {
    String postData = "api_key=" + writeAPIKey + "&field" + String(1) + "=" + String(yf) + "&field" + String(2) + "=" + String(ref);
    client.println( "POST /update HTTP/1.1" );
    client.println( "Host: api.thingspeak.com" );
    client.println( "Connection: close" );
    client.println( "Content-Type: application/x-www-form-urlencoded" );
    client.println( "Content-Length: " + String( postData.length() ) );
    client.println();
    client.println( postData );
    //Serial.println ( "Sent to the Server" );
  }
  else
  {
    Serial.println ( "Connection Failed" );
  }

}

