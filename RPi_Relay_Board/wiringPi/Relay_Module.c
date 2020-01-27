/****************************************************

				P25 ----> Relay_Ch1
				P28 ----> Relay_Ch2
				P29 ----> Relay_Ch3

*****************************************************/
#include <wiringPi.h>
#include <stdio.h>

#define Relay_Ch1 25
#define Relay_Ch2 28
#define Relay_Ch3 29

int main(void)
{
	if(wiringPiSetup() == -1)return 0;
	pinMode(Relay_Ch1,OUTPUT);
	pinMode(Relay_Ch2,OUTPUT);
	pinMode(Relay_Ch3,OUTPUT);
	printf("Setuping The Realy Module is [success]\n");

	while(1)
	{
		//Control the Channel 1
		digitalWrite(Relay_Ch1,LOW);
		printf("Channel 1:The Common Contact is access to the Normal Open Contact!\n");
		delayMicroseconds(1000000);//delay 10ms

		digitalWrite(Relay_Ch1,HIGH);
		printf("Channel 1:The Common Contact is access to the Normal Closed Contact!\n\n");
		delayMicroseconds(1000000);//delay 10ms


		//Control the Channel 2
		digitalWrite(Relay_Ch2,LOW);
		printf("Channel 2:The Common Contact is access to the Normal Open Contact!\n");	
		delayMicroseconds(1000000);//delay 10ms

		digitalWrite(Relay_Ch2,HIGH);
		printf("Channel 2:The Common Contact is access to the Normal Closed Contact!\n\n");
		delayMicroseconds(1000000);//delay 10ms


		//Control The Channel 3
		digitalWrite(Relay_Ch3,LOW);
		printf("Channel 3:The Common Contact is access to the Normal Open Contact!\n");
		delayMicroseconds(1000000);//delay 10ms	
		
		digitalWrite(Relay_Ch3,HIGH);
		printf("Channel 3:The Common Contact is access to the Normal Closed Contact!\n\n");
		delayMicroseconds(1000000);//delay 10ms
	}
	
}
