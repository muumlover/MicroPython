import _thread

import micropython

import pyb

micropython.alloc_emergency_exception_buf(100)

SEND_SIZE = 33  # report is 33 bytes long
RECV_SIZE = 64

# ROW = ['B4', 'B5', 'B6', 'B7', 'B8', 'C14']
# COL = ['B12', 'B13', 'B14', 'B15', 'A8', 'A9', 'A10', 'A15', 'B9', 'B1', 'B0', 'B2', 'A7', 'C15', 'A1', 'A2']
# C14->B3 A7->B10 C15->A3 B2 A0
ROW_PINS = ['B4', 'B5', 'B6', 'B7', 'B8', 'B3']
COL_PINS = ['B12', 'B13', 'B14', 'B15', 'A8', 'A9', 'A10', 'A15', 'B9', 'B1', 'B0', 'A0', 'B10', 'A3', 'A1', 'A2']

START, COUNT = 0x04, 26 + 10
(K_A, K_B, K_C, K_D, K_E, K_F, K_G, K_H, K_I, K_J, K_K, K_L, K_M, K_N, K_O, K_P, K_Q, K_R, K_S, K_T, K_U, K_V, K_W, K_X,
 K_Y, K_Z, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0) = range(START, START + COUNT)
START, COUNT = 0x28, 10 + 1 + 2 + 1 + 4
(K_ENT, K_ESC, K_BSPC, K_TAB, K_SPC, K_MINS, K_EQL, K_LBRC, K_RBRC, K_BSLS, _,
 K_SCLN, K_QUOT, K_GRV, K_COMM, K_DOT, K_SLSH, K_CAPS) = range(START, START + COUNT)
START, COUNT = 0x3A, 12 + 9 + 4
(K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12,
 K_PSCR, K_SLCK, K_PAUS, K_INS, K_HOME, K_PGUP, K_DEL, K_END, K_PGDN,
 K_RGHT, K_LEFT, K_DOWN, K_UP) = range(START, START + COUNT)
START, COUNT = 0xE0, 8
(K_LCTL, K_LSFT, K_LALT, K_LGUI, K_RCTL, K_RSFT, K_RALT, K_RGUI) = range(START, START + COUNT)

K_FN = 0xFF
_ = __ = ___ = ____ = 0

KEY_MAP = [
    [K_ESC, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12, K_PSCR, K_SLCK, K_PAUS],
    [K_GRV, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_MINS, K_EQL, K_BSPC, K_INS, K_PGUP],
    [K_TAB, K_Q, K_W, K_E, K_R, K_T, K_Y, K_U, K_I, K_O, K_P, K_LBRC, K_RBRC, K_BSLS, K_DEL, K_PGDN],
    [K_CAPS, K_A, K_S, K_D, K_F, K_G, K_H, K_J, K_K, K_L, K_SCLN, K_QUOT, ___, K_ENT, K_HOME, K_END],
    [K_LSFT, K_Z, K_X, K_C, K_V, K_B, K_N, K_M, K_COMM, K_DOT, K_SLSH, ___, ___, K_RSFT, K_UP, ____],
    [K_LCTL, K_LGUI, K_LALT, __, _, K_SPC, _, _, _, K_RALT, K_FN, _, K_RCTL, K_LEFT, K_DOWN, K_RGHT],
]

KEY_MAP_FN = [
    [K_ESC, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12, K_PSCR, K_SLCK, K_PAUS],
    [K_GRV, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_MINS, K_EQL, K_BSPC, K_INS, K_PGUP],
    [K_TAB, K_Q, K_W, K_E, K_R, K_T, K_Y, K_U, K_I, K_O, K_P, K_LBRC, K_RBRC, K_BSLS, K_DEL, K_PGDN],
    [K_CAPS, K_A, K_S, K_D, K_F, K_G, K_H, K_J, K_K, K_L, K_SCLN, K_QUOT, ___, K_ENT, K_HOME, K_END],
    [K_LSFT, K_Z, K_X, K_C, K_V, K_B, K_N, K_M, K_COMM, K_DOT, K_SLSH, ___, ___, K_RSFT, K_PGUP, __],
    [K_LCTL, K_LGUI, K_LALT, __, __, K_SPC, _, _, _, K_RALT, K_FN, _, K_RCTL, K_HOME, K_PGDN, K_END],
]


def thread_entry(self):
    while True:
        if self.hid is not None:
            # self.hid.recv(self.recv_buf)
            # print(self.recv_buf)
            buf = self.hid.recv(64)
            print(buf)
        pass
    pass


class KeyBoard:
    HEAD = 2

    def __init__(self):
        self.hid = pyb.USB_HID() if 'HID' in pyb.usb_mode() else None

        if self.hid is not None:
            _thread.start_new_thread(thread_entry, (self,))

        self.send_buf = bytearray(SEND_SIZE)
        self.recv_buf = bytearray(RECV_SIZE)

        self.fn = False
        self.row_pins = [pyb.Pin(x) for x in ROW_PINS]
        self.col_pins = [pyb.Pin(x) for x in COL_PINS]

        for row_pin in self.row_pins:
            row_pin.init(pyb.Pin.OUT_OD)
            row_pin.high()
        for col_pin in self.col_pins:
            col_pin.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

    @property
    def key_map(self):
        return KEY_MAP_FN if self.fn else KEY_MAP

    def _get_index(self, code):
        if code > 0xdf:
            return 0, 1 << (code & 0x07)
        return (code >> 3) + self.HEAD, 1 << (code & 0x07)

    def _check(self, code):
        byte_index, bit_index = self._get_index(code)
        return self.send_buf[byte_index] & bit_index

    def _set_key(self, code):
        if code == 0xff:
            self.fn = True
            return
        byte_index, bit_index = self._get_index(code)
        self.send_buf[byte_index] = self.send_buf[byte_index] | bit_index

    def _reset_key(self, code):
        if code == 0xff:
            self.fn = False
            return
        byte_index, bit_index = self._get_index(code)
        self.send_buf[byte_index] = self.send_buf[byte_index] & ~bit_index

    def _scan_matrix(self):
        for row, row_pin in enumerate(self.row_pins):
            row_pin.low()
            for col, col_pin in enumerate(self.col_pins):
                if col_pin.value() == 0:
                    self._set_key(self.key_map[row][col])
                else:
                    self._reset_key(self.key_map[row][col])
            row_pin.high()

        if self._check(self.key_map[5][5]):
            pyb.LED(1).on()
        else:
            pyb.LED(1).off()

    def run(self):
        while True:
            self._scan_matrix()
            if self.hid is not None:
                pyb.LED(1).on()
                self.hid.send(self.send_buf)
                pyb.LED(1).off()
            else:
                if 'HID' in pyb.usb_mode():
                    self.hid = pyb.USB_HID()


if __name__ == '__main__':
    kb = KeyBoard()
    kb.run()
