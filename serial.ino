int option;
int led = 8;
int pass=0;
void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
}
void loop(){
 
 //si existe datos disponibles los leemos
 if (Serial.available()>0){
    option=Serial.read();
    if(option=='A'){
      Serial.write('B');//reconocimiento de arduino por la interfaz python 
      Serial.write('\n');//reconocimiento de arduino por la interfaz python      
    }   
  
    if(option=='L') {
      //delay(1000);
      digitalWrite(led, LOW);
      //Serial.println("OFF");
    }
    else if(option=='H') {
      //delay(1000);
      digitalWrite(led, HIGH);
      //Serial.println("ON");
    }
  }
}
