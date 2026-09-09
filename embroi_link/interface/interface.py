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
    QMenu,
    QScrollBar,
)
from PyQt6.QtGui import QPixmap, QImage, QColor, QMovie
from PyQt6 import uic
from PyQt6.QtCore import Qt

from embroi_link.src.base import Base
from embroi_link.src.gif import Gif
from embroi_link.src.embrodery_obj import EmbroderyObj, HISTORY_FILE_PATH, PROJECT_DIR

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

        self.tableWidgetThreadColor.cellDoubleClicked.connect(
            self.on_double_click_on_cell
        )
        self.tableWidgetThreadColor.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.tableWidgetThreadColor.customContextMenuRequested.connect(
            self.on_click_right_on_cell
        )

        self.viewNewImage.mousePressEvent = self.on_image_click
        self.viewNewImage.mouseDoubleClickEvent = self.on_image_double_click

        self.list_embroidery_stiches = QMenu()
        self.embrodery_obj = EmbroderyObj()
        self.gif = Gif()
        self.base = Base()

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        self.init_window()

    # Public methods

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

            if self.embrodery_obj.cv_image_result is None:
                self.pushButtonCreate.clicked.emit()

            self.stackedWidget.setCurrentIndex(1)

        self.refresh_color_table()
        self._init_embroidery_stiches()

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

    def refresh_color_table(self):
        """function for representation colors in the thread colors palette"""
        self.tableWidgetThreadColor.clear()
        colors = self.embrodery_obj.list_colors
        if len(colors) != 0:
            for b, g, r in colors:
                color = QColor(r, g, b)
                self.show_color(color)
        self.horizontalSliderK.setValue(len(colors))

    # Events

    def keyPressEvent(self, event):
        # TODO: nu merge mereu
        if event.key() == Qt.Key.Key_A:
            self.stackedWidget.setCurrentIndex(0)
        elif event.key() == Qt.Key.Key_D:
            self.stackedWidget.setCurrentIndex(1)
        elif event.key() == Qt.Key.Key_X:
            self.stackedWidget.setCurrentIndex(2)
            self.show_loading()
        else:
            super().keyPressEvent(event)

    def on_image_click(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_image(self.viewNewImage, self.embrodery_obj.cv_image_result)
            return

        x, y = self._get_image_coords(event)
        image_selected_zone = self.embrodery_obj.click_zone(x, y, None)
        if image_selected_zone is None:
            return

        self.show_image(self.viewNewImage, image_selected_zone)

    def on_image_double_click(self, event):
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        x, y = self._get_image_coords(event)
        _ = self.embrodery_obj.click_zone(x, y, color)
        self.show_image(self.viewNewImage, self.embrodery_obj.cv_image_result)
        self.refresh_color_table()

    def on_click_right_on_cell(self, pos):
        item = self.tableWidgetThreadColor.itemAt(pos)
        if item is None:
            return

        # # 1. Create the scrollbar
        # scrollbar = QScrollBar(Qt.Orientation.Vertical)

        # # 2. Change the context menu policy
        # scrollbar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # # 3. Define the custom menu function
        # def show_custom_menu(position):
        #     menu = QMenu()
        #     action1 = menu.addAction("Reset Scroll")
        #     action2 = menu.addAction("Bookmark Position")

        #     # Show the menu at the cursor position
        #     selected_action = menu.exec(scrollbar.mapToGlobal(position))

        #     if selected_action == action1:
        #         scrollbar.setValue(0)

        # 4. Connect the signal
        # scrollbar.customContextMenuRequested.connect(show_custom_menu)

        self.list_embroidery_stiches.setMaximumHeight(200)
        # self.list_embroidery_stiches.exec(scrollbar.mapToGlobal(pos))

        self.list_embroidery_stiches.exec(
            self.tableWidgetThreadColor.viewport().mapToGlobal(pos)
        )

        if self.selected_number_from_embroidery_stiches is not None:
            bg = item.background().color()
            brightness = (bg.red() * 0.299) + (bg.green() * 0.587) + (bg.blue() * 0.114)

            if brightness < 128:
                item.setForeground(QColor(255, 255, 255))
            else:
                item.setForeground(QColor(0, 0, 0))

            item.setText(str(self.selected_number_from_embroidery_stiches))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def on_double_click_on_cell(self, row, col):
        """function to add color to the thread colors palette"""
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

    def on_change_image(self, item):
        self.embrodery_obj.load_image(item.text())

        self.show_image(self.viewOriginalImage, self.embrodery_obj.cv_image)
        self.show_image(self.viewNewImage, self.embrodery_obj.cv_image_result)
        self.refresh_color_table()

        self.stackedWidget.setCurrentIndex(0)

    # Slots

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

    def on_create_design(self):
        """function to create the embroidery design"""
        # Verify if the image is loaded
        if self.viewOriginalImage.scene() is None:
            print("No image loaded.")
            return

        cv_image, colors = self.base.image_Kmeans(
            self.embrodery_obj.cv_image, self.horizontalSliderK.value()
        )
        # cv_image = self.base.image_contour(cv_image)

        self.embrodery_obj.colors(colors, True)
        self.embrodery_obj.cv_image_result = cv_image

        self.show_image(self.viewNewImage, self.embrodery_obj.cv_image_result)

        self.stackedWidget.setCurrentIndex(1)

        self.refresh_color_table()

    def on_save_image(self):
        """slot for save the result image"""
        self.embrodery_obj.save_image()

    def on_number_selected(self, number):
        self.selected_number_from_embroidery_stiches = number

    def on_k_released(self):
        if self.horizontalSliderK.sliderPosition() != len(
            self.embrodery_obj.list_colors
        ):
            self.pushButtonCreate.clicked.emit()

    def on_k_changed(self, new_value):
        self.labelThreadColorsPalatte.setText(f"Thread Colors Palatte: {new_value}")

    # Private methods

    def _init_embroidery_stiches(self):
        pixmap = QPixmap(
            "/workspaces/EmbroiLink/embroi_link/res/EmbroideryStitches.png"
        )

        self.labelListOfEmbroideryStitches.resize(1000, 300)
        self.labelListOfEmbroideryStitches.setPixmap(
            pixmap.scaled(
                self.labelListOfEmbroideryStitches.width(),
                self.labelListOfEmbroideryStitches.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.labelListOfEmbroideryStitches.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i in range(1, 43):
            action = self.list_embroidery_stiches.addAction(str(i))
            action.triggered.connect(lambda checked, x=i: self.on_number_selected(x))
        self.selected_number_from_embroidery_stiches = None

    def _convert_coords(self, x_view, y_view):
        h_img, w_img, _ = self.embrodery_obj.cv_image_result.shape

        pixmap_new_image = None
        for item in self.viewNewImage.scene().items():
            if isinstance(item, QGraphicsPixmapItem):
                pixmap_new_image = item.pixmap()

        if pixmap_new_image is None:
            return -1, -1

        w_view = pixmap_new_image.width()
        h_view = pixmap_new_image.height()

        x_real = int(x_view * w_img / w_view)
        y_real = int(y_view * h_img / h_view)

        return x_real, y_real

    def _get_image_coords(self, event):
        scene_pos = self.viewNewImage.mapToScene(event.position().toPoint())
        return self._convert_coords(int(scene_pos.x()), int(scene_pos.y()))

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
