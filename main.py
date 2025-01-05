import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)  # Adjust for your OLED resolution (e.g., 128x32)

# Clear the display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw text
font = ImageFont.load_default()
draw.text((0, 0), "Hello, OLED!", font=font, fill=255)

# Display image
oled.image(image)
oled.show()

# Wait
time.sleep(5)

