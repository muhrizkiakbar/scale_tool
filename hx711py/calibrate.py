import time
import RPi.GPIO as GPIO
from hx711 import HX711  # Import your HX711 class

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
zero_button = 17  # Change GPIO pin if needed
GPIO.setup(zero_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up as input with pull-up resistor

# Set up HX711
hx711 = HX711(5,6, gain=128)  # Adjust pins for HX711

# Tare the scale initially
hx711.reset()
hx711.tare()

# Function to read average raw value
def read_average(times=10):
    total = 0
    for _ in range(times):
        total += hx711.get_value()
    return total // times

# Function to calibrate the scale
def calibrate(load_cell_weight):
    print("Taring the scale...")
    hx711.tare()  # Tare the scale
    time.sleep(2)

    print("Place known weight on the scale.")
    time.sleep(4)

    print("Reading raw value for the known weight...")
    raw_value = read_average(10)  # Read raw value several times to get an average
    print(f"Raw Value with known weight: {raw_value}")

    # Calculate scale factor
    scale_factor = raw_value / load_cell_weight
    print(f"Scale Factor: {scale_factor}")

    return scale_factor

# Known weight for calibration
known_weight = 200  # Adjust to the weight you will use to calibrate (grams)

# Start calibration
scale_factor = calibrate(known_weight)

# Zero button debounce function
def is_button_pressed():
    # time.sleep(0.05)  # Debounce delay
    # return not zero_button.value()  # Button pressed when value is LOW
    time.sleep(0.05)  # Debounce delay
    return GPIO.input(zero_button) == GPIO.LOW  # Button pressed when value is LOW

# Main loop
try:
    while True:
        if is_button_pressed():  # Check if the button is pressed
            # lcd.clear()
            # lcd.putstr("Zeroing scale...")
            hx711.tare()  # Zero (tare) the scale
            time.sleep(1)  # Give time for taring
            # lcd.clear()
        
        weight_raw = hx711.get_value()
        weight_grams = weight_raw / scale_factor
        weight_grams_int = int(weight_grams)

        print(f"Weight: {weight_grams_int}")
        # lcd.clear()
        # lcd.putstr(f"Weight: {weight_grams_int} g")
        time.sleep(1)
except KeyboardInterrupt:
        pass # or print("received a keyboard interrupt, exiting.")
finally:
    GPIO.cleanup()

