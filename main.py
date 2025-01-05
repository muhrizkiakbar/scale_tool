import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Pin configuration for HX711
DT_PIN = 5
SCK_PIN = 6

# Setup GPIO
hx711 = HX711(DT_PIN, SCK_PIN)

# Function to read the raw data from the HX711
def read_weight(num_samples=10):
    weights = []
    for _ in range(num_samples):
        weight = hx711.get_weight(5)  # Take a single reading with 5 readings averaged internally
        weights.append(weight)
        time.sleep(0.1)
    # Return the average weight
    return sum(weights) / len(weights)

# Calibration function
def calibrate():
    print("Place a known weight on the scale.")
    print("After placing the weight, press Enter to start calibration.")
    input("Press Enter to continue...")

    # Take several measurements and find the mean
    measurements = []
    for i in range(10):
        weight = hx711.get_weight(5)  # Average 5 readings
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
    # Tare the scale (set zero)
    hx711.tare()
    print("Taring complete. Now calibrate the scale.")
    
    # Calibrate the scale
    calibrate()
    
    # Continuously print weight readings
    while True:
        weight = read_weight()
        print(f"Weight: {weight:.2f} grams")
        time.sleep(1)

