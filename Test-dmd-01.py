"""
A test script for controlling the DLP® LightCrafter™ DM365 using the dm365 module.
"""

import numpy as np
import binascii
import math
import time
import dm365
import os

# Initialize the dm365 object
dir = os.path.dirname(__file__)
dmd = dm365.dm365()

# Connect to the DM365 device
dmd.connect()

# Retrieve and print the current display mode
dmd.getDisplayMode()

# Retrieve and print the revision information
dmd.getRevision()

# Set the display mode to Static Image Mode
dmd.setModeToStaticImage()

# Display a static image
dmd.displayStaticImage('pattern_8_07.bmp')
time.sleep(10)

# Set the display mode to Internal Test Pattern Mode
dmd.setModeToInternalTestPattern()

# Display internal test patterns
dmd.displayInternalTestPattern(0)
time.sleep(10)
dmd.displayInternalTestPattern(13)
time.sleep(10)

# Close the connection to the DM365 device
dmd.close()
