#! /bin/bash

if [ $1 == 'CH1' ]
then
 ch=26
elif [ $1 == 'CH2' ]
then
 ch=20
elif [ $1 == 'CH3' ]
then
 ch=21
else
 echo "Parameter error"
 exit
fi

if [ $2 == 'ON' ]
then
 state=0
elif [ $2 == 'OFF' ]
then
 state=1
else
 echo "Parameter error"
 exit
fi

echo $ch > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio$ch/direction
echo $state > /sys/class/gpio/gpio$ch/value
echo Relay $1 $2

