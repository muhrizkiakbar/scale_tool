import time
import RPi.GPIO as GPIO
from hx711 import HX711
from smbus2 import SMBus
import adafruit_ssd1306

# Pin setup
DT_PIN = 5  # HX711 DT
SCK_PIN = 6  # HX711 SCK
TARE_BUTTON_PIN = 17  # GPIO for tare button

# OLED setup
I2C_BUS = SMBus(1)
OLED_ADDRESS = 0x3C
WIDTH = 128
HEIGHT = 32
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, I2C_BUS, addr=OLED_ADDRESS)

# HX711 setup
hx = HX711(dout_pin=DT_PIN, pd_sck_pin=SCK_PIN)

# Global variables
tare_offset = 0

# Calibration factor (to be determined during calibration)
CALIBRATION_FACTOR = 1  # Adjust after calibration


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TARE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(CALIBRATION_FACTOR)
    hx.reset()
    hx.tare()

    oled.fill(0)
    oled.show()


def calibrate():
    print("Place a known weight on the scale.")
    input("Press Enter when ready...")
    raw_val = hx.get_weight(10)
    known_weight = float(input("Enter the weight (grams): "))
    calibration_factor = raw_val / known_weight
    print(f"Calibration Factor: {calibration_factor}")
    return calibration_factor


def tare(channel):
    global tare_offset
    tare_offset = hx.get_weight(10)
    print("Tared!")
    display_message("Tared!")


def display_message(message):
    oled.fill(0)
    oled.text(message, 0, 0, 1)
    oled.show()


def main():
    global tare_offset
    try:
        setup()
        GPIO.add_event_detect(TARE_BUTTON_PIN, GPIO.FALLING, callback=tare, bouncetime=300)

        while True:
            weight = (hx.get_weight(10) - tare_offset) / CALIBRATION_FACTOR
            display_message(f"Weight: {weight:.2f} g")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
        oled.fill(0)
        oled.show()


if __name__ == "__main__":
    CALIBRATION_FACTOR = calibrate()
    main()

