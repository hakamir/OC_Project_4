// Librairie et Variable
#include <WaspSigfox.h>
#include <String.h>
WaspUART UART;
int i;
uint8_t socket = SOCKET0;
uint8_t error;
uint32_t address   = 0x000001;

char sigfox_packet[25];
char tab[5] = {};
int c = 0;
int flag = 0;


// Setup du code 
void setup()
{
  // Init
  USB.ON();
  UART.setBaudrate(115200);
  UART.setUART(1);
  UART.beginUART();
  Utils.setMuxAux1();
  delay(2000);

// Configuration SIGFOX
  USB.ON();
  //////////////////////////////////////////////
  // switch on
  //////////////////////////////////////////////
  error = Sigfox.ON(socket);
  // Check status
  if( error == 0 ) 
  {
    USB.println(F("Switch ON OK")); 
  }
  else 
  {
    USB.println(F("Switch ON ERROR")); 
  } 
}

// Main 
void loop()
{
  // put your main code here, to run repeatedly:
  delay(500);
  if (serialAvailable(1))
  {
    UART.readBuffer(11); 
    tab[0] = UART._buffer [0];
    tab[1] = UART._buffer [1]; 
    flag = 1;
    USB.println(tab);
  }
  
  // Si UART OK alors envoie du packet
  if (flag == 1)
  {
    snprintf( sigfox_packet, sizeof(sigfox_packet), "%s", tab);
    USB.println(F("Routing the packet to Sigfox network (only first 12 bytes)..."));    
    USB.print(F("Sigfox packet to send: "));
    USB.println(sigfox_packet); 

   // send Sigfox packet with received data (only first 12 bytes)  
    error = Sigfox.send(sigfox_packet);

    // Check sending status
    if( error == 0 ) 
    {
      USB.println(F("Sigfox packet sent OK"));     
    }
    else 
    {
      USB.println(F("Sigfox packet sent ERROR")); 
    } 
      USB.println(F("---------------------------------------"));
      USB.println();
      flag = 0;
  }
  delay(5000);
}
