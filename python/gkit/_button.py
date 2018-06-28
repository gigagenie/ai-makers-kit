import time

import RPi.GPIO as GPIO

class Button(object):

    def __init__(self,
                 channel,
                 polarity=GPIO.FALLING,
                 pull_up_down=GPIO.PUD_UP,
                 debounce_time=0.08):
        if polarity not in [GPIO.FALLING, GPIO.RISING]:
            raise ValueError(
                'polarity must be one of: GPIO.FALLING or GPIO.RISING')

        self.channel = int(channel)
        self.polarity = polarity
        self.expected_value = polarity == GPIO.RISING
        self.debounce_time = debounce_time

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN, pull_up_down=pull_up_down)

        self.callback = None

    def wait_for_press(self):
        GPIO.add_event_detect(self.channel, self.polarity)
        while True:
            if GPIO.event_detected(self.channel) and self._debounce():
                GPIO.remove_event_detect(self.channel)
                return
            time.sleep(0.02)

    def on_press(self, callback):
        GPIO.remove_event_detect(self.channel)
        if callback is not None:
            self.callback = callback
            GPIO.add_event_detect(
                self.channel, self.polarity, callback=self._debounce_and_callback)

    def _debounce_and_callback(self, _):
        if self._debounce():
            self.callback()

    def _debounce(self):
        start = time.time()
        while time.time() < start + self.debounce_time:
            if GPIO.input(self.channel) != self.expected_value:
                return False
            time.sleep(0.01)
        return True
