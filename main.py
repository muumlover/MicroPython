import micropython
# noinspection PyUnresolvedReferences
import pyb

micropython.alloc_emergency_exception_buf(100)

ENABLE_USB = True
ROW = ['B4', 'B5', 'B6', 'B7', 'B8', 'A1']
COL = ['B12', 'B13', 'B14', 'B15', 'A8', 'A9', 'A10', 'A15', 'B9', 'A7', 'A6', 'B0', 'A5', 'A2', 'A3', 'A4']

KEY_MAP = [
    [0] * len(COL),
    [0] * len(COL),
    [0] * len(COL),
    [0] * len(COL),
    [0] * len(COL),
    [0] * 5 + [0x29] + [0] * (len(COL) - 6),
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
            row_pin.high()
        for col_pin in self.col_pins:
            col_pin.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

    def _get_index(self, code):
        return int(code / 8) + self.HEAD, 1 << (code % 8)

    def _check(self, code):
        byte_index, bit_index = self._get_index(code)
        return self.buf[byte_index] & bit_index

    def _set(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] | bit_index

    def _reset(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] & ~bit_index

    def _scan(self):
        for row, row_pin in enumerate(self.row_pins):
            row_pin.low()
            for col, col_pin in enumerate(self.col_pins):
                if col_pin.value() == 0:
                    self._set(KEY_MAP[row][col])
                else:
                    self._reset(KEY_MAP[row][col])
            row_pin.high()

        if self._check(0x29):
            pyb.LED(1).on()
        else:
            pyb.LED(1).off()

    def run(self):
        while True:
            self._scan()
            if ENABLE_USB:
                self.hid.send(self.buf)


if __name__ == '__main__':
    kb = KeyBoard()
    kb.run()
