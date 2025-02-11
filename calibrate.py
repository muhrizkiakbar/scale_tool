import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Pin setup
DT_PIN = 5  # HX711 DT
SCK_PIN = 6  # HX711 SCK

# Known weight for calibration (in grams)
KNOWN_WEIGHT = 200  # Set this to a known weight in grams (e.g., 500g)

# HX711 setup

# Set the number of readings you want to average
READINGS = 10
hx = HX711(5,6)

hx.reset()
hx.tare()  # Tare the scale

def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()

def calibrate(hx):
    # Get the raw data for the known weight
    print(f"Place {KNOWN_WEIGHT}g on the scale.")
    input("Press Enter when ready...")
    
    # Read raw data multiple times and average
    raw_data = [hx.get_raw_data_mean(READINGS) for _ in range(READINGS)]
    average_raw_value = sum(raw_data) / len(raw_data)
    
    print(f"Raw Value for {KNOWN_WEIGHT}g: {average_raw_value}")
    
    # Calculate the calibration factor (reference_unit)
    reference_unit = average_raw_value / KNOWN_WEIGHT
    print(f"Calculated reference_unit: {reference_unit}")
    
    return reference_unit

while True:
    try:
        setup(hx)
    
        # Find the reference_unit for the known weight
        reference_unit = calibrate(hx)
        
        # Set the reference_unit
        hx.set_reference_unit(reference_unit)
        
        print(f"Set reference_unit to: {reference_unit}")
        
        # Now you can start using the scale
        while True:
            weight = hx.get_weight(10) / reference_unit
            print(f"Weight: {weight:.2f} grams")
            time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

