# noinspection PyUnresolvedReferences
import pyb

pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard)
