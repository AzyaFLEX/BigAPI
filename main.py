from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import uic
from API import *
import sys
import os


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
        self.change_lay.clicked.connect(self.def_change_lay)
        self.return_lay.clicked.connect(self.def_return_lay)
        self.cancel.clicked.connect(self.def_cancel)
        self.postcode.stateChanged.connect(self.add_postcode)
        self.is_postcode_added = False
        self.scale = 0.1
        self.start = "Лицей 17, 2-й Давыдовский мкр., 21, Кострома, Костромская обл.,"
        self.map = "map"
        self.coords, self.coords_flag = None, None
        self.center = (512, 420)
        self.points = []
        self.get_coords()
        self.set_map()
        self.write_full_address(self.start)

    def def_cancel(self):
        helper = self.field.text()
        self.field.setText(self.start)
        self.write_full_address(self.start)
        self.set_map()
        self.field.setText(helper)

    def def_change_lay(self):
        self.map = {"map": "sat", "sat": "skl", "skl": "trf", "trf": "map"}[self.map]
        self.update()

    def write_full_address(self, address):
        self.full_adress.setText(get_address(address, self.is_postcode_added))

    def add_postcode(self):
        # у многих адресов нет почтового индекса.
        # для теста можно использовать адрес офиса Яндекса (Москва Льва Толстого 16)
        self.is_postcode_added = not self.is_postcode_added    # 9 задача
        self.write_full_address(self.full_adress.text())    # 10 задача

    def def_return_lay(self):
        self.map = "map"
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            move = self.scale / 0.1 * 0.01
            data = [event.x() - self.center[0], event.y() - self.center[1]]
            point = [self.coords[0] + data[0] * (self.scale / 150),
                           self.coords[1] - data[1] * (self.scale / 150)]
            data = get_organization(get_coords_to_address(point))[0]['properties']['name']
            if data:
                self.field_2.setText(data)
        elif event.buttons() == QtCore.Qt.LeftButton:
            move = self.scale / 0.1 * 0.01
            data = [event.x() - self.center[0], event.y() - self.center[1]]
            point = [self.coords[0] + data[0] * (self.scale / 150),
                     self.coords[1] - data[1] * (self.scale / 150)]
            try:
                data = get_coords_to_address(point)[0]['properties']['name']
            except Exception:
                data = ""
            self.coords_flag = tuple(point)
            self.field.setText(data)
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.scale + 0.1 <= 3:
                self.scale *= 2
                self.update()
        if event.key() == Qt.Key_PageDown:
            if self.scale + 0.00001 > 0.00078125:
                self.scale /= 2
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
            if self.field.text():
                self.write_full_address(self.field.text())
            else:
                self.write_full_address(self.start)
            with open("map_file.txt", "wb") as file:
                self.coords_flag = self.coords
                file.write(get_map(self.coords, self.scale, self.map, [self.coords_flag] + self.points))
            pixmap = QPixmap("map_file.txt")
            self.image.setPixmap(pixmap)
            self.setFocus(True)
        except Exception as error:
            print(error)

    def update(self):
        with open("map_file.txt", "wb") as file:
            file.write(get_map(self.coords, self.scale, self.map, [self.coords_flag] + self.points))
        pixmap = QPixmap("map_file.txt")
        self.image.setPixmap(pixmap)
        self.setFocus(True)

    def get_coords(self):
        if self.field.text():
            self.coords = get_coords(get_address(self.field.text()))
        else:
            self.coords = get_coords(get_address(self.start))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    exec_ = app.exec()
    os.system('echo. > map_file.txt')
    sys.exit(exec_)
