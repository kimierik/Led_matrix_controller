const int datapin = 9;
const int data2pin = 6;
const int clockpin = 11;
const int clock2pin = 5;
const int latchpin = 10;

const int rows         = 15; //the number on horizontal rows
const int collumbs     = 16; //the number of vertical collumbs

int lediterate = 8;

//the image you get when you start the system
int dummy[100] = {7 + 16 * 5, 10 + 16 * 5, 139, 138 + 16, 137 + 16 * 2, 136 + 16 * 2, 135 + 16, 134};
//array size is set to 100. to we can have max of 100 leds on at the same time
//more leds would just look too slow and they would just start blinking

long rnum;
long cnum;

bool reading = false;
int ledlength = -1;

void setup() {
  pinMode(datapin, OUTPUT);
  pinMode(data2pin, OUTPUT);
  pinMode(clockpin, OUTPUT);
  pinMode(clock2pin, OUTPUT);
  pinMode(latchpin, OUTPUT);
  Serial.begin(9600);
  /*
    for (int i =0;i<totalnum;i++){
    dummy[i]= dummy[i]+16*14;

    };
  */



}




//VV this is the part that receives data and puts it in to the array
void loop() {
  int bytesToRead = Serial.available();
  if (!reading && bytesToRead>=2) {
    int command = Serial.read();
    if (command == 'w') {
      reading = true;
      lediterate = 0;
      
      ledlength=Serial.read();
      
      for (int i = 0; i < 100; i++) {
        dummy[i] = -1;
      }
      //reset dummy
    }
  }

  if (reading && Serial.available() > 0) {
   int led = Serial.read();
    if (led < 0) {
      return;
    }
    if (lediterate<100){
    
    
    dummy[lediterate] = led;
    lediterate++;
    }
  }

  if (lediterate >= ledlength) {
    reading = false;
  }



  //bool plus;
  int row;
  int collum;
  //long i = 1;

if (reading){
  return;
  }
  //leds on one at a time
  //needs a data input rework or make the algo within the for loop
  for (int led = 0; led < lediterate; led++) {
    row = ceil((float(dummy[led]) / float(collumbs)));

    collum = dummy[led] - ((row - 1) * collumbs);
    //Serial.println("r"+String(row)+"c"+String(collum)+"led"+String(dummy[led]));

    rnum = 1 << (row - 1);
    cnum = 1 << (collum - 1);


    //Serial.println("rn"+String(rnum)+"cn"+String(cnum)+"led"+String(dummy[led]));
    digitalWrite(latchpin, LOW);
    shiftOut(datapin, clockpin, MSBFIRST, rnum >> 8);
    shiftOut(datapin, clockpin, MSBFIRST, rnum);

    shiftOut(data2pin, clock2pin, MSBFIRST, cnum >> 8);
    shiftOut(data2pin, clock2pin, MSBFIRST, cnum);
    digitalWrite(latchpin, HIGH);


  }
}
