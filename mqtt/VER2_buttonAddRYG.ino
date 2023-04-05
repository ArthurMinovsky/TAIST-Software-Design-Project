#define BUTTON_PIN_1 26
#define BUTTON_PIN_2 27
#define LED_PIN 33
#define LED_R_1 18
#define LED_Y_1 19
#define LED_G_1 21

int button_state;
int led_state = LOW; 
int last_button_state;
int buttonState2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN_1, INPUT_PULLUP);
  pinMode(BUTTON_PIN_2, INPUT);  

  pinMode(LED_R_1, OUTPUT); 
  pinMode(LED_Y_1, OUTPUT);
  pinMode(LED_G_1, OUTPUT);
  
  digitalWrite(LED_R_1, HIGH);
  digitalWrite(LED_Y_1, LOW);
  digitalWrite(LED_G_1, LOW);

  button_state = digitalRead(BUTTON_PIN_1);
  buttonState2 = digitalRead(BUTTON_PIN_2);
    
}

void loop() {
  // put your main code here, to run repeatedly:

  last_button_state = button_state;
  button_state = digitalRead(BUTTON_PIN_1);

  if (last_button_state == HIGH && button_state == LOW) {
    Serial.println("The button is pressed");
    // toggle state of LED
    led_state = !led_state;
    Serial.println(led_state);
    // control LED arccoding to the toggled state
    digitalWrite(LED_PIN, led_state);
    
    if (led_state == 1){
      digitalWrite(LED_R_1, LOW);
		  digitalWrite(LED_Y_1, HIGH);
		  digitalWrite(LED_G_1, LOW);
      delay(1000);
      buttonState2 = digitalRead(BUTTON_PIN_2);
      Serial.println(buttonState2);

      if (buttonState2 == HIGH){
        digitalWrite(LED_R_1, LOW);
		    digitalWrite(LED_Y_1, LOW);
		    digitalWrite(LED_G_1, HIGH);
        delay(5000);
      }      
      else{
      digitalWrite(LED_R_1, HIGH);
		  digitalWrite(LED_Y_1, LOW);
		  digitalWrite(LED_G_1, LOW);      
      delay(1000);
      }    
    }
       
  }
  digitalWrite(LED_R_1, HIGH);
  digitalWrite(LED_Y_1, LOW);
  digitalWrite(LED_G_1, LOW);  
}
