import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, qRgb
from PyQt5.QtCore import Qt
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical

# TensorFlow uyarılarını önlemek için ortam değişkenini ayarla
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

class DrawApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processing with NeurAI')
        self.setWindowIcon(QIcon('../Assets/brainlogo.ico'))
        self.setGeometry(100, 100, 400, 400)

        self.canvas = QLabel()
        self.canvas.setFixedSize(200, 200)
        self.canvas.setStyleSheet("border: 2px solid black; background-color: white;")
        self.canvas.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)

        self.clear_button = QPushButton('Temizle')
        self.clear_button.clicked.connect(self.clear_canvas)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)

        self.image = QImage(self.canvas.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.last_point = None

        self.model = tf.keras.models.load_model('mnist_model.h5')

    def clear_canvas(self):
        self.image.fill(Qt.white)
        self.canvas.setPixmap(QPixmap.fromImage(self.image))
        self.result_label.clear()

    def mousePressEvent(self, event):
        self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_point:
            painter = QPainter(self.image)
            painter.setPen(Qt.black)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.canvas.setPixmap(QPixmap.fromImage(self.image))

    def mouseReleaseEvent(self, event):
        self.last_point = None
        image_array = self.qimage_to_numpy(self.image)

        # Resmi 0 ile 1 arasında ölçeklendirin
        image_array = image_array.astype('float32') / 255.0

        # Tahmin etmek için modeli kullanın
        prediction = self.model.predict(image_array.reshape(1, 28, 28, 1))

        # En yüksek olasılığa sahip sınıfı alın
        predicted_number = np.argmax(prediction)

        # Tahmin edilen rakamı etikete yazdırın
        self.result_label.setText(f'Tahmin Edilen Rakam: {predicted_number}')

    def qimage_to_numpy(self, qimage):
        # Resmi 28x28 boyutuna uygun şekilde boyutlandır
        resized_image = qimage.scaled(28, 28).convertToFormat(QImage.Format_Grayscale8)

        # QImage'dan NumPy dizisine dönüştür
        buffer = resized_image.bits()
        buffer.setsize(resized_image.byteCount())
        image_array = np.frombuffer(buffer, dtype=np.uint8).reshape((28, 28, 1))

        # NumPy dizisini normalize et
        image_array = image_array.astype('float32') / 255.0

        return image_array


if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw_app = DrawApp()
    draw_app.show()
    sys.exit(app.exec_())
