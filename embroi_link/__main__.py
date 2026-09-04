import sys
from PyQt6.QtWidgets import QApplication

from embroi_link.interface.interface import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    app.exec()
