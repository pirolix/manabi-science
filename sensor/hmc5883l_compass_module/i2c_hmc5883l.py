#!/usr/bin/python
# -*- coding: utf-8 -*-
import smbus            # I2C を使う
import math
from time import sleep

### define #############################################################
DEV_ADDR = 0x1E         # device address
REG_CONFIG_A = 0x00	# config register A
REG_MODE = 0x02		# mode register
MAGNET_XOUT = 0x03	# data register X
MAGNET_YOUT = 0x05	# data register Y
MAGNET_ZOUT = 0x07	# data register Z

# 1byte read
def read_byte( addr ):
    return bus.read_byte_data( DEV_ADDR, addr )

# 2byte read
def read_word( addr ):
    high = read_byte( addr   )
    low  = read_byte( addr+1 )
    return (high << 8) + low

# Sensor data read
def read_word_sensor( addr ):
    val = read_word( addr )
    if( val < 0x8000 ):	# positive value
        return val
    else:		# negative value
        return val - 65536

### Main function ######################################################
bus = smbus.SMBus( 1 )
bus.write_byte_data( DEV_ADDR, REG_CONFIG_A, 0xe0 );
bus.write_byte_data( DEV_ADDR, REG_MODE, 0x00 );
while 1:
    print 'X=%6d' % read_word_sensor( MAGNET_XOUT ),
    print 'Y=%6d' % read_word_sensor( MAGNET_YOUT ),
    print 'Z=%6d' % read_word_sensor( MAGNET_ZOUT ),
    print # 改行
    sleep( 1 )
