# !/usr/bin/env python
# encoding: utf-8

"""
@Time    : 2020/9/20 16:30
@Author  : Sam Wong
@Email   : muumlover@live.com
@Blog    : https://blog.ronpy.com
@Project : MicroPython
@FileName: main.py
@Software: PyCharm
@license : (C) Copyright 2020 by Sam Wong. All rights reserved.
@Desc    :

# pyb.usb_mode('CDC+HID',hid=pyb.hid_keyboard)

if pyb.Pin('A0').value():
    pyb.usb_mode('VCP+HID',hid=pyb.hid_keyboard)

    pyb.hid_keyboard = (1, 1, 8, 8, b'\x05\x01\t\x06\xa1\x01\x05\x07\x19\xe0)\xe7\x15\x00%\x01u\x01\x95\x08\x81\x02\x95\x01u\x08\x81\x01\x95\x05u\x01\x05\x08\x19\x01)\x05\x91\x02\x95\x01u\x03\x91\x01\x95\x06u\x08\x15\x00%e\x05\x07\x19\x00)e\x81\x00\xc0')

    0501 0906 a101 0507 19e0 29e7 1500 2501 7501 9508 8102 9501 7508 8101 9505 7501 0508 1901 2905 9102 9501 7503 9101 9506 7508 1500 2565 0507 1900 2965 8100 c0
    0501 0906 a101 0507 19e0 29e7 1500 2501 7501 9508 8102 9501 7508 8103 9505 7501 0508 1901 2905 9102 9501 7503 9103 9506 7508 1500 25ff 0507 1900 2965 8100 c0

hid_keyboard = bytearray([
    0x05, 0x01,  # USAGE_PAGE(Generic Desktop)
    0x09, 0x06,  # USAGE(Keyboard)
    0xa1, 0x01,  # COLLECTION(Application)

    0x05, 0x07,  # USAGE_PAGE(Keyboard)
    0x19, 0xe0,  # USAGE_MINIMUM(Keyboard Left Ctrl)
    0x29, 0xe7,  # USAGE_MAXIMUM(Keyboard Right GUI)
    0x15, 0x00,  # LOGICAL_MINIMUM(0)
    0x25, 0x01,  # LOGICAL_MAXIMUM(1)
    0x75, 0x01,  # REPORT_SIZE(1)
    0x95, 0x08,  # REPORT_COUNT(8)
    0x81, 0x02,  # INPUT(Data, Var, Abs)

    0x95, 0x01,  # REPORT_COUNT(1)
    0x75, 0x08,  # REPORT_SIZE(8)
    0x81, 0x03,  # INPUT(Cnst, Var, Abs)

    0x95, 0x05,  # REPORT_COUNT(5)
    0x75, 0x01,  # REPORT_SIZE(1)
    0x05, 0x08,  # USAGE_PAGE(LEDs)
    0x19, 0x01,  # USAGE_MINIMUM(Num Lock)
    0x29, 0x05,  # USAGE_MAXIMUM(Kana)
    0x91, 0x02,  # OUTPUT(Data, Var, Abs)

    0x95, 0x01,  # REPORT_COUNT(1)
    0x75, 0x03,  # REPORT_SIZE(3)
    0x91, 0x03,  # OUTPUT(Cnst, Var, Abs)

    0x95, 0x78,  # REPORT_COUNT(120)
    0x75, 0x01,  # REPORT_SIZE(1)
    0x15, 0x00,  # LOGICAL_MINIMUM(0)
    0x25, 0x01,  # LOGICAL_MAXIMUM(1)
    0x05, 0x07,  # USAGE_PAGE(Keyboard)
    0x19, 0x00,  # USAGE_MINIMUM(Reserved(no event indicated))
    0x29, 0x65,  # USAGE_MAXIMUM(Keyboard Application)
    0x81, 0x02,  # INPUT(Data, Var, Abs)

    0xc0,  # END_COLLECTION / * 63 * /
])

if pyb.Pin('A0').value():
    pyb.usb_mode('VCP+HID',hid=hid_keyboard)

if pyb.Pin('A0').value():
    pyb.usb_mode('VCP+HID',hid=b'\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x78\x75\x01\x15\x00\x25\x01\x05\x07\x19\x00\x29\x65\x81\x02\xc0')
"""

import micropython
# noinspection PyUnresolvedReferences
import pyb

micropython.alloc_emergency_exception_buf(100)


class KeyBoard:
    def __init__(self):
        self.hid = pyb.USB_HID()
        self.buf = bytearray(8)  # report is 8 bytes long

    def _scan(self):
        if pyb.Pin('A0').value():
            self.buf[2] = 0
            pyb.LED(1).off()
        else:
            self.buf[2] = 0x29
            pyb.LED(1).on()

    def run(self):
        while True:
            self._scan()
            self.hid.send(self.buf)


if __name__ == '__main__':
    kb = KeyBoard()
    kb.run()
