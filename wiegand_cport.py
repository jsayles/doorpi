import sys
import time
import pifacedigitalio

WIEGANDMAXDATA = 32
WIEGANDTIMEOUT = 3000000

class Controller:
   pifacedigital = pifacedigitalio.PiFaceDigital()
   listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

   wiegandData = [0] * WIEGANDMAXDATA
   wiegandBitCount = 0
   #wiegandBitTime

   def data0Pulse(self, event):
      #print "data0Pulse"
      if self.wiegandBitCount / 8 < WIEGANDMAXDATA:
         self.wiegandData[self.wiegandBitCount / 8] <<= 1;
         self.wiegandBitCount = self.wiegandBitCount + 1
      #clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);

   def data1Pulse(self, event):
      #print "data1Pulse"
      if self.wiegandBitCount / 8 < WIEGANDMAXDATA:
         self.wiegandData[self.wiegandBitCount / 8] <<= 1
         self.wiegandData[self.wiegandBitCount / 8] |= 1
         self.wiegandBitCount = self.wiegandBitCount + 1
      #clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);

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
         print controller.wiegandData
         time.sleep(1)
   except (KeyboardInterrupt, SystemExit):
      controller.stop()
      sys.exit(0)
