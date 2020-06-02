#!/bin/bash

cd microphone/
arecord -D plughw:2 -d 5 -c1 -r 48000 -f S32_LE -t wav -V mono -v $1
cd ..