import sys
import time
import pifacedigitalio
from datetime import datetime

DATAFILE = "data.log"
FLUSH = 8

class Controller:
   pifacedigital = pifacedigitalio.PiFaceDigital()
   listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

   def data0Pulse(self, event):
      self.datafile.write("0")
      self.bit_count = self.bit_count + 1
      if self.bit_count >= FLUSH:
         self.datafile.flush()
         self.bit_count = 0

   def data1Pulse(self, event):
      self.datafile.write("1")
      self.bit_count = self.bit_count + 1
      if self.bit_count >= FLUSH:
         self.datafile.flush()
         self.bit_count = 0

   def start(self, d0pin, d1pin):
      print "Opening '%s' for writing" % DATAFILE
      self.datafile = open(DATAFILE, 'a') 
      self.datafile.write("\n")
      self.datafile.write(str(datetime.now()))
      self.datafile.write("\n")
      self.datafile.flush()

      print "Listening on pins %s and %s" % (d0pin, d1pin)
      self.listener.register(d0pin, pifacedigitalio.IODIR_FALLING_EDGE, self.data0Pulse)
      self.listener.register(d1pin, pifacedigitalio.IODIR_FALLING_EDGE, self.data1Pulse)
      self.listener.activate()

      self.bit_count = 0

   def stop(self):
      self.datafile.close()
      self.listener.deactivate()

if __name__ == "__main__":
   # Start our controller on pins 0 and 1
   controller = Controller()
   controller.start(0, 1)

   loopCount = 0
   try:
      while True:
         loopCount = loopCount + 1
         time.sleep(1)
   except (KeyboardInterrupt, SystemExit):
      controller.stop()
      sys.exit(0)
