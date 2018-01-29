import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)

DEVICE = 0x20
IODIRA = 0x00
OLATA = 0x14
GPIOA = 0x12

bus.write_byte_data(DEVICE, IODIRA, 0x0)

bus.write_byte_data(DEVICE, IODIRA, 0)
bus.write_byte_data(DEVICE, OLATA, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Bakerloo
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

# Central
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

# Circle
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# District
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

#Hammersmith & City
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

# Jubilee
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Metropolitan
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# Northern
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Piccadilly
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

###########

# Bakerloo
GPIO.output(4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)

# Central
GPIO.output(27, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

# Circle
GPIO.output(18, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

# District
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)

#Hammersmith & City
GPIO.output(8, GPIO.LOW)
GPIO.output(7, GPIO.LOW)

# Jubilee
GPIO.output(12, GPIO.LOW)
GPIO.output(16, GPIO.LOW)

# Metropolitan
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)

# Northern
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)

# Piccadilly
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
