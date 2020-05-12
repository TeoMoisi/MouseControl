# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel)

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Control Panel')
        self.setGeometry(100, 100, 200, 200)
        self.show()


#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    window = MainWindow()
#    sys.exit(app.exec_())
