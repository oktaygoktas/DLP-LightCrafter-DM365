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

class dm365:
    """A class to manage connections and data transmission with the DLP LightCrafter DM365."""

    def __init__(self):
        """Initialize the socket connection."""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, testFlag=0):
        """
        Connect to the DM365 device.

        :param testFlag: Set to 1 to connect to a local host for testing.
        """
        if testFlag == 1:
            HOST = '127.0.0.1'  # For test purposes
            PORT = 50007  # Start dmd_TestServer.py for test mode
        else:
            HOST = '192.168.1.100'  # DM365 module
            PORT = 21845
        print(f'Connecting to {HOST} and {PORT}')

        resp = self.s.connect_ex((HOST, PORT))
        if resp == 0:
            print(f'Connected to {HOST} and {PORT}')
        else:
            print(f'Connection Failed to {HOST} and {PORT}')
            quit()

    def close(self):
        """Close the socket connection."""
        self.s.close()
        return 0

    def sendData(self, packet):
        """
        Send data to the DM365 device.

        :param packet: The data packet to send.
        :return: The response from the device.
        """
        self.s.sendall(packet)
        ans = self.s.recv(1024)
        if ans[0] == 0:
            print('The device returned LightCrafter System Busy Packet: Try again')
        if ans[0] == 1:
            print(self.checkError(int(ans[6])))
        return ans

    def checkError(self, errorByte):
        """
        Check for errors based on the error byte.

        :param errorByte: The error byte received from the device.
        :return: A string describing the error.
        """
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
        }.get(errorByte, 'Unknown Error')

    def getDisplayMode(self):
        """
        Get the current display mode of the DM365 device.

        :return: The response from the device indicating the display mode.
        """
        print('Reading display mode.')
        currentPacket = b'\x04\x01\x01\x00\x00\x00\x06'
        ans = self.sendData(currentPacket)
        if ans[6] == 0:
            print('Dmd is in Static Image Mode')
        elif ans[6] == 1:
            print('Dmd is in Internal Test Pattern Mode')
        elif ans[6] == 2:
            print('Dmd is in HDMI Video Input Mode')
        elif ans[6] == 3:
            print('Dmd is in Reserved- Not used Mode')
        elif ans[6] == 4:
            print('Dmd is in Pattern Sequence Display Mode')
        else:
            print('Something is wrong: Returned data is out of range Mode')
        return ans

    def getRevision(self):
        """
        Get the revision information of the DM365 device.

        :return: The response from the device with revision details.
        """
        print('Reading revision')
        currentPacket = b'\x04\x01\x00\x00\x01\x00\x00\x06'
        ans = self.sendData(currentPacket)
        self.printSrting(ans[6:len(ans) - 1])
        return ans

    def printSrting(self, ans):
        """Print a string decoded from the device response."""
        msg = ans.decode('utf-8')
        print(msg)

    def setModeToStaticImage(self):
        """
        Set the display mode to Static Image Mode.

        :return: The response from the device.
        """
        print('Set mode to StaticImage')
        currentPacket = b'\x02\x01\x01\x00\x01\x00\x00\x05'
        ans = self.sendData(currentPacket)
        return ans

    def displayStaticImage(self, fileName):
        """
        Display a static image on the DM365 device.

        :param fileName: The file name of the BMP image to display.
        :return: The response from the device.
        """
        print('Display Static Image')
        self.setModeToStaticImage()
        header = bytearray(b'\x02\x01\x05\x00\x00\x00')
        imData = self.readBMPImage(fileName)
        ans = self.makeAndSendPacket(header, imData)
        return ans

    def setModeToInternalTestPattern(self):
        """
        Set the display mode to Internal Test Pattern Mode.

        :return: The response from the device.
        """
        print('Set Mode To Internal TestPattern')
        currentPacket = b'\x02\x01\x01\x00\x01\x00\x01\x06'
        ans = self.sendData(currentPacket)
        return ans

    def displayInternalTestPattern(self, n):
        """
        Display an internal test pattern on the DM365 device.

        :param n: The pattern number to display.
        :return: The response from the device.
        """
        print('Display Internal TestPattern')
        self.setModeToInternalTestPattern()
        currentPacket = bytearray(b'\x02\x01\x03\x00\x01\x00')
        currentPacket.append(n)
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans

    def appendCheckSum(self, packet):
        """
        Append a checksum to the packet.

        :param packet: The packet to append the checksum to.
        :return: The packet with the checksum appended.
        """
        sumPacket = sum(packet)
        checksum = bytes([sumPacket % 256])
        packet.append(checksum[0])
        return packet

    def getpayloadLength(self, payload):
        """
        Get the payload length in LSB and MSB.

        :param payload: The payload to calculate the length for.
        :return: A list containing the LSB and MSB of the payload length.
        """
        lenpayloadMSB = int(math.floor(len(payload) / 256))
        lenpayloadLSB = int(len(payload) % 256)
        return [lenpayloadLSB, lenpayloadMSB]

    def printData(self, data, length=0):
        """
        Print data with a specified length.

        :param data: The data to print.
        :param length: The length of data to print. If 0, print all data.
        """
        if length > 0:
            out = [data[i] for i in range(length)]
        elif length < 0:
            out = [data[-(i + 1)] for i in range(abs(length))]
        else:
            out = [data[i] for i in range(len(data))]
        print(out)

    def readBMPImage(self, bmpFile):
        """
        Read a BMP image file.

        :param bmpFile: The BMP file to read.
        :return: The image data as a bytearray.
        """
        with open(bmpFile, 'rb') as f:
            imdata = bytearray(f.read())
            return imdata

    def makeAndSendPacket(self, header, imData):
        """
        Create and send a packet with image data.

        :param header: The header for the packet.
        :param imData: The image data to include in the packet.
        :return: The response from the device.
        """
        MAX_PACKET_LENGTH = 512
        print('Loading Image')
        blockSize = math.ceil(float(len(imData)) / float(MAX_PACKET_LENGTH))
        print(f'blockSize = {blockSize}')

        for i in np.arange(blockSize):
            if i == 0:
                payload = imData[0:MAX_PACKET_LENGTH]
                header[3] = int(1)
                print('Sending First packet')
            else:
                if i == blockSize - 1:
                    payload = imData[i * MAX_PACKET_LENGTH:]
                    header[3] = int(3)
                    print('Sending last packet')
                else:
                    payload = imData[i * MAX_PACKET_LENGTH:(i + 1) * MAX_PACKET_LENGTH]
                    header[3] = int(2)

            [lenpayloadLSB, lenpayloadMSB] = self.getpayloadLength(payload)
            header[4] = lenpayloadLSB
            header[5] = lenpayloadMSB

            currentPacket = bytearray(header)
            currentPacket.extend(payload)
            currentPacket = self.appendCheckSum(currentPacket)
            self.printData(currentPacket)

            ans = self.sendData(currentPacket)
        return ans

    def setDisplaySetting(self, flip_X=0, flip_Y=0, rotate=0):
        """
        Set the display settings for the DM365 device.

        :param flip_X: Flip the display horizontally.
        :param flip_Y: Flip the display vertically.
        :param rotate: Rotate the display.
        :return: The response from the device.
        """
        print(f'Setting The Display Setting flip_X={flip_X}, flip_Y={flip_Y}, rotate={rotate}')
        payload = bytearray([int(flip_X), int(flip_Y), int(rotate)])
        header = bytearray(b'\x02\x01\x07\x00\x03\x00')
        currentPacket = header + payload
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans

    def getDisplaySetting(self):
        """
        Get the current display settings of the DM365 device.

        :return: The response from the device with display settings.
        """
        print('Getting The Display Setting')
        header = bytearray(b'\x04\x01\x07\x00\x00\x00')
        currentPacket = self.appendCheckSum(header)
        ans = self.sendData(currentPacket)
        flip_X = ans[6]
        flip_Y = ans[7]
        rotate = ans[8]
        print(f'The Display Setting are flip_X={flip_X}, flip_Y={flip_Y}, rotate={rotate}')
        return ans

    def setModeToPatternSequenceDisplay(self):
        """
        Set the display mode to Pattern Sequence Mode.

        :return: The response from the device.
        """
        currentPacket = b'\x02\x01\x01\x00\x01\x00\x04\x09'
        ans = self.sendData(currentPacket)
        return ans

    def setPatternSeqSetting(self, bitDepth=8, numOfPatters=2, Mode=0, InputTriggerType=1, InputTriggerDelay=0, AutoTriggerPeriod=3333334, ExposureTime=3333334, LEDSelect=1):
        """
        Set the pattern sequence settings for the DM365 device.

        :param bitDepth: The bit depth for the pattern.
        :param numOfPatters: The number of patterns.
        :param Mode: The mode for the pattern sequence.
        :param InputTriggerType: The input trigger type.
        :param InputTriggerDelay: The input trigger delay.
        :param AutoTriggerPeriod: The auto trigger period.
        :param ExposureTime: The exposure time.
        :param LEDSelect: The LED selection.
        :return: The response from the device.
        """
        print('Setting pattern settings')
        payload = bytearray([
            bitDepth, numOfPatters, Mode, int(InputTriggerType),
            InputTriggerDelay & 0xff, (InputTriggerDelay >> 8) & 0xff,
            (InputTriggerDelay >> 16) & 0xff, (InputTriggerDelay >> 24) & 0xff,
            AutoTriggerPeriod & 0xff, (AutoTriggerPeriod >> 8) & 0xff,
            (AutoTriggerPeriod >> 16) & 0xff, (AutoTriggerPeriod >> 24) & 0xff,
            ExposureTime & 0xff, (ExposureTime >> 8) & 0xff,
            (ExposureTime >> 16) & 0xff, (ExposureTime >> 24) & 0xff,
            LEDSelect
        ])
        header = bytearray(b'\x02\x04\x00\x00')
        [lenpayloadLSB, lenpayloadMSB] = self.getpayloadLength(payload)
        header.extend([lenpayloadLSB, lenpayloadMSB])

        currentPacket = header + payload
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans

    def PatternDefinition(self, n, fileName):
        """
        Define and send a pattern to the DM365 device.

        :param n: The pattern number.
        :param fileName: The file name of the BMP image for the pattern.
        :return: The response from the device.
        """
        self.setModeToPatternSequenceDisplay()
        print(f'Defining and sending the {n}th pattern data')
        imData = bytearray([int(n)]) + self.readBMPImage(fileName)
        header = bytearray(b'\x02\x04\x01\x00\x00\x00')
        ans = self.makeAndSendPacket(header, imData)
        return ans

    def startPatternSequence(self):
        """
        Start the pattern sequence on the DM365 device.

        :return: The response from the device.
        """
        print('Starting Pattern Sequence')
        currentPacket = bytearray(b'\x02\x04\x02\x00\x01\x00\x01')
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans

    def stoptPatternSequence(self):
        """
        Stop the pattern sequence on the DM365 device.

        :return: The response from the device.
        """
        print('Stopping Pattern Sequence')
        currentPacket = bytearray(b'\x02\x04\x02\x00\x01\x00\x00')
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans

    def displayPatterns(self, n1, n2):
        """
        Display patterns on the DM365 device.

        :param n1: The starting pattern number.
        :param n2: The ending pattern number.
        :return: The response from the device.
        """
        payload = bytearray([int(n1), int(n2)])
        header = bytearray(b'\x02\x04\x05\x00\x02\x00')
        currentPacket = header + payload
        currentPacket = self.appendCheckSum(currentPacket)
        ans = self.sendData(currentPacket)
        return ans
