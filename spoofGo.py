import serial
import time


def checksum(message):
    b0 = 0
    b1 = 0
    for i in range(0, len(message)):
        b0 += int(message[i])
        b1 += b0
    return bytes([b0 % 256, b1 % 256])


def createMessage(message):
    message = bytes([0x02]) + message
    check = checksum(message)
    message = message + check + bytes([0x03])
    return message

# look for ttyUSB in Linux (ls /dev/tty\*)
# with serial.Serial(port="/dev/ttyUSB1", baudrate = 9600, timeout = 60) as tester:
# Use COMx in windows
# with serial.Serial(port="COM7", baudrate = 9600, timeout = 60) as tester:

    # read sync char
    print("waiting for sync char...")
    readback = tester.read(1)

    if len(readback) and readback[0] == 0x55:
        print("sync char received")
        print([hex(b) for b in readback])

        handshakeRequest = createMessage(bytes([0x1, 0]))
        print("sending handshake request")
        print([hex(b) for b in handshakeRequest])
        tester.write(handshakeRequest)

        print("waiting for handshake response...")
        readback = tester.read(10)
        print([hex(b) for b in readback])

        if len(readback) == 10 and readback[1] == 0x81:
            print("handshake response received")

            while (1):
                print("waiting for status data...")
                readback = tester.read(12)
                print([hex(b) for b in readback])

                if len(readback) == 12 and readback[1] == 0x80:
                    print("status data received")
                    statusDataID = readback[3] + (readback[4] << 8)
                    dataValue = readback[5] + (readback[6] << 8)

                    print("status data id: " + str(statusDataID) +
                          ", value: " + str(dataValue))
                    ackMessage = createMessage(bytes([0x2, 0x0]))
                    print("sending ack")
                    print([hex(b) for b in ackMessage])
                    tester.write(ackMessage)
                    break
