import micropython
# noinspection PyUnresolvedReferences
import pyb

micropython.alloc_emergency_exception_buf(100)


class KeyBoard:
    HEAD = 2

    def __init__(self):
        self.hid = pyb.USB_HID()
        self.buf = bytearray(17)  # report is 8 bytes long

    def _get_index(self, code):
        return int(code / 8) + self.HEAD, 1 << (code % 8)

    def _set(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] | bit_index

    def _reset(self, code):
        byte_index, bit_index = self._get_index(code)
        self.buf[byte_index] = self.buf[byte_index] & ~bit_index

    def _scan(self):
        if pyb.Pin('A0').value():
            self._reset(0x29)
            pyb.LED(1).off()
        else:
            self._set(0x29)
            pyb.LED(1).on()

    def run(self):
        while True:
            self._scan()
            self.hid.send(self.buf)


if __name__ == '__main__':
    kb = KeyBoard()
    kb.run()
