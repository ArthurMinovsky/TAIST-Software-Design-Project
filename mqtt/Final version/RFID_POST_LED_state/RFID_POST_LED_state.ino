#define BUTTON_PIN_1 26
#define BUTTON_PIN_2 27
#define LED_PIN 33
#define LED_R_1 18
#define LED_Y_1 19
#define LED_G_1 21

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

// If using the breakout with SPI, define the pins for SPI communication.
#define PN532_SCK  (14)
#define PN532_MOSI (13)
#define PN532_SS   (15)
#define PN532_MISO (12)
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);



const char* ssid = "Xysis";//WIFI SSID
const char* password = "enable111";//WIFI password

//Your Domain name with URL path or IP address with path
const char* serverName1 = "http://329f-1-47-130-233.ngrok.io/add_car_in";// API link car_out
const char* serverName2 = "http://329f-1-47-130-233.ngrok.io/add_car_out";// API link car_in
// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;
uint32_t oldcardid1 = 00000000;
uint32_t oldcardid2 = 00000000;


int button_state1;
int button_state2;
int led_state = LOW; 
int last_button_state;
int last_button_state2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN_1, INPUT_PULLUP);
  pinMode(BUTTON_PIN_2, INPUT_PULLUP);  

  pinMode(LED_R_1, OUTPUT); 
  pinMode(LED_Y_1, OUTPUT);
  pinMode(LED_G_1, OUTPUT);
  
  digitalWrite(LED_R_1, HIGH);
  digitalWrite(LED_Y_1, LOW);
  digitalWrite(LED_G_1, LOW);

  button_state1 = digitalRead(BUTTON_PIN_1);
  button_state2 = digitalRead(BUTTON_PIN_2);

  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);

  Serial.println("Waiting for an ISO14443A Card ...");
  
  WiFi.begin("Xysis", "enable111");
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("publishing the first reading.");
  
  
}

void buttonWait1(int buttonPin1){
  int buttonState1 = 0;
  while(1){
    buttonState1 = digitalRead(buttonPin1);
    if (buttonState1 == LOW) {
      return;
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  button_state1 = HIGH;	
  last_button_state = button_state1;
  button_state1 = digitalRead(BUTTON_PIN_1);
  

  if (last_button_state == HIGH && button_state1 == LOW) {
    Serial.println("The button is pressed");
    // toggle state of LED
    led_state = !led_state;
    Serial.println(led_state);
    // control LED arccoding to the toggled state
    digitalWrite(LED_PIN, led_state);
    
    if (led_state == 1){

  //CODE RFID//
      uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

    if (success) {
    // Display some basic information about the card
    Serial.println("Found an ISO14443A card");
    Serial.print("  UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
    Serial.print("  UID Value: ");
    nfc.PrintHex(uid, uidLength);

    if (uidLength == 4)
    {
      // We probably have a Mifare Classic card ...
      uint32_t cardid = uid[0];
      cardid <<= 8;
      cardid |= uid[1];
      cardid <<= 8;
      cardid |= uid[2];
      cardid <<= 8;
      cardid |= uid[3];
      Serial.print("Seems to be a Mifare Classic card #");
      Serial.println(cardid);

      
       //Send an HTTP POST request every 10 minutes
  if (oldcardid1 != cardid) {

    //LED PART accuator part
    
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
    
      // Your Domain name with URL path or IP address with path
      http.begin(client, serverName1);
      
      // If you need Node-RED/server authentication, insert user and password below
      //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
      
      // Specify content-type header
      //
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      // Data to send with HTTP POST
      
      //String httpRequestData = "api_key=tPmAT5Ab3j7F9&sensor=BME280&value1=24.25&value2=49.54&value3=1005.14";           
      // Send HTTP POST request
      
      //int httpResponseCode = http.POST(httpRequestData);
      
      // If you need an HTTP request with a content type: application/json, use the following:
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST("{\"card_id\":\""+String(cardid)+"\"}");

      // If you need an HTTP request with a content type: text/plain
      //http.addHeader("Content-Type", "text/plain");
      //int httpResponseCode = http.POST("Hello, World!");
     
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
        
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    oldcardid1 = cardid;
  }





      
    }
    Serial.println("");
   }
   //RFID
      

      delay(1000);
      
      digitalWrite(LED_R_1, LOW);
      digitalWrite(LED_Y_1, HIGH);
      digitalWrite(LED_G_1, LOW);
      delay(1000);
      buttonWait1(27);
      digitalWrite(LED_R_1, LOW);
      digitalWrite(LED_Y_1, LOW);
      digitalWrite(LED_G_1, HIGH);
      delay(2000);   
      digitalWrite(LED_R_1, HIGH);
      digitalWrite(LED_Y_1, LOW);
      digitalWrite(LED_G_1, LOW);
      led_state = 0;  
      digitalWrite(LED_PIN, led_state);     
    }
  }



  
  else if(last_button_state == HIGH && button_state1 == HIGH){
    if(led_state == 0){
    button_state2 = digitalRead(BUTTON_PIN_2);
      if (button_state2 == LOW){
        digitalWrite(LED_R_1, LOW);
      	digitalWrite(LED_Y_1, HIGH);
      	digitalWrite(LED_G_1, LOW);     
        delay(2000);

   //RFID pub complete//
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

    if (success) {
    // Display some basic information about the card
    Serial.println("Found an ISO14443A card");
    Serial.print("  UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
    Serial.print("  UID Value: ");
    nfc.PrintHex(uid, uidLength);

    if (uidLength == 4)
    {
      // We probably have a Mifare Classic card ...
      uint32_t cardid = uid[0];
      cardid <<= 8;
      cardid |= uid[1];
      cardid <<= 8;
      cardid |= uid[2];
      cardid <<= 8;
      cardid |= uid[3];
      Serial.print("Seems to be a Mifare Classic card #");
      Serial.println(cardid);

      
       //Send an HTTP POST request every 10 minutes
  if (oldcardid2 != cardid) {

    //LED PART accuator part
    
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
    
      // Your Domain name with URL path or IP address with path
      http.begin(client, serverName2);
      
      // If you need Node-RED/server authentication, insert user and password below
      //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
      
      // Specify content-type header
      //
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      // Data to send with HTTP POST
      
      //String httpRequestData = "api_key=tPmAT5Ab3j7F9&sensor=BME280&value1=24.25&value2=49.54&value3=1005.14";           
      // Send HTTP POST request
      
      //int httpResponseCode = http.POST(httpRequestData);
      
      // If you need an HTTP request with a content type: application/json, use the following:
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST("{\"card_id\":\""+String(cardid)+"\"}");

      // If you need an HTTP request with a content type: text/plain
      //http.addHeader("Content-Type", "text/plain");
      //int httpResponseCode = http.POST("Hello, World!");
     
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
        
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    oldcardid2 = cardid;
  }   
    }
    Serial.println("");
  }
  //Rfid
  
      
        digitalWrite(LED_R_1, LOW);
      	digitalWrite(LED_Y_1, LOW);
      	digitalWrite(LED_G_1, HIGH);  
        delay(2000); 
      }
    }
  } 
  digitalWrite(LED_R_1, HIGH);
  digitalWrite(LED_Y_1, LOW);
  digitalWrite(LED_G_1, LOW);  
}
