from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)
        self.new_game.clicked.connect(self.start_game)
        self.exit.clicked.connect(self.exit_game)
        self.setWindowTitle('Buzz Lighter: The Menu')

    def start_game(self):
        os.system('python main.py')
        sys.exit(app.exec_())

    def exit_game(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())