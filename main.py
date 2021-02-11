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

    def set_map(self):
        try:
            self.get_coords()
            with open("map_file.txt", "wb") as file:
                file.write(get_map(self.coords, self.scale, pt=self.coords))
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
