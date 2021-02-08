import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class App(QWidget):
    def __init__(self):
        """
        :arg self.image : QLabel под изображение
        :arg self.field : QLineEdit под поле запроса
        :arg self.btn : QPushButton кнопка
        """
        super().__init__()
        uic.loadUi("main.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
