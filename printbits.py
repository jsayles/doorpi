import sys
import time
import pifacedigitalio
from datetime import datetime

class Controller:
   pifacedigital = pifacedigitalio.PiFaceDigital()
   listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

   def data0Pulse(self, event):
      sys.stdout.write("0")

   def data1Pulse(self, event):
      sys.stdout.write("1")

   def start(self, d0pin, d1pin):
      print "Listening on pins %s and %s" % (d0pin, d1pin)
      self.listener.register(d0pin, pifacedigitalio.IODIR_FALLING_EDGE, self.data0Pulse)
      self.listener.register(d1pin, pifacedigitalio.IODIR_FALLING_EDGE, self.data1Pulse)
      self.listener.activate()

   def stop(self):
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
         sys.stdout.flush()
   except (KeyboardInterrupt, SystemExit):
      controller.stop()
      sys.exit(0)
