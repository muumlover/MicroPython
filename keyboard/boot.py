import pyb

USB_VID = 0x5241
USB_PID = 0x006a

pyb.LED(1).off()
pyb.delay(500)  # Necessary delay, prevent failed initialization of USB_HID
"""
https:#github.com/micropython/micropython/blob/cb84e22ac6b1356986f63f5b6db95493da81fa5f/ports/stm32/usbdev/class/inc/usbd_cdc_msc_hid0.h#L54
subclass; # 0=no sub class, 1=boot
protocol; # 0=none, 1=keyboard, 2=mouse
max_packet_len; # only support up to 255
polling_interval; # in units of 1ms
report_desc; #
"""
hid_kbd_keyboard = (1, 1, 8, 1, bytes([
    0x05, 0x01,  # Usage Page (Generic Desktop)
    0x09, 0x06,  # Usage (Keyboard)
    0xA1, 0x01,  # Collection (Application)
    # Modifiers (8 bits)
    0x05, 0x07,  # Usage Page (Keyboard)
    0x19, 0xE0,  # Usage Minimum (Keyboard Left Control)
    0x29, 0xE7,  # Usage Maximum (Keyboard Right GUI)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x95, 0x08,  # Report Count (8)
    0x75, 0x01,  # Report Size (1)
    0x81, 0x02,  # Input (Data, Variable, Absolute)
    # Reserved(1 byte)
    0x81, 0x01,  # Input(Constant)
    # Keycodes (6 bytes)
    0x19, 0x00,  # Usage Minimum (0)
    0x29, 0xFF,  # Usage Maximum (255)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0xFF,  # Logical Maximum (255)
    0x95, 0x06,  # Report Count (6)
    0x75, 0x08,  # Report Size (8)
    0x81, 0x00,  # Input (Data, Array, Absolute)

    # Status LEDs (5 bits)
    0x05, 0x08,  # Usage Page (LED)
    0x19, 0x01,  # Usage Minimum (Num Lock)
    0x29, 0x05,  # Usage Maximum (Kana)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x95, 0x05,  # Report Count (5)
    0x75, 0x01,  # Report Size (1)
    0x91, 0x02,  # Output (Data, Variable, Absolute)
    # LED padding (3 bits)
    0x95, 0x03,  # Report Count (3)
    0x91, 0x01,  # Output (Constant)
    0xC0  # End Collection
]))
hid_nkro_keyboard = (1, 1, 33, 1, bytes([
    0x05, 0x01,  # Usage Page (Generic Desktop)
    0x09, 0x06,  # Usage (Keyboard)
    0xA1, 0x01,  # Collection (Application)
    # Modifiers (8 bits)
    0x05, 0x07,  # Usage Page (Keyboard)
    0x19, 0xE0,  # Usage Minimum (Keyboard Left Control)
    0x29, 0xE7,  # Usage Maximum (Keyboard Right GUI)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x95, 0x08,  # Report Count (8)
    0x75, 0x01,  # Report Size (1)
    0x81, 0x02,  # Input (Data, Variable, Absolute)
    # Reserved(1 byte)
    0x81, 0x01,  # Input(Constant)
    # Keycodes
    0x05, 0x07,  # Usage Page (Keyboard/Keypad)
    0x19, 0x00,  # Usage Minimum (0)
    0x29, 0xF7,  # Usage Maximum (247)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x95, 0xF8,  # Report Count (248)
    0x75, 0x01,  # Report Size (1)
    0x81, 0x02,  # Input (Data, Variable, Absolute, Bitfield)

    # Status LEDs (5 bits)
    0x05, 0x08,  # Usage Page (LED)
    0x19, 0x01,  # Usage Minimum (Num Lock)
    0x29, 0x05,  # Usage Maximum (Kana)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x95, 0x05,  # Report Count (5)
    0x75, 0x01,  # Report Size (1)
    0x91, 0x02,  # Output (Data, Variable, Absolute)
    # LED padding (3 bits)
    0x95, 0x03,  # Report Count (3)
    0x91, 0x01,  # Output (Constant)
    0xC0  # End Collection
]))
pyb.usb_mode('VCP+HID', vid=USB_VID, pid=USB_PID, hid=hid_nkro_keyboard)

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
