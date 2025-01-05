import sys
import time
import RPi.GPIO as GPIO
from hx711 import HX711  # Import your HX711 class

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
zero_button = 17  # Change GPIO pin if needed
GPIO.setup(zero_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up as input with pull-up resistor

# Set up HX711
hx711 = HX711(5,6, gain=128)  # Adjust pins for HX711
hx711.set_reference_unit(-6459)
hx711.set_offset(2971992)

def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()


while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx711.get_value()
        print(val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
