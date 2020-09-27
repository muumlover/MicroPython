import pyb

pyb.LED(1).off()
pyb.delay(500)  # Necessary delay, prevent failed initialization of USB_HID
"""
https://github.com/micropython/micropython/blob/cb84e22ac6b1356986f63f5b6db95493da81fa5f/ports/stm32/usbdev/class/inc/usbd_cdc_msc_hid0.h#L54
subclass; // 0=no sub class, 1=boot
protocol; // 0=none, 1=keyboard, 2=mouse
max_packet_len; // only support up to 255
polling_interval; // in units of 1ms
report_desc; //
"""
hid_keyboard = (1, 1, 17, 1, bytes([
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
]))

pyb.usb_mode('VCP+HID', hid=hid_keyboard)

if 'HID' not in pyb.usb_mode():
    pyb.hard_reset()

pyb.LED(1).on()
pyb.delay(100)
pyb.LED(1).off()
pyb.delay(100)
pyb.LED(1).on()
pyb.delay(100)
pyb.LED(1).off()
pyb.delay(500)
