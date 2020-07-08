#tests if the mic system is working
#originally written by John Haas

import subprocess

def main():
    #calls subprocess that runs mic
    cmd = ['/home/pi/Recycling-ML-Project-johns_testing/mic.sh', "mictest.wav"]
    p1=subprocess.run(cmd)

if __name__ == "__main__":
    main()