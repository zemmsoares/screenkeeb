from pynput import keyboard
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

# The key codes for the mod keys
MOD_KEYS = {keyboard.Key.alt_l, keyboard.Key.shift_l}
CLOSE_KEY = keyboard.KeyCode(char='q')

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowOpacity(0.7)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | 
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowTransparentForInput |
            QtCore.Qt.Tool
        )
        self.setStyleSheet("background:transparent;")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.layout_img = QtGui.QPixmap('layer1.png')
        self.numeric_layout_img = QtGui.QPixmap('layer2.png')

        self.is_mod_pressed = False
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setPixmap(self.layout_img)
        self.image_label.setFixedSize(self.layout_img.size())

        self.setFixedSize(self.layout_img.size())

    def toggle_layout(self, is_mod_pressed):
        self.is_mod_pressed = is_mod_pressed
        if self.is_mod_pressed:
            self.image_label.setPixmap(self.numeric_layout_img)
            self.image_label.setFixedSize(self.numeric_layout_img.size())
            self.setFixedSize(self.numeric_layout_img.size())
        else:
            self.image_label.setPixmap(self.layout_img)
            self.image_label.setFixedSize(self.layout_img.size())
            self.setFixedSize(self.layout_img.size())

app = QtWidgets.QApplication([])
window = TransparentWindow()

def on_press(key):
    if key in MOD_KEYS:
        window.toggle_layout(True)

def on_release(key):
    if key in MOD_KEYS:
        window.toggle_layout(False)

def close_application():
    app.quit()

with keyboard.GlobalHotKeys({
    '<alt_l>+<shift_l>+q': close_application
}) as hotkey_listener:
    with keyboard.Listener(on_press=on_press, on_release=on_release):
        window.show()
        sys.exit(app.exec_())