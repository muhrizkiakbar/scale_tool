import RPi.GPIO as GPIO
from hx711 import HX711  # Install via pip: pip install HX711
import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

# Constants
DATA_PIN = 5
CLOCK_PIN = 6
TARE_BUTTON_PIN = 17
OLED_WIDTH = 128
OLED_HEIGHT = 32
MAX_WEIGHT_KG = 10  # Maximum load cell capacity in kilograms

# Setup OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Setup HX711
hx = HX711(DATA_PIN, CLOCK_PIN)

# GPIO setup for Tare Button
GPIO.setmode(GPIO.BCM)
GPIO.setup(TARE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def calibrate():
    """Calibrate the scale with a known weight."""
    print("Ensure the scale is empty, then press Enter.")
    input()
    hx.reset()
    print("Calibrating... Ensure the scale is stable.")
    hx.tare()
    print("Place a known weight on the scale (e.g., 1kg), then press Enter.")
    input()
    known_weight = float(input("Enter the weight in grams: "))
    reading = hx.get_raw_data_mean()
    scale_factor = reading / known_weight
    hx.set_scale_ratio(scale_factor)
    print(f"Calibration complete. Scale factor set to: {scale_factor}")

def display_weight(weight):
    """Display the weight on the OLED."""
    oled.fill(0)
    oled.text("Weight:", 0, 0)
    oled.text(f"{weight:.2f} g", 0, 16)
    oled.show()

def main():
    print("Initializing scale...")
    calibrate()
    print("Scale ready. Press the tare button to reset weight.")
    while True:
        if GPIO.input(TARE_BUTTON_PIN) == GPIO.LOW:  # Button pressed
            print("Taring...")
            hx.tare()
            print("Tare complete.")
        weight = hx.get_weight_mean(10)  # Average over 10 samples
        display_weight(weight)
        time.sleep(0.1)

try:
    main()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()

