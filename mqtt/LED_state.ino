#define BUTTON_PIN_1 26
#define BUTTON_PIN_2 27
#define LED_PIN 33
#define LED_R_1 18
#define LED_Y_1 19
#define LED_G_1 21

int button_state1;
int button_state2;
int led_state = LOW; 
int last_button_state;
int last_button_state2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
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
