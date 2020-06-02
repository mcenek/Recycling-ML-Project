/****************************************************
			
			P26    ---->    Relay_Ch1
			P20    ---->    Relay_Ch2
			P21    ---->    Relay_Ch3

****************************************************/
#include "bcm2835.h"
#include "stdio.h"

#define Relay_Ch1 26
#define Relay_Ch2 20
#define Relay_Ch3 21

int main(int argc,char **argv)
{
	if(!bcm2835_init()) return 1;
	bcm2835_gpio_fsel(Relay_Ch1,BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_fsel(Relay_Ch2,BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_fsel(Relay_Ch3,BCM2835_GPIO_FSEL_OUTP);
	
	printf("Setup The Relay Module is [success]!\n");
	while(1)
	{
		//Control The Channel 1
		bcm2835_gpio_write(Relay_Ch1,LOW);
		printf("Channel 1:The Common Contact is access to the Normal Open Contact!\n");
		bcm2835_delay(1000);

		bcm2835_gpio_write(Relay_Ch1,HIGH);
		printf("Channel 1:The Common Contact is access to the Normal Closed Contact!\n\n");
		bcm2835_delay(1000);


		//Control The Channnel 2
		bcm2835_gpio_write(Relay_Ch2,LOW);
		printf("Channel 2:The Common Contact is access to the Normal Open Contact!\n");
		bcm2835_delay(1000);
		
		bcm2835_gpio_write(Relay_Ch2,HIGH);
		printf("Channel 2:THe Common Contact is access to the Normal Closed Contact!\n\n");
		bcm2835_delay(1000);


		//Control The Channel 3
		bcm2835_gpio_write(Relay_Ch3,LOW);
		printf("Channel 3:The Common Contact is access to the Normal Open Contact!\n");
		bcm2835_delay(1000);

		bcm2835_gpio_write(Relay_Ch3,HIGH);
		printf("Channel 3:the Common Contact is access to the Normal Closed Contact!\n\n");		
		bcm2835_delay(1000);
	}

	bcm2835_close();
	return 0;
}
