from machine import Pin

led_onboard = Pin("LED", Pin.OUT)

def set_status(on):
    if on:
        led_onboard.on()
    else:
        led_onboard.off()