import imp
import RPi.GPIO as GPIO
import smbus
import requests
import json
import time
from time import sleep

try:

    LEDVal = 0

    bus = smbus.SMBus(1)

    DEVICE = 0x20
    IODIRA = 0x00
    OLATA = 0x14
    GPIOA = 0x12

    bus.write_byte_data(DEVICE,IODIRA,0x0)

    bus.write_byte_data(DEVICE,IODIRA,0)
    bus.write_byte_data(DEVICE,OLATA,0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #Bakerloo
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)

    #Central
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    #Circle
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)

    #District
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    #Hammersmith & City
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)

    #Jubilee
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)

    #Metropolitan
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    #Northern
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)

    #Piccadilly
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)

    def getLineStatus():
        j = requests.get('https://api.tfl.gov.uk/Line/Mode/tube%2Cdlr/Status')
        if (j is None or j == []):
            print("Empty or null JSON response")
            bus.write_byte_data(DEVICE, OLATA, 64)
            exit
        return j.json()
        
    class line(object):

        def __init__(self, name, lineSeverity, redPin, greenPin):
            self.name = name
            self.lineSeverity = lineSeverity
            self.redPin = redPin
            self.greenPin = greenPin

    Bakerloo = line("Bakerloo", 0, 4, 17)
    Central = line("Central", 0, 27, 22)
    Circle = line("Circle", 0, 18, 23)
    District = line("District", 0, 24, 25)
    HammersmithCity = line("Hammersmith & City", 0, 8, 7)
    Jubilee = line("Jubilee", 0, 12, 16)
    Metropolitan = line("Metropolitan", 0, 20, 21)
    Northern = line("Northern", 0, 5, 6)
    Piccadilly = line("Piccadilly", 0, 13, 19)

    Victoria = line("Victoria", 0, 1, 2)
    WaterlooCity = line("Waterloo & City", 0, 4, 8)
    DLR = line("DLR", 0, 16, 32)

    lineList = []
    MCPList = []

    lineList.append(Bakerloo)
    lineList.append(Central)
    lineList.append(Circle)
    lineList.append(District)
    lineList.append(HammersmithCity)
    lineList.append(Jubilee)
    lineList.append(Metropolitan)
    lineList.append(Northern)
    lineList.append(Piccadilly)

    MCPList.append(Victoria)
    MCPList.append(WaterlooCity)
    MCPList.append(DLR)

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
            for l in MCPList:
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

        LEDVal += 128
        bus.write_byte_data(DEVICE, OLATA, LEDVal)
        time.sleep(300)

except:
    e = sys.exc_info()[0]
    print( "<p>Error: %s</p>" % e )
    bus.write_byte_data(DEVICE, OLATA, 64)

finally:
    print("Execution finished")

