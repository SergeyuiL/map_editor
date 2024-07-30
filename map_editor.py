import sys
import yaml
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint

class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Map Editor')
        self.showMaximized()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: white;")
        self.image_label.setFocusPolicy(Qt.StrongFocus)  

        self.load_button = QPushButton('Load Map', self)
        self.load_button.clicked.connect(self.load_map)

        self.save_button = QPushButton('Save Map', self)
        self.save_button.clicked.connect(self.save_map)

        self.save_as_button = QPushButton('Save Map As', self)
        self.save_as_button.clicked.connect(self.save_map_as)

        layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.save_as_button)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.map_image = None
        self.image_path = None
        self.map_resolution = None
        self.map_origin = None

        self.frame_pos = QPoint(0, 0)  
        self.scale_factor = 1.0

        self.history = []

    def load_map(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Map Folder')
        if folder_path:
            yaml_file = None
            pgm_file = None

            for file in os.listdir(folder_path):
                if file.endswith('.yaml'):
                    yaml_file = os.path.join(folder_path, file)
                elif file.endswith('.pgm'):
                    pgm_file = os.path.join(folder_path, file)

            if yaml_file and pgm_file:
                with open(yaml_file, 'r') as file:
                    yaml_data = yaml.safe_load(file)
                    self.image_path = pgm_file
                    self.map_resolution = yaml_data['resolution']
                    self.map_origin = yaml_data['origin']

                self.map_image = QImage(self.image_path)
                self.frame_pos = QPoint(self.map_image.width() // 2, self.map_image.height() // 2)
                self.update_displayed_image()

    def save_map(self):
        if self.image_path:
            self.map_image.save(self.image_path)

    def save_map_as(self):
        if self.map_image is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Map As", "", "PGM Files (*.pgm);;All Files (*)", options=options)
            if file_path:
                self.map_image.save(file_path)

    def update_displayed_image(self):
        if self.map_image is not None:
            # Calculate the scale factor and offsets to center the image
            image_size = self.map_image.size()
            label_size = self.image_label.size()

            self.scale_factor = min(label_size.width() / image_size.width(), label_size.height() / image_size.height())

            scaled_image = self.map_image.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)

            painter = QPainter(pixmap)
            pen = QPen(QColor(255, 0, 0), 1, Qt.SolidLine)
            painter.setPen(pen)
            # Draw the 1x1 selection frame accurately on the image
            scaled_frame_pos = QPoint(int(self.frame_pos.x() * self.scale_factor), int(self.frame_pos.y() * self.scale_factor))
            painter.drawRect(scaled_frame_pos.x(), scaled_frame_pos.y(), int(self.scale_factor), int(self.scale_factor))
            painter.end()
            self.image_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if self.map_image is not None:
            if event.key() == Qt.Key_Left:
                self.frame_pos.setX(max(0, self.frame_pos.x() - 1))
            elif event.key() == Qt.Key_Right:
                self.frame_pos.setX(min(self.map_image.width() - 1, self.frame_pos.x() + 1))
            elif event.key() == Qt.Key_Up:
                self.frame_pos.setY(max(0, self.frame_pos.y() - 1))
            elif event.key() == Qt.Key_Down:
                self.frame_pos.setY(min(self.map_image.height() - 1, self.frame_pos.y() + 1))
            elif event.key() == Qt.Key_Space:
                self.toggle_pixel()
            self.update_displayed_image()

    def toggle_pixel(self):
        if self.map_image is not None:
            painter = QPainter(self.map_image)
            x, y = self.frame_pos.x(), self.frame_pos.y()
            current_color = self.map_image.pixelColor(x, y)
            new_color = QColor(0, 0, 0) if current_color == QColor(255, 255, 255) else QColor(255, 255, 255)
            painter.setPen(new_color)
            painter.drawPoint(x, y)
            self.history.append((x, y, current_color))
            painter.end()
            self.update_displayed_image()

    def undo_last_action(self):
        if self.history:
            x, y, color = self.history.pop()
            painter = QPainter(self.map_image)
            painter.setPen(color)
            painter.drawPoint(x, y)
            painter.end()
            self.update_displayed_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MapEditor()
    editor.show()
    editor.image_label.setFocus()  
    sys.exit(app.exec_())
