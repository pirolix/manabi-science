#!/usr/bin/python
# -*- coding: utf-8 -*-
import smbus            # use I2C
import math
from time import sleep  # time module
import sys
import os

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

# gnuplot を子プロセスとして起動
g = os.popen( 'gnuplot -noraise', 'w' )

try:
    # ring buffer を準備する
    BUFFER_SIZE = 20
    accel_x = [0] * BUFFER_SIZE
    accel_y = [0] * BUFFER_SIZE
    accel_z = [0] * BUFFER_SIZE
    buffer_index = 0
    while 1:
        # 加速度を取得する
        accel_x[buffer_index], \
        accel_y[buffer_index], \
        accel_z[buffer_index] = get_accel_data_g()
        buffer_index = ( buffer_index + 1 ) % BUFFER_SIZE
        # gnuplot にコマンドを書き出す
        g.write("""
set xrange [-1.5:1.5]
set yrange [-1.5:1.5]
set zrange [-1.5:1.5]
splot '-' with lines linewidth 3
""")
        # ring buffer の内容を書き出す
        i = 0
        while i < BUFFER_SIZE:
          g.write( "%f %f %f\n" % ( \
              accel_x[(buffer_index+i)%BUFFER_SIZE], \
              accel_y[(buffer_index+i)%BUFFER_SIZE], \
              accel_z[(buffer_index+i)%BUFFER_SIZE] ))
          i = i + 1
        g.write( "e\n" )
        g.flush() # 即時反映
        sleep(0.05)

# Ctrl+C で割り込まれた際、子プロセスを閉じる
except KeyboardInterrupt:
    g.close()
