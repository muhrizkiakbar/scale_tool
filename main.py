import time
import RPi.GPIO as GPIO
from hx711 import HX711
import board
import busio
import adafruit_ssd1306

# Pin setup
DT_PIN = 5  # HX711 DT
SCK_PIN = 6  # HX711 SCK
TARE_BUTTON_PIN = 17  # GPIO for tare button

# OLED setup
i2c = busio.I2C(board.SCL, board.SDA)
WIDTH = 128
HEIGHT = 32
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# HX711 setup
hx = HX711(DOUT_PIN=DT_PIN, PD_SCK=SCK_PIN)

# Global variables
tare_offset = 0
CALIBRATION_FACTOR = 1  # To be determined during calibration


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TARE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    hx.reset()
    hx.tare()  # Tare the scale

    oled.fill(0)
    oled.show()


def calibrate():
    print("Place a known weight on the scale.")
    input("Press Enter when ready...")
    raw_val = hx.get_raw_data_mean(10)
    known_weight = float(input("Enter the weight (grams): "))
    calibration_factor = raw_val / known_weight
    print(f"Calibration Factor: {calibration_factor}")
    return calibration_factor


def tare(channel):
    global tare_offset
    tare_offset = hx.get_raw_data_mean(10)
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
            raw_data = hx.get_raw_data_mean(10)
            if raw_data is not None:
                weight = (raw_data - tare_offset) / CALIBRATION_FACTOR
                display_message(f"Weight: {weight:.2f} g")
            else:
                display_message("Error reading!")
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

