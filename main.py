from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi
from luma.core.virtual import matrix
import time

# Initialize SPI
serial = spi(port=0, device=0, gpio=None)
device = max7219(serial, cascaded=4, block_orientation=90, rotate=0)
device.contrast(16)

# Display some text
virtual = matrix(device)
virtual.text = "HELLO"
time.sleep(5)

