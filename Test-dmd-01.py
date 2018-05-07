# A test code for controlling the DLP® LightCrafter™ DM365. 
import numpy as np
import binascii
import math
import time
import dm365
import os
dir = os.path.dirname(__file__)  
dmd = dm365.dm365()
#####################################################


dmd.connect() #Do not comment this line

# ######### ********************   ##################################
# ####### ********************   ##################################

dmd.getDisplayMode()


######## ********************   ##################################

dmd.getRevision()

####### ********************   ##################################
dmd.setModeToStaticImage()


# ######### ********************   ##################################

dmd.displayStaticImage('pattern_8_07.bmp')

time.sleep(10)



# # # ######### ********************   ##################################
# # ######### ********************   ##################################
dmd.setModeToInternalTestPattern()


# # ######### ********************   ##################################

# # #Give an integer between 0 to 14 as argument
dmd.displayInternalTestPattern( 0)
time.sleep(10)
# # #Give an integer between 0 to 14 as argument
dmd.displayInternalTestPattern( 13)

time.sleep(10)

## UNCOMMENT FOR TRYING
# # ######### ***
# # # ######### ********************   ##################################
# # ######### ********************   ##################################

# # dmd.getDisplaySetting()
# # time.sleep(5)
# # dmd.setDisplaySetting( 0, 0, 0)
# # dmd.getDisplaySetting()
# # time.sleep(1)


# file = os.path.join(dir, 'Images\PatSeqImages\pattern_8_07.bmp')
# dmd.displayStaticImage(file)

# # time.sleep(5)
# # dmd.setDisplaySetting( 0, 0, 0)
# # time.sleep(5)
# # dmd.setDisplaySetting( 0, 1, 0)
# # time.sleep(5)
# # dmd.setDisplaySetting( 1, 1, 0)
# # time.sleep(5)
# # dmd.setDisplaySetting( 1, 0, 0)
# # time.sleep(5)
# # dmd.setDisplaySetting( 0, 0, 0)
# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_8_07.bmp')
# # dmd.setDisplaySetting( 0, 0, 0)
# # dmd.displayStaticImage(file)
# # time.sleep(5)
# # # ######### ********************   ##################################
# # # ######### ********************   ##################################
# # dmd.setModeToPatternSequenceDisplay()

# # dmd.setPatternSeqSetting()# For default values of ( bitDepth=8, numOfPatters=5, Mode =0, InputTriggerType = 1, InputTriggerDelay = 0, AutoTriggerPeriod = 3333334, ExposureTime = 3333334, LEDSelect =1  )

# # # or give as you like. time to be given  in microseconds 
# # dmd.setPatternSeqSetting( bitDepth=8, numOfPatters=5, Mode =0, InputTriggerType = 1, InputTriggerDelay = 0, AutoTriggerPeriod = 3333334, ExposureTime = 3333334, LEDSelect =1  )
# # dmd.setModeToPatternSequenceDisplay()
# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_1_00.bmp') 

# # dmd.PatternDefinition( 0, file)  # n is the pattern number to be loaded

# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_1_01.bmp')

# # dmd.PatternDefinition( 1, file)

# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_1_02.bmp')

# # dmd.PatternDefinition( 2, file)

# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_1_03.bmp')

# # dmd.PatternDefinition( 3, file)

# # file = os.path.join(dir, 'Images\PatSeqImages\pattern_1_04.bmp')

# # dmd.PatternDefinition( 4, file)

# # dmd.startPatternSequence()
# # time.sleep(30)


# # dmd.stoptPatternSequence()


# # ######### ********************   ##################################
# # ######### ********************   ##################################
# # ######### ********************   ##################################
# ######### ********************   ##################################
dmd.close()
