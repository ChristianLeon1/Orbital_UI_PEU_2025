#include <SPI.h> 
#include <SD.h> 

File myfile; 
char a; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000); 

  while(!Serial);  // Esperar a que se abra el serial port. 

  delay (5000);

  Serial.print("Inicializando tarjeta SD ... \n");

  if (!SD.begin(5)) {
    Serial.println("Inicialización fallida. Comprobar tarjeta SD \n");
    while (1);
  }
  Serial.println("Inicialización completa. \n \n");

  myfile = SD.open("/Datos_mis_simul.csv"); 
  if (myfile){
    while (myfile.available()){
      a = myfile.read();
      Serial.write(a);
      if (a == '\n') {
        delay (33); 
      }
    }
    myfile.close(); 
  } else {
    Serial.println("Error al abrir el archivo: Datos_mis_simul.csv");
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
