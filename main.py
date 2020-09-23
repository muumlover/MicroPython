# noinspection PyUnresolvedReferences
import pyb

hid = pyb.USB_HID()

usb_buf = bytearray(8)  # report is 8 bytes long


def on_push(line):
    global usb_buf
    if pyb.Pin('A0').value():
        usb_buf[0] = 0
        usb_buf[2] = 0
        pyb.LED(1).off()
        hid.send(usb_buf)  # key released
    else:
        usb_buf[2] = 0x29
        hid.send(usb_buf)  # key released
        pyb.LED(1).on()


ext = pyb.ExtInt(pyb.Pin('A0'), pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, on_push)
while True:
    pass
