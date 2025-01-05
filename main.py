import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Pin configuration for HX711
DT_PIN = 5
SCK_PIN = 6

# Setup GPIO
GPIO.setmode(GPIO.BCM)
hx711 = HX711(DT_PIN, SCK_PIN)

# Function to read the raw data from the HX711
def read_weight():
    try:
        weight = hx711.get_weight_mean(20)  # Average 20 readings
        print("Raw weight:", weight)
        return weight
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()

# Calibration function
def calibrate():
    print("Place a known weight on the scale.")
    print("After placing the weight, press Enter to start calibration.")
    input("Press Enter to continue...")

    # Take several measurements and find the mean
    measurements = []
    for i in range(10):
        weight = hx711.get_weight_mean(10)
        measurements.append(weight)
        time.sleep(0.1)

    # Compute the mean weight
    mean_weight = sum(measurements) / len(measurements)
    print(f"Mean reading with no weight: {mean_weight}")
    
    print("Now, enter the known weight in grams that you have placed on the scale.")
    known_weight = float(input("Enter known weight (grams): "))
    
    # Calculate the scale factor (calibration factor)
    calibration_factor = known_weight / mean_weight
    print(f"Calibration factor: {calibration_factor}")
    
    # Set the calibration factor
    hx711.set_scale(calibration_factor)

    print("Calibration complete.")

# Main program
if __name__ == "__main__":
    # Calibrate the scale
    calibrate()
    
    # Continuously print weight readings
    while True:
        weight = read_weight()
        print(f"Weight: {weight:.2f} grams")
        time.sleep(1)

