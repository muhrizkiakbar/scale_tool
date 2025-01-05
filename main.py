import RPi.GPIO as GPIO
from time import sleep
from hx711 import HX711
from adafruit_ssd1306 import SSD1306_I2C
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Pin configuration
DT = 5
SCK = 6
TARE_BUTTON = 17

# Initialize HX711
hx = HX711(dout_pin=DT, pd_sck_pin=SCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)  # Set this after calibration
hx.reset()
hx.tare()

# Initialize OLED
WIDTH = 128
HEIGHT = 64
i2c = board.I2C()
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize LED Matrix
serial = spi(port=0, device=0, gpio=noop())
led_matrix = max7219(serial, cascaded=1, block_orientation=90)

# GPIO setup for Tare Button
GPIO.setmode(GPIO.BCM)
GPIO.setup(TARE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def calibrate():
    print("Calibrating... Place a known weight on the scale.")
    sleep(5)
    raw_value = hx.get_weight(5)
    known_weight = float(input("Enter the weight in grams: "))
    calibration_factor = raw_value / known_weight
    hx.set_reference_unit(calibration_factor)
    print(f"Calibration factor set to {calibration_factor}")
    hx.tare()
    return calibration_factor

def tare(channel):
    print("Tare button pressed. Resetting...")
    hx.tare()

# Attach button interrupt
GPIO.add_event_detect(TARE_BUTTON, GPIO.FALLING, callback=tare, bouncetime=300)

def display_measurements(weight):
    # OLED Display
    oled.fill(0)
    oled.text(f"Weight: {weight:.2f} g", 0, 0, 1)
    oled.show()

    # LED Matrix
    with canvas(led_matrix) as draw:
        draw.text((1, 1), f"{weight:.2f} g", fill="white")

def main():
    print("Starting scale...")
    calibration_factor = calibrate()

    try:
        while True:
            weight = hx.get_weight(5)
            display_measurements(weight)
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

