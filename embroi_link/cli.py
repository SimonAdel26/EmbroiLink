

import sys
from PyQt6.QtWidgets import QApplication, QPushButton

def add(a,b):
    return a+b

def main() :

    app = QApplication(sys.argv)

    window = QPushButton("Push Me")
    window.show()

    app.exec()


