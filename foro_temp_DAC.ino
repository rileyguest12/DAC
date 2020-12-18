// Author: Riley Guest  https://www.ametherm.com/thermistor/ntc-thermistors-steinhart-and-hart-equation

int data;
int thermistor1Pin = 0;                // Analog pin designation for thermistors 
int thermistor2Pin = 1;           
int thermistor3Pin = 2;
int thermistor4Pin = 3;
int thermistor5Pin = 4;
int thermistor6Pin = 5;

int redPin = 10;                      // Digital pin for red LED
int greenPin = 12;                    // Digital pin for green LED
int bluePin = 11;                     // Digital pin for blue LED

int V0, V1, V2, V3, V4, V5;           // The analog output of the voltage across both thermistors will average both readings

float resistance = 10000;             // Resistor value in the circuit 10k ohm

float logR0, logR1, logR2, logR3, logR4, logR5;
float R0, R1, R2, R3, R4, R5;
float T0, T1, T2, T3, T4, T5, Tc, Tf, Tave;     // Variables for calculations  

float c1 = 1.009249522e-03,
      c2 = 2.378405444e-04,     // The three coefficients in the steinhart-hart equation
      c3 = 2.019202697e-07;

float tempzero;

int Status;

void setup() 
{
Serial.begin(9600);             // Starts the serial read at a baudrate of 9600
pinMode(redPin, OUTPUT);        // Initializes the redPin as a digital output
pinMode(greenPin, OUTPUT);      // Initializes the greenPin as a digital output
pinMode(bluePin, OUTPUT);       // Initializes the bluePin as a digital output
}

void loop() 
{                               // Starts the main loop function
//  if (Serial.available() > 0);  // If the serial is available, start the function
  {
  int data = Serial.read();               // Declaring 'data' as an integer and it is constantly reading the serial for inputs
                                          // This works for talking the arduino serial from python, giving commands and such
                                          
  V0 = analogRead(thermistor1Pin);         // Declares V0 as the variable for the analog signal coming from Arduino 
  V1 = analogRead(thermistor2Pin);       
  V2 = analogRead(thermistor3Pin);
  V3 = analogRead(thermistor4Pin);
  V4 = analogRead(thermistor5Pin);
  V5 = analogRead(thermistor6Pin);
  
  R0 = resistance * (1023.0 / (float)V0 - 1.0);   // Resistance reading off of V0
  R1 = resistance * (1023.0 / (float)V1 - 1.0);   
  R2 = resistance * (1023.0 / (float)V2 - 1.0);   
  R3 = resistance * (1023.0 / (float)V3 - 1.0);   
  R4 = resistance * (1023.0 / (float)V4 - 1.0);  
  R5 = resistance * (1023.0 / (float)V5 - 1.0);  

  logR0 = log(R0);
  logR1 = log(R1);
  logR2 = log(R2);
  logR3 = log(R3);
  logR4 = log(R4);                        
  logR5 = log(R5);                        
  
  T0 = (1.0 / (c1 + c2*logR0 + c3*logR0*logR0*logR0));     // Temperature reading off of thermistors
  T1 = (1.0 / (c1 + c2*logR1 + c3*logR1*logR1*logR1));     
  T2 = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));     
  T3 = (1.0 / (c1 + c2*logR3 + c3*logR3*logR3*logR3));    
  T4 = (1.0 / (c1 + c2*logR4 + c3*logR4*logR4*logR4));     
  T5 = (1.0 / (c1 + c2*logR5 + c3*logR5*logR5*logR5));     
  
  Tave = (T0+T1+T2+T3+T4+T5)/(6);                         // Average calculation between the two                            
  Tc = Tave - 273.15;                                     // Conversion to celsius from kelvin
  Tf = (Tc * 9.0)/ 5.0 + 32.0;                            // Conversion to farenheit from celsius

  tempzero = T0-273.15;
   
  Serial.println(tempzero);        
//  Serial.print(" ");            
//  Serial.print(T1-273.15);        
//  Serial.print(" ");            
//  Serial.print(T2-273.15);        
//  Serial.print(" ");            
//  Serial.print(T3-273.15);         
//  Serial.print(" ");            
//  Serial.print(T4-273.15);             
//  Serial.print(" ");            
//  Serial.print(T5-273.15);            
//  Serial.print(" ");
//  Serial.println(Tave-273.15);             
  delay(100);                     
  }


  if (tempzero > 25) {                  // LED control with all conditional statements
    digitalWrite(redPin, HIGH);
    }
    
  else {
    digitalWrite(redPin, LOW);
    }
    
  if (Tc < 25) {
    digitalWrite (greenPin, HIGH);}
  
  else {
    digitalWrite(greenPin, LOW);}
    
  if (Tc < 15) {
    digitalWrite (bluePin, HIGH);}
    
  else {
    digitalWrite (bluePin,LOW);}
  
  if (data == '1') {
    digitalWrite (greenPin, HIGH);}
  
  else if (data =='0') {
    digitalWrite (greenPin, LOW);}
}
