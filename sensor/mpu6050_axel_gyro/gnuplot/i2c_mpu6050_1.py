#!/usr/bin/python
# -*- coding: utf-8 -*-
import smbus            # use I2C
import math
from time import sleep  # time module
import sys

### define #############################################################
DEV_ADDR = 0x68         # device address
PWR_MGMT_1 = 0x6b       # Power Management 1
ACCEL_XOUT = 0x3b       # Axel X-axis
ACCEL_YOUT = 0x3d       # Axel Y-axis
ACCEL_ZOUT = 0x3f       # Axel Z-axis

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
    if( val < 0x8000 ):
        return val # positive value
    else:
        return val - 65536 # negative value

# Get Axel data (raw value)
def get_accel_data_lsb():
    x = read_word_sensor( ACCEL_XOUT )
    y = read_word_sensor( ACCEL_YOUT )
    z = read_word_sensor( ACCEL_ZOUT )
    return [ x, y, z ]
# Get Axel data (G)
def get_accel_data_g():
    x,y,z = get_accel_data_lsb()
    # Sensitivity = 16384 LSB/G, @cf datasheet
    x = x / 16384.0
    y = y / 16384.0
    z = z / 16384.0
    return [x, y, z]

### Main function ######################################################
bus = smbus.SMBus( 1 )
bus.write_byte_data( DEV_ADDR, PWR_MGMT_1, 0 )

i = 1
while 1:
    # 加速度
    accel_x, accel_y, accel_z = get_accel_data_g()
    # 小数点以下第3位まで表示.
    print '%d %.3f %.3f %.3f' % ( i, accel_x, accel_y, accel_z )
    i = i + 1
    sys.stdout.flush()
    sleep(0.1)
