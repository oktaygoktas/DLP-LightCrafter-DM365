""" A python module to send and receive data from DLP® LightCrafter™ DM365.
Written by Oktay Göktaş, University of Toronto, Department of Physics,
January 2018.   Free to use. The code is just a simple python solution to use dmd and  provided as is. 
Please use at your own risk. Your device might be different than the one used on this study.
The usage of the functions are given on the example file Test-dmd.py"""
import socket
import sys
import numpy as np
import binascii
import math

#####################################
#####################################
class dm365:
	def __init__(self):
		self.s =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, testFlag =0):
	    """ Connecting call it giving the argument 1 if you want to connect a  local host."""
	    
	    if (testFlag == 1):
	        HOST = '127.0.0.1'    # For test purposes to see if commands are being sent correctly         
	        PORT = 50007          #First Start dmd_TestServer.py for use on the test mode    
	    else: 
	        HOST = '192.168.1.100'   # dm365 module
	        PORT = 21845
	    print('Connecting to ' + str(HOST) + ' and ' + str(PORT))
	    
	    
	    
	    #resp = s.connect((HOST, PORT))
	    resp = self.s.connect_ex((HOST, PORT))
	    if (resp==0):
	        print('Connected ' + str(HOST) + ' and ' + str(PORT))
	        print(self.s)
	    else:
	        print('Connection Failed to ' + str(HOST) + ' and ' + str(PORT))
	        quit()

	##############################
	##############################
	def close(self):
	    #""" Closing Connection"""	    
	    #print(self.s)
	    
	    resp =  self.s.close()
	        
	    return 0
	##############################	      

	##############################
	##############################
	def sendData(self, packet):
	    #""" Sending Data"""	    
	    
	    resp = self.s.sendall(packet)
	    ans = self.s.recv(1024)
	    if (ans[0] == 0):
	        print('The device returned LightCrafter System Busy Packet: Try again')

	    if (ans[0] == 1):
	        print(self.checkError( int( ans[6] ) ))
	        
	    return ans
	##############################
	##########################
	##########################

	def checkError(errorByte):
		#"""Function for checkin errors"""	 
	    return {
	        1: 'Command execution failed with unknown error1',
	        2: 'Invalid command',
	        3: 'Invalid Parameter',
	        4: 'Out of memory resource',
	        5: 'Hardware device failure',
	        6: 'Hardware busy',
	        7: 'Not Initialized (any of the preconditions for the command is not met)',
	        8: 'Some object referred by the command is not found. For example, a solution name was not found',
	        9: 'Checksum Error.',
	        10: 'Packet format error due to insufficient or larger than expected payload size',
	        11: 'Command continuation error due to incorrect continuation flag',
	    }.get(errorByte, 'Uknown Error')   

	##############################
	##########################
	def getDisplayMode(self):
	    #""" Getting Display Mode""
	    
	    print('Reading display mode.  ')
	    currentPacket = b'\x04\x01\x01\x00\x00\x00\x06'
	    ans = self.sendData( currentPacket) 
	    if (ans[6] ==0):
	        print('Dmd is in Static Image Mode')
	    elif(ans[6] ==1):
	        print('Dmd is in Internal Test Pattern Mode')
	    elif(ans[6] ==2):
	        print('Dmd is in HDMI Video Input Mode')
	    elif(ans[6] ==3):
	        print('Dmd is in Reserved- Not used Mode')
	    elif(ans[6] ==4):
	        print('Dmd is in Pattern Sequence Display Mode')
	    else:
	        print('Something is wrong: Returned data is out of range Mode')
	    
	    return ans
	#######################
	def getRevision(self):
	    #""" Getting Revision"""
	    
	    # 0x00 – DM365 SW Revision
	    #  0x10 – FPGA Firmware Revision
	    # 0x20 – MSP430 SW Revision
	    print('Reading revision')
	    currentPacket = b'\x04\x01\x00\x00\x01\x00\x00\x06'
	    ans = self.sendData(currentPacket) 
	    self.printSrting(ans[6:len(ans)-1])
	    return ans
	######################
	##########################
	##########################
	def printSrting(ans):
	    msg = ans.decode('utf-8')
	    print(msg)
	    
	##########################
	#  Display Static Image   functions
	##########################
	def setModeToStaticImage(self):#Setting  the display mode to Static Image Mode
	    #""" Setting  the display mode to Static Image Mode"""
	    #For Static images 6th byte must be  0
	    print('Set mode to StaticImage')
	    currentPacket = b'\x02\x01\x01\x00\x01\x00\x00\x05'
	    ans = self.sendData(currentPacket) 
	    return ans

	##########################
	##########################
	def displayStaticImage(self,fileName):
		#""" Setting  the display mode to Static Image Mode"""
	    print('Display  Static Image') 
	    self.setModeToStaticImage()
	    imData = []
	    header =  []
	    header =  bytearray(b'\x02\x01\x05\x00\x00\x00')#The last byte is being changed in the makeAndSendPAcket func
	    imData = self.readBMPImage(fileName)#  'Square_wx80_wy250.bmp'
	    ans = self.makeAndSendPacket(header, imData)
	    return  ans
	##########################
	#   INTERNAL TEST PATTERN FUNC
	##########################
	def setModeToInternalTestPattern(self):#Setting  the display mode to Static Image Mode
	    #1 For Static images 6th byte 1
	    #
	    print('set Mode To Internal TestPattern') 
	    currentPacket = b'\x02\x01\x01\x00\x01\x00\x01\x06'
	    ans = self.sendData(currentPacket) 
	    return ans
	##########################
	##########################
	##########################
	##########################
	    
	def displayInternalTestPattern(self,n):
	    print('Display Internal TestPattern') 
	    #Give an integer between 0 to 14 as argument
	    # 0x0 - 14×8 Checkerboard (default)
	    # 0x01 - Solid black
	    # 0x02 - Solid white
	    # 0x03 - Solid green
	    # 0x04 - Solid blue
	    # 0x05 - Solid red
	    # 0x06 - Vertical lines (1-white, 7-black)
	    # 0x07 - Horizontal lines (1-white, 7-black)
	    # 0x08 - Vertical lines (1-white, 1-black)
	    # 0x09 - Horizontal lines (1-white, 1-black)
	    # 0x0A - Diagonal lines
	    # 0x0B - Vertical Gray Ramps
	    # 0x0C - Horizontal Gray Ramps
	    # 0x0D - ANSI 4×4 Checkerboard
	    self.setModeToInternalTestPattern()    ##Setting mode to internal test pattern
	    currentPacket = bytearray(b'\x02\x01\x03\x00\x01\x00')
	    currentPacket.append(n)   
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans
	###############################
	##### PACKET PREP FUNCTIONS
	###############################
	def appendCheckSum(self, packet):
	    #packet = bytearray(b'\x04\x01\x01\x00\x01\x00')
	    sumPacket = sum(packet)
	    print(sumPacket)
	    checksum = bytes([sumPacket % 256])
	    print(checksum)
	    packet.append(checksum[0])
	    return packet
	#########################
	##########################    
	def getpayloadLength(self, payload):
	    lenpayloadMSB = int(math.floor(len(payload)/256))
	    lenpayloadLSB = int(len(payload) % 256)
	    return [lenpayloadLSB, lenpayloadMSB]
	##########################
	##########################

	def printData(self, data, length=0):
	    if (length>0):
	        out = [data[i] for i in range(length)]
	    elif(length<0):
	        out = [data[-(i+1)] for i in range(abs(length))]
	    else:
	        out = [data[i] for i in range(len(data))]
	    print(out)

	##########################
	##########################
	def printSrting(self, ans):
	    msg = ans.decode('utf-8')
	    print(msg)

	#########################
	##########################

	def readBMPImage(self, bmpFile):
	    with open(bmpFile, 'rb') as f:
	        imdata =bytearray((f.read()))
	        return imdata




	##########################
	##########################

	def makeAndSendPacket(self, header, imData):
	    MAX_PACKET_LENGTH = 512 #Max 65535
	    payload = []
	    print('Loading Image')
	    currentPacket = []
	    blockSize = math.ceil(float(len(imData)) / float(MAX_PACKET_LENGTH))
	    print('blockSize = {}'.format(blockSize))


	    for i in np.arange(blockSize):

	        if(i==0):
	            payload = imData[0:MAX_PACKET_LENGTH]

	            header[3] = int(1)
	            print('Sending First  paket')
	            #self.printData(header)
	            #self.printData(payload)

	        else:
	            
	            if (i== blockSize-1):
	                payload = imData[i*MAX_PACKET_LENGTH:]

	                header[3] = int(3)
	                print('Sending last  paket')
	                #self.printData(header)
	                #self.printData(payload)
	            else:
	            	
	                payload = imData[i*MAX_PACKET_LENGTH:(i+1)*MAX_PACKET_LENGTH]

	                header[3] = int(2)


	        [lenpayloadLSB,lenpayloadMSB] =  self.getpayloadLength(payload)

	        

	        header[4] = lenpayloadLSB
	        header[5] =  lenpayloadMSB

	        currentPacket = bytearray(header)
	        currentPacket.extend(payload)
	        currentPacket = self.appendCheckSum(currentPacket)
	        self.printData(currentPacket)

	        ans = self.sendData(currentPacket) 
	    return ans
	##########################
	##########################   
	def setDisplaySetting(self, flip_X=0, flip_Y=0, rotate=0):
	    # Give arguments as one if you want actions
	    print('Setting The Display Setting  flip_X={} , flip_Y={},  rotate={}'.format(flip_X, flip_Y, rotate))
	    payload = bytearray([])
	    header =[]
	    currentPacket = []
	    header = bytearray(b'\x02\x01\x07\x00\x03\x00')
	    payload.append(int(flip_X))
	    payload.append(int(flip_Y))
	    payload.append(int(rotate))

	    currentPacket = header
	    currentPacket.extend(payload)   
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans

	##########################
	##########################   
	def getDisplaySetting(self):
	    # Give arguments as one if you want actions
	    print('Getting The Display Setting  ')
	    payload = bytearray([])
	    header =[]
	    currentPacket = []
	    header = bytearray(b'\x04\x01\x07\x00\x00\x00')

	    currentPacket = header
	    #currentPacket.extend(payload)   
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket)
	    flip_X = ans[6]
	    flip_Y = ans[7]
	    rotate = ans[8]
	    print('The Display Setting are  flip_X={} , flip_Y={},  rotate={}'.format(flip_X, flip_Y, rotate)) 
	    #self.printData(ans)
	    return ans
	##########  *****************************************************************
	##########  *****************************************************************
	##########   Commands for pattern sequence Display
	##########  ********** Display******************************************************
	##########  *****************************************************************
	#########################
	### Commands for pattern sequence    ####
	########################## 
	def setModeToPatternSequenceDisplay(self):
	    #""" Setting  the display mode to PatternSequence Mode"""
	    #
	    currentPacket = []
	    currentPacket = b'\x02\x01\x01\x00\x01\x00\x04\x09'
	    ans = self.sendData(currentPacket) 
	    return ans

	##########################
	########################## 
	def setPatternSeqSetting(self, bitDepth=8, numOfPatters=2, Mode =0, InputTriggerType = 1, InputTriggerDelay = 0, AutoTriggerPeriod = 3333334, ExposureTime = 3333334, LEDSelect =1  ):#Setting  the display mode to Static Image Mode
	    #This needs to be worked,LEDSelect =1, 
	    print('Setting  pattern settings ')
	    payload = bytearray([])
	    header = []
	    currentPacket = []
	    header = bytearray(b'\x02\x04\x00\x00')  # This might be b'\x02\x04\x00\x00' Because later in  versions changed!!!
	    payload.append(bitDepth)
	    payload.append(numOfPatters)
	    payload.append(Mode)
	    payload.append(int(InputTriggerType))
	    #
	    payload.append( InputTriggerDelay & 0xff )
	    payload.append( (InputTriggerDelay>>8) & 0xff )     
	    payload.append( (InputTriggerDelay>>16) & 0xff )
	    payload.append( (InputTriggerDelay>>24) & 0xff )
	   
	    # Putting  InputTriggerDelay in 4 bytes 
	    payload.append( AutoTriggerPeriod & 0xff )
	    payload.append( (AutoTriggerPeriod>>8) & 0xff )
	    payload.append( (AutoTriggerPeriod>>16) & 0xff )
	    payload.append( (AutoTriggerPeriod>>24) & 0xff )    
	    # Putting  InputTriggerDelay in 4 bytes 
	    payload.append( ExposureTime & 0xff )
	    payload.append( (ExposureTime>>8) & 0xff )
	    payload.append( (ExposureTime>>16) & 0xff )
	    payload.append( (ExposureTime>>24) & 0xff )   
	    payload.append( LEDSelect )  

	    [lenpayloadLSB,lenpayloadMSB] =  self.getpayloadLength(payload)
	    header.append(lenpayloadLSB)
	    header.append(lenpayloadMSB)


	    currentPacket = bytearray(header)
	    currentPacket.extend(payload)   
	    currentPacket = self.appendCheckSum(currentPacket)
	    #printData(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans
	    


	##########################
	##########################      
	def PatternDefinition(self, n, fileName):
	    # n is the pattern number to be loaded
	    self.setModeToPatternSequenceDisplay()
	    print('defining and sending the ' + str(n) +'th pattern data')
	    imData = []
	    imData = bytearray(imData)
	    imData.append(int(n)) # This is the pattern sequence number
	    header =  []
	    header =  bytearray(b'\x02\x04\x01\x00\x00\x00')#The last 3 bbytes(flag, LSB and MSB) is being changed in the makeAndSendPAcket func
	    imData.extend(self.readBMPImage(fileName) )#  'Square_wx80_wy250.bmp'
	    ans = self.makeAndSendPacket(header, imData)
	    return  ans
	##########################
	########################## 
	def startPatternSequence(self):#Starting Patter Sequence
	    #""" Starting Patter Sequence"""
	    print('Starting Patter Sequence') 
	    currentPacket = bytearray(b'\x02\x04\x02\x00\x01\x00\x01')
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans
	##########################
	########################## 
	def stoptPatternSequence(self):#Stopping Patter Sequence
	    #""" Stopping Patter Sequence"""
	    print('Stopping Patter Sequence') 
	    currentPacket = bytearray(b'\x02\x04\x02\x00\x01\x00\x00')
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans
	##########################
	##########################      
	def displayPatterns(self, n1, n2):
	    #This command (supported in DM365 firmware version 3.0 or greater) continuously displays the selected
	    #pattern sequence with the indicates exposure and trigger period settings
	    #Byte 0 - Byte 1 Pattern number. Range of values 1-1500
	    payload = bytearray([])
	    header = []
	    currentPacket = []
	    header = bytearray(b'\x02\x04\x05\x00\x02\x00')
	    payload.append(int(n1))
	    payload.append(int(n2))
	    currentPacket = header
	    currentPacket.extend(payload)
	    currentPacket = self.appendCheckSum(currentPacket)
	    ans = self.sendData(currentPacket) 
	    return ans
	##########################
	##########################


	##########################
	##########################