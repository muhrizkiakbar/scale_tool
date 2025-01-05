import time
from machine import Pin, I2C
# from pico_i2c_lcd import I2cLcd  # Import your I2C LCD class
from hx711 import HX711  # Import your HX711 class

# Set up I2C for the LCD
# i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # Adjust pins as needed

# # LCD setup
# lcd = I2cLcd(i2c, 0x27, 2, 16)  # Adjust the I2C address and dimensions

# Set up HX711
hx711 = HX711(clock=Pin(5), data=Pin(6), gain=128)  # Adjust pins for HX711

# Tare the scale initially
hx711.tare()

# Set up button for zeroing the scale
zero_button = Pin(15, Pin.IN, Pin.PULL_UP)  # Change GPIO 15 to your chosen pin

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
    time.sleep(2)

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
    time.sleep(0.05)  # Debounce delay
    return not zero_button.value()  # Button pressed when value is LOW

# Main loop
while True:
    if is_button_pressed():  # Check if the button is pressed
        # lcd.clear()
        # lcd.putstr("Zeroing scale...")
        hx711.tare()  # Zero (tare) the scale
        time.sleep(1)  # Give time for taring
        # lcd.clear()
    
    # Read weight and display
    weight_raw = hx711.get_value()
    weight_grams = weight_raw / scale_factor
    weight_grams_int = int(weight_grams)

    # lcd.clear()
    # lcd.putstr(f"Weight: {weight_grams_int} g")
    time.sleep(1)
