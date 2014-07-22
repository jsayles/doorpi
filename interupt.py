import sys
import pifacedigitalio

class Controller:
   pifacedigital = pifacedigitalio.PiFaceDigital()
   listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

   pressCount = 0

   def switch_pressed(self, event):
      #print "pressed"
      event.chip.output_pins[event.pin_num].turn_on()
      self.pressCount = self.pressCount + 1

   def switch_unpressed(self, event):
      #print "unpressed"
      event.chip.output_pins[event.pin_num].turn_off()

   def start(self):
      self.listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, self.switch_pressed)
      self.listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, self.switch_unpressed)
      self.listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, self.switch_pressed)
      self.listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, self.switch_unpressed)
      self.listener.activate()

   def stop(self):
      print "Pressed %s times!" % self.pressCount
      self.listener.deactivate()

if __name__ == "__main__":
   controller = Controller()
   controller.start()

   loopCount = 0
   try:
      while True:
         loopCount = loopCount + 1
   except (KeyboardInterrupt, SystemExit):
      controller.stop()
      sys.exit(0)
