import imp
import RPi.GPIO as GPIO
import smbus
import requests
import json
import time
from time import sleep

try:

    LEDVal = 0
    LEDValB = 0
    LEDSecondVal = 0
    LEDSecondValB = 0

    bus = smbus.SMBus(1)

    # GND,GND,GND
    DEVICE = 0x20

    # GND, GND, 3.3V
    SECONDDEVICE = 0x21

    IODIRA = 0x00
    IODIRB = 0x01

    OLATA = 0x14
    OLATB = 0x15

    GPIOA = 0x12
    GPIOB = 0x13

    bus.write_byte_data(DEVICE, IODIRA, 0x0)
    bus.write_byte_data(DEVICE, IODIRA, 0)
    bus.write_byte_data(DEVICE, OLATA, 0)

    bus.write_byte_data(DEVICE, IODIRB, 0x0)
    bus.write_byte_data(DEVICE, IODIRB, 0)
    bus.write_byte_data(DEVICE, OLATB, 0)

    bus.write_byte_data(SECONDDEVICE, IODIRA, 0x0)
    bus.write_byte_data(SECONDDEVICE, IODIRA, 0)
    bus.write_byte_data(SECONDDEVICE, OLATA, 0)

    bus.write_byte_data(SECONDDEVICE, IODIRB, 0x0)
    bus.write_byte_data(SECONDDEVICE, IODIRB, 0)
    bus.write_byte_data(SECONDDEVICE, OLATB, 0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIOList = [4, 17, 27, 18, 23, 24, 22, 25, 8, 7, 5, 6, 13, 19, 26, 16, 20, 21]

    for i in GPIOList:
        GPIO.setup(i, GPIO.OUT)

    def getLineStatus():
        j = requests.get('https://api.tfl.gov.uk/Line/Mode/tube%2Cdlr/Status')
        if (j is None or j == []):
            print("Empty or null JSON response")
            bus.write_byte_data(DEVICE, OLATA, 0)
            exit
        return j.json()

    class line(object):

        def __init__(self, name, lineSeverity, redPin, greenPin, bluePin):
            self.name = name
            self.lineSeverity = lineSeverity
            self.redPin = redPin
            self.greenPin = greenPin

    Bakerloo = line("Bakerloo", 0, 4, 17, 27)
    Central = line("Central", 0, 18, 23, 24)
    Circle = line("Circle", 0, 22, 25, 8)
    District = line("District", 0, 7, 5, 6)
    HammersmithCity = line("Hammersmith & City", 0, 13, 19 26)
    Jubilee = line("Jubilee", 0, 16, 20, 21)

    Victoria = line("Victoria", 0, 1, 2, 4)
    WaterlooCity = line("Waterloo & City", 0, 8, 16, 32)
    
    Metropolitan = line("Metropolitan", 0, 1, 2, 4)
    Northern = line("Northern", 0, 8, 16, 32)

    Piccadilly = line("Piccadilly", 0, 4, 2, 1)
    
    DLR = line("DLR", 0, 2, 4, 1)

    lineList = [Bakerloo, Central, Circle, District, HammersmithCity, Jubilee]

    MCPListA = [Victoria, WaterlooCity]
    MCPListB = [Metropolitan, Northern]
    MCPSecondList = [Piccadilly]
    MCPSecondListB = [DLR]

    while True:
        result = getLineStatus()
        for val in result:
            for r in lineList:
                if val['name'] == r.name:
                    for severity in val['lineStatuses']:
                        r.lineSeverity = severity['statusSeverity']
                        if r.lineSeverity == 10:
                            GPIO.output(r.greenPin, GPIO.HIGH)
                            GPIO.output(r.redPin, GPIO.LOW)
                            print(r.name + "'s LED is green")
                        elif r.lineSeverity <= 9 and r.lineSeverity >= 5:
                            GPIO.output(r.greenPin, GPIO.HIGH)
                            GPIO.output(r.redPin, GPIO.HIGH)
                            print(r.name + "'s LED is red and green")
                        elif r.lineSeverity == 20:
                            GPIO.output(r.greenPin, GPIO.LOW)
                            GPIO.output(r.redPin, GPIO.LOW)
                            print(r.name + "'s LED is off")
                        else:
                            GPIO.output(r.greenPin, GPIO.LOW)
                            GPIO.output(r.redPin, GPIO.HIGH)
                            print(r.name + "'s LED is red")
            for l in MCPListA:
                if val['name'] == l.name:
                    for severity in val['lineStatuses']:
                        l.lineSeverity = severity['statusSeverity']
                        if l.lineSeverity == 10:
                            LEDVal += l.greenPin
                            print(l.name + "'s LED is green")
                        elif l.lineSeverity <= 9 and l.lineSeverity >= 5:
                            LEDVal += l.greenPin
                            LEDVal += l.redPin
                            print(l.name + "'s LED is red and green")
                        elif l.lineSeverity == 20:
                            LEDVal += l.redPin
                            print(l.name + "'s LED is red")
            for l in MCPListB:
                if val['name'] == l.name:
                    for severity in val['lineStatuses']:
                        l.lineSeverity = severity['statusSeverity']
                        if l.lineSeverity == 10:
                            LEDValB += l.greenPin
                            print(l.name + "'s LED is green")
                        elif l.lineSeverity <= 9 and l.lineSeverity >= 5:
                            LEDValB += l.greenPin
                            LEDValB += l.redPin
                            print(l.name + "'s LED is red and green")
                        elif l.lineSeverity == 20:
                            LEDValB += l.redPin
                            print(l.name + "'s LED is red")
            for s in MCPSecondList:
                if val['name'] == s.name:
                    for severity in val['lineStatuses']:
                        s.lineSeverity = severity['statusSeverity']
                        if s.lineSeverity == 10:
                            LEDSecondVal += s.greenPin
                            print(s.name + "'s LED is green")
                        elif s.lineSeverity <= 9 and s.lineSeverity >= 5:
                            LEDSecondVal += s.greenPin
                            LEDSecondVal += s.redPin
                            print(s.name + "'s LED is red and green")
                        elif s.lineSeverity == 20:
                            LEDSecondVal += s.redPin
                            print(s.name + "'s LED is red")
            for s in MCPSecondListB:
                if val['name'] == s.name:
                    for severity in val['lineStatuses']:
                        s.lineSeverity = severity['statusSeverity']
                        if s.lineSeverity == 10:
                            LEDSecondValB += s.greenPin
                            print(s.name + "'s LED is green")
                        elif s.lineSeverity <= 9 and s.lineSeverity >= 5:
                            LEDSecondValB += s.greenPin
                            LEDSecondValB += s.redPin
                            print(s.name + "'s LED is red and green")
                        elif s.lineSeverity == 20:
                            LEDSecondValB += s.redPin
                            print(s.name + "'s LED is red")

        bus.write_byte_data(DEVICE, OLATA, LEDVal)
        bus.write_byte_data(DEVICE, OLATB, LEDValB)
        bus.write_byte_data(SECONDDEVICE, OLATA, LEDSecondVal)
        bus.write_byte_data(SECONDDEVICE, OLATB, LEDSecondValB)
        time.sleep(300)

except BaseException:
    e = sys.exc_info()[0]
    print("<p>Error: %s</p>" % e)

finally:
    GPIO.cleanup()
    bus.write_byte_data(DEVICE, OLATA, 0)
    bus.write_byte_data(SECONDDEVICE, OLATB, 0)
    print("Execution finished")
