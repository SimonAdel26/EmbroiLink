from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QColorDialog,
    QGraphicsPixmapItem,
    QMenu,
    QDialog,
    QListWidget,
    QVBoxLayout,
)


class NumberSelectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alege număr")
        self.resize(200, 300)  # important pentru scroll

        layout = QVBoxLayout(self)

        self.list = QListWidget()
        layout.addWidget(self.list)

        # scroll garantat
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # adaugă numerele 1–42
        for i in range(1, 43):
            self.list.addItem(str(i))

        self.list.itemClicked.connect(self.on_item_clicked)
        self.selected_number = None

    def on_item_clicked(self, item):
        self.selected_number = int(item.text())
        self.accept()
