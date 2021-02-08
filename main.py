from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from API import *
import sys


class App(QWidget):
    def __init__(self):
        """
        :arg self.image : QLabel под изображение
        :arg self.field : QLineEdit под поле запроса
        :arg self.btn : QPushButton кнопка
        """
        super().__init__()
        uic.loadUi("main.ui", self)
        self.btn.clicked.connect(self.set_map)
        self.scale = 0.05
        self.start = "2-й Давыдовский мкр., 21, Кострома, Костромская обл., 156016"
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
