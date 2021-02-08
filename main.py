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
        self.coords = None
        self.get_coords()
        self.set_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.scale + 0.1 <= 3:
                self.scale += 0.1
                self.update()
        if event.key() == Qt.Key_PageDown:
            if self.scale - 0.1 > 0.001:
                self.scale -= 0.1
                self.update()
        move = self.scale / 0.1 * 0.01
        if event.key() == Qt.Key_Up:
            self.coords = (self.coords[0], self.coords[1] + move)
            self.update()
        if event.key() == Qt.Key_Left:
            self.coords = (self.coords[0] - move, self.coords[1])
            self.update()
        if event.key() == Qt.Key_Right:
            self.coords = (self.coords[0] + move, self.coords[1])
            self.update()
        if event.key() == Qt.Key_Down:
            self.coords = (self.coords[0], self.coords[1] - move)
            self.update()

    def set_map(self):
        try:
            self.get_coords()
            with open("map_file.txt", "wb") as file:
                file.write(get_map(self.coords, self.scale))
            pixmap = QPixmap("map_file.txt")
            self.image.setPixmap(pixmap)
        except Exception as error:
            print(error)

    def update(self):
        with open("map_file.txt", "wb") as file:
            file.write(get_map(self.coords, self.scale))
        pixmap = QPixmap("map_file.txt")
        self.image.setPixmap(pixmap)

    def get_coords(self):
        if self.field.text():
            self.coords = get_coords(get_address(self.field.text()))
        else:
            self.coords = get_coords(get_address(self.start))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
