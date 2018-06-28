"""Drivers for shared functionality provided by AI Makers Kit."""

import gkit._button
import gkit._led

# GPIO definitions
GPIO_BUTTON = 29
GPIO_LED = 31

# Import LED class to expose the LED constants.
LED = gkit._led.LED

# Global variables. They are lazily initialized.
_gkit_button = None
_gkit_led = None


def get_button():
    """Returns a driver to the AI.Makers.Kit button.

    The button driver detects edges on GPIO_BUTTON. It can be used both
    synchronously and asynchrously.

    Synchronous usage:
        button = gkit.drivers.get_button()
        button.wait_for_press()
        # The above function does not return until the button is pressed.
        my_recognizer.recognize()
        ...

    Asynchronous usage:
        def on_button_press(_):
            print('The button is pressed!')

        button = gkit.drivers.get_button()
        button.on_press(on_button_press)
        # The console will print 'The button is pressed!' every time the button is
        # pressed.
        ...
        # To cancel the callback, pass None:
        button.on_press(None)
        # Calling wait_for_press() also cancels any callback.
    """
    global _gkit_button
    if _gkit_button is None:
        _gkit_button = gkit._button.Button(channel=GPIO_BUTTON)
    return _gkit_button


def get_led():
    """Returns a driver to control the AI.Makers.Kit LED light with various animations.

    led = gkit.drivers.get_led()

    # You may set any LED animation:
    led.set_state(gkit.drivers.LED.PULSE_QUICK)
    led.set_state(gkit.drivers.LED.BLINK)

    # Or turn off the light but keep the driver running:
    led.set_state(gkit.drivers.LED_OFF)
    """
    global _gkit_led
    if _gkit_led is None:
        _gkit_led = gkit._led.LED(channel=GPIO_LED)
        _gkit_led.start()
    return _gkit_led

