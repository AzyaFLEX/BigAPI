from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from API import *
import sys


class App(QWidget):
    def __init__(self):
        """
        :param self.image : QLabel под изображение
        :param self.field : QLineEdit под поле запроса
        :param self.btn : QPushButton кнопка
        """
        super().__init__()
        uic.loadUi("main.ui", self)
        self.btn.clicked.connect(self.set_map)
        self.scale = 0.1
        self.start = "2-й Давыдовский мкр., 21, Кострома, Костромская обл., 156016"
        self.set_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.scale + 0.1 <= 3:
                self.scale += 0.1
                print(self.scale)
            self.set_map()
        if event.key() == Qt.Key_PageDown:
            if self.scale - 0.1 > 0:
                self.scale -= 0.1
                print(self.scale)
                self.set_map()

    def set_map(self):
        if self.field.text():
            with open("map_file.txt", "wb") as file:
                file.write(get_map(get_coords(get_address(self.field.text())), self.scale))
        else:
            with open("map_file.txt", "wb") as file:
                file.write(get_map(get_coords(get_address(self.start)), self.scale))
        pixmap = QPixmap("map_file.txt")
        self.image.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
