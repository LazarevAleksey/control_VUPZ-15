void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {}
}

String buffer = "";

void generate_answer_get_status(String bmk_num) {
  Serial.print("bmk="+bmk_num+" bmkS=007 bmkSK=2 pr=000 pr0=000 pr1=000 temp=+232 P05=064 P10=125 P15=219 P20=316 P25=401 P30=489 P35=581 Err=00000000 uPit=23 temHeart=+05 timeW=00003053 prAtmCal0=+00 prAtmCal1=+00 Styp=00 l=000 temp2=+242 timeR=000006 cs=114\r\n");
}

void generate_answer_get_status(String bmk_num, String Err){
  Serial.print("bmk="+bmk_num+" bmkS=007 bmkSK=2 pr=000 pr0=000 pr1=000 temp=+232 P05=064 P10=125 P15=219 P20=316 P25=401 P30=489 P35=581 Err="+ Err +" uPit=23 temHeart=+05 timeW=00003053 prAtmCal0=+00 prAtmCal1=+00 Styp=00 l=000 temp2=+242 timeR=000006 cs=114\r\n");
}

void generate_answer_gPr(String bmk_num, String pr1, String pr2){
  Serial.print("bmk="+bmk_num+" pr0="+pr1+" pr1="+pr2+" pr2=000 er=00000000 bmkC=007 prC0=003 prC1=000 erC=00000000 cs=016\r\n");
}


String list_of_bmk[13] = {"009", "010", "011", 
                          "012", "013", "014",
                          "015", "016", "017",
                          "018", "019", "020",
                          "021"};

void loop() {
  // serial read section
  while (Serial.available())  // this will be skipped if no data present, leading to
                              // the code sitting in the delay function below
  {
    delay(30);
    int b = Serial.available();
    for (int i = 0; i < b; ++i) {
      char c = Serial.read();
      buffer += String(c);
    }

    for(int i = 0; i < 13; ++i){
      String bmk = list_of_bmk[i];
      if (buffer.equals("bmk:" + bmk + ":getStatus\r\n")){
        generate_answer_get_status(bmk);
      } 
      continue;
      if (buffer.equals("bmk:" + bmk + ":gPr\r\n")){
        generate_answer_gPr(bmk, "300", "100");
      }      
      continue;
    }
    buffer = "";
  }
}
