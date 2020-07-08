#Originally intended for use with the relay base which has been since changed
#Originally written by Dan Moldovan and has since been modified for use without the relay by John Haas

import os
from gps import *
from time import *
import time
import threading

gpsd = None #seting the global variable

#class that handles gps operation
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

#      os.system('clear')

#     prints various readings from gps
      print (' GPS reading')
      print( '----------------------------------------')
      print('latitude    ' , gpsd.fix.latitude)
      print( 'longitude   ' , gpsd.fix.longitude)
      print('time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
      print('altitude (m)' , gpsd.fix.altitude)
      print ('eps         ' , gpsd.fix.eps)
      print ('epx         ' , gpsd.fix.epx)
      print ('epv         ' , gpsd.fix.epv)
      print ('ept         ' , gpsd.fix.ept)
      print ('speed (m/s) ' , gpsd.fix.speed)
      print ('climb       ' , gpsd.fix.climb)
      print ('track       ' , gpsd.fix.track)
      print ('mode        ' , gpsd.fix.mode)
      print()
      print ('sats        ' , gpsd.satellites)

      time.sleep(2) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print("Done")