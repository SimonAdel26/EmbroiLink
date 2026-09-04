from PyQt6.QtWidgets import (
    QPushButton,
    QMainWindow,
    QFileDialog,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QTableWidgetItem,
    QColorDialog,
    QSplitter,
)
from PyQt6.QtGui import QPixmap, QImage, QColor, QMovie
from PyQt6 import uic
from PyQt6.QtCore import Qt

from embroi_link.src.base import Base
from embroi_link.src.gif import Gif
from embroi_link.src.embrodery_obj import EmbroderyObj, HISTORY_FILE_PATH

from pathlib import Path
import sys
import os
import cv2
import numpy as np
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path.cwd() / "embroi_link/interface/ui/window.ui", self)
        self.setWindowTitle("EmbroiLink")

        self.pushButtonUpload.clicked.connect(self.on_upload_image)
        self.pushButtonCreate.clicked.connect(self.on_create_design)
        self.pushButtonSave.clicked.connect(self.on_save_image)
        self.horizontalSliderK.valueChanged.connect(self.on_k_changed)
        self.horizontalSliderK.sliderReleased.connect(self.on_k_released)
        self.tableWidgetThreadColor.cellDoubleClicked.connect(self.cell_double_click)

        self.embrodery_obj = EmbroderyObj()
        self.gif = Gif()
        self.base = Base()

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        self.init_window()

    def keyPressEvent(self, event):
        # TODO: nu merge mereu
        if event.key() == Qt.Key.Key_A:
            self.stackedWidget.setCurrentIndex(0)
        elif event.key() == Qt.Key.Key_D:
            self.stackedWidget.setCurrentIndex(1)
        else:
            super().keyPressEvent(event)

    # ---------------------------------------   INIT WINDOW     ------------------------------------------------

    def init_window(self):

        with open(HISTORY_FILE_PATH, "r") as f:
            data = json.load(f)

        for key in data.keys():
            self.listWidgetHistory.addItem(key)

        self.on_k_changed(10)

        self.listWidgetHistory.itemDoubleClicked.connect(self.on_change_image)
        if self.listWidgetHistory.count() != 0:
            item = self.listWidgetHistory.item(0)
            self.listWidgetHistory.itemDoubleClicked.emit(item)

        self.refresh_color_table()

    def on_k_released(self):
        if self.horizontalSliderK.sliderPosition() != len(
            self.embrodery_obj.list_colors
        ):
            self.pushButtonCreate.clicked.emit()

    def on_k_changed(self, new_value):
        self.labelThreadColorsPalatte.setText(f"Thread Colors Palatte: {new_value}")

    def on_change_image(self, item):

        self.embrodery_obj.load_image(item.text(), False)

        self.refresh_color_table()
        self.show_image(self.viewOriginalImage, self.embrodery_obj.cv_image)
        self.show_image(self.viewNewImage, self.embrodery_obj.cv_image_result)
        self.stackedWidget.setCurrentIndex(0)

        self.embrodery_obj.colors(self.embrodery_obj.list_colors, False)
        colors = self.embrodery_obj.list_colors
        self.horizontalSliderK.valueChanged.emit(len(colors))
        self.refresh_color_table()

    def on_upload_image(self):
        """function (slot) to upload an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Upload Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )

        if not file_path:
            return

        self.embrodery_obj.load_image(file_path, True)
        self.show_image(self.viewOriginalImage, self.embrodery_obj.cv_image)
        self.listWidgetHistory.addItem(str(self.embrodery_obj.image_path))
        self.pushButtonCreate.clicked.emit()

        self.embrodery_obj.colors(self.embrodery_obj.list_colors, True)
        colors = self.embrodery_obj.list_colors
        self.horizontalSliderK.valueChanged.emit(len(colors))

    def on_create_design(self):
        """function to create the embroidery design"""
        # Verify if the image is loaded
        if self.viewOriginalImage.scene() is None:
            print("No image loaded.")
            return

        cv_image, colors = self.base.image_Kmeans(
            self.embrodery_obj.cv_image, self.horizontalSliderK.value()
        )

        cv_image = self.base.image_contour(cv_image)

        self.embrodery_obj.list_colors = colors

        self.show_image(self.viewNewImage, cv_image)

        self.embrodery_obj.cv_image_result = cv_image

        self.stackedWidget.setCurrentIndex(1)

        self.refresh_color_table()

    def on_save_image(self):
        """slot for save the result image"""
        self.embrodery_obj.save_image()

    # -----------------------------------------------    IMAGE SHOW     ---------------------------------------------

    def show_image(self, qt_graphics_view, cv_image):
        self.viewNewImage.setScene(None)
        if cv_image is None:
            return

        scene = QGraphicsScene()
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        height, width, _ = cv_image.shape
        bytes_per_line = 3 * width

        pixmap = QPixmap.fromImage(
            QImage(
                cv_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGB888,
            )
        )
        scene.addPixmap(pixmap)
        qt_graphics_view.setScene(scene)

    def show_loading(self):
        self.stackedWidget.setCurrentIndex(2)
        self.labelGif.clear()
        movie = QMovie(self.gif.get_random())
        movie.setScaledSize(self.labelGif.size())
        self.labelGif.setMovie(movie)
        movie.start()

    # ------------------------------------------  GET COLORS from the Thread Colors Palette -----------------------------------

    def get_colors(self):

        # Get the row and column count of the table
        rows = self.tableWidgetThreadColor.rowCount()
        cols = self.tableWidgetThreadColor.columnCount()

        # Create a list to store the colors
        colors = []
        for row in range(rows):
            for col in range(cols):
                item = self.tableWidgetThreadColor.item(row, col)
                if item is not None:
                    colors.append(item.data(Qt.ItemDataRole.UserRole))

        # Return the list of colors
        return colors

    def show_color(self, color):

        rows = self.tableWidgetThreadColor.rowCount()
        cols = self.tableWidgetThreadColor.columnCount()

        if rows == 0:
            self.tableWidgetThreadColor.insertRow(0)
            rows = 1

        # Find the first empty cell in the table
        color_added = False
        for r in range(rows):
            for c in range(cols):
                if self.tableWidgetThreadColor.item(r, c) is None:
                    # Create a new QTableWidgetItem with the selected color
                    item = QTableWidgetItem()
                    item.setBackground(color)
                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        (color.red(), color.green(), color.blue()),
                    )
                    self.tableWidgetThreadColor.setItem(r, c, item)
                    color_added = True
                    break

            if color_added:
                break

        # If no empty cell was found, add a new row and insert the color there
        if not color_added:
            self.tableWidgetThreadColor.insertRow(rows)
            item = QTableWidgetItem()
            item.setBackground(color)
            item.setData(
                Qt.ItemDataRole.UserRole, (color.red(), color.green(), color.blue())
            )
            self.tableWidgetThreadColor.setItem(rows, 0, item)

    def refresh_color_table(self):
        self.tableWidgetThreadColor.clear()
        colors = self.embrodery_obj.list_colors
        if len(colors) != 0:
            for b, g, r in colors:
                color = QColor(r, g, b)
                self.show_color(color)

    # function to add color to the thread colors palette
    def cell_double_click(self, row, col):
        print(self.embrodery_obj.image_path)
        # Open a color dialog to select a color
        item = self.tableWidgetThreadColor.item(row, col)

        start_color = item.background().color()
        color = QColorDialog.getColor(start_color, None, None)
        if not color.isValid():
            return

        item = QTableWidgetItem()
        item.setBackground(color)
        item.setData(
            Qt.ItemDataRole.UserRole,
            (color.red(), color.green(), color.blue()),
        )
        self.tableWidgetThreadColor.removeCellWidget(row, col)
        self.tableWidgetThreadColor.setItem(row, col, item)
        self.tableWidgetThreadColor.setFocus()

        colors = self.get_colors()
        self.embrodery_obj.colors(colors, True)
