import micropython
# noinspection PyUnresolvedReferences
import pyb

micropython.alloc_emergency_exception_buf(100)

ENABLE_USB = False
ROW = ['B4', 'B5', 'B6', 'B7', 'B8', 'A1']
COL = ['B12', 'B13', 'B14', 'B15', 'A8', 'A9', 'A10', 'A15', 'B9', 'A7', 'A6', 'B0', 'A5', 'A2', 'A3', 'A4']

KEY_MAP = [
    [],
    [],
    [],
    [],
    [],
    [0, 0, 0, 0, 0, 0x29],
]


class KeyBoard:
    HEAD = 2

    def __init__(self):
        self.hid = pyb.USB_HID()
        self.buf = bytearray(17)  # report is 8 bytes long

        self.row_pins = [pyb.Pin(x) for x in ROW]
        self.col_pins = [pyb.Pin(x) for x in COL]

        for row_pin in self.row_pins:
            row_pin.init(pyb.Pin.OUT_OD)
        for col_pin in self.col_pins:
            col_pin.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

    def _get_index(self, code):
        return int(code / 8) + self.HEAD, 1 << (code % 8)

    def _set(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] | bit_index

    def _reset(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] & ~bit_index

    def _scan(self):
        if pyb.Pin('A9').value() == 0:
            self._set(0x29)
            pyb.LED(1).on()
        else:
            self._reset(0x29)
            pyb.LED(1).off()

    def run(self):
        while True:
            self._scan()
            if ENABLE_USB:
                self.hid.send(self.buf)


def on_target():
    global ENABLE_USB
    if not ENABLE_USB:
        ENABLE_USB = True


ext = pyb.ExtInt(pyb.Pin('A0'), pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, on_target)

if __name__ == '__main__':
    kb = KeyBoard()
    kb.run()
