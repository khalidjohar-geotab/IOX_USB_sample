import serial
import time

def checksum(message):
 b0 = 0
 b1 = 0

 for i in range(0, len(message)):
  b0 += int(message[i])
  b1 += b0
 return bytes([b0%256, b1%256])

def createMessage(message):
 message = bytes([0x02]) + message
 check = checksum(message)
 message = message + check + bytes([0x03])
 return message

# look for ttyUSB in Linux (ls /dev/tty\*)
# with serial.Serial(port="/dev/ttyUSB0", baudrate = 9600, timeout=1) as tester:
# Use COMx in windows
# with serial.Serial(port="COM4", baudrate = 9600, timeout = 10) as tester:

# send sync char
 print("sending sync char")
 print("['0x55']")
 tester.write(bytes([0x55]))
 print("waiting for handshake request...")
 readback = tester.read(6)

 print([hex(b) for b in readback])

 if len(readback) == 6 and readback[1] == 1:
  print("handshake request received")
  #send the handshake response
  deviceID = 4208 #4208 is a test Device ID
  handshakeResponse = createMessage(bytes([0x81, 4, deviceID%256, (deviceID >> 8)%256, 0, 0]))
  print("sending handshake response")
  print([hex(b) for b in handshakeResponse])
  tester.write(handshakeResponse)
  time.sleep(1)
  # send some status data
  statusDataID = 35349 #status data id of "Test engine measurement / fake data"
  dataValue = 200 #data value of 10 will show on MyGeotab (because of the conversion factor of 0.1 and offset of -10)
  dataMessage = createMessage(bytes([0x80, 6, statusDataID%256, (statusDataID >> 8)%256, dataValue%256, (dataValue >> 8)%256, 0, 0]))

  print("sending status data")
  print([hex(b) for b in dataMessage])
  tester.write(dataMessage)
  print("waiting for data ACK...")
  readback = tester.read(6)

  print([hex(b) for b in readback])

  if len(readback) == 6 and readback[1] == 2:
   print("data ACK received")
 Else:
  print("invalid response")
