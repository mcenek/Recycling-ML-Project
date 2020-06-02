#!/bin/bash

cd sound_files/
arecord -D plughw:2  -c1 -r 48000 -d 5 -f S32_LE -t wav -V mono -v $1
cd ..