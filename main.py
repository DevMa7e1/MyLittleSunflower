from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PIL import Image
import sys

app = QApplication(sys.argv)

def load_image(name: str, size: tuple[int, int]):
    img = Image.open(name)
    img = img.resize(size, Image.Resampling.NEAREST)
    return QPixmap.fromImage(img.toqimage())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyLittleSunflower")
        mainbox = QHBoxLayout()
        box1 = QVBoxLayout()

        imagelabel = QLabel()
        imagelabel.setPixmap(load_image('res/flower-default.png', (128, 256)))
        imagelabel.setFixedSize(QSize(128, 256))
        imagelabel.setScaledContents(True)
        box1.addWidget(imagelabel)

        progress = QProgressBar()
        progress.setValue(50)
        box1.addWidget(progress)

        flower = QWidget()
        flower.setLayout(box1)
        mainbox.addWidget(flower)

        box2 = QVBoxLayout()
        box2.setAlignment(Qt.AlignmentFlag.AlignTop)

        time = QLabel()
        time.setAlignment(Qt.AlignmentFlag.AlignRight)
        time.setText('10\n21')
        font = time.font()
        font.setPixelSize(70)
        time.setFont(font)
        box2.addWidget(time)

        label1 = QLabel()
        font = label1.font()
        font.setPixelSize(20)
        font.setBold(True)
        label1.setFont(font)
        label1.setText("0/10 hours")
        box2.addWidget(label1)

        label2 = QLabel()
        label2.setText("Break in: 40min")
        font = label2.font()
        font.setPixelSize(14)
        label2.setFont(font)
        box2.addWidget(label2)

        extra = QWidget()
        extra.setLayout(box2)
        mainbox.addWidget(extra)

        mainwidget = QWidget()
        mainwidget.setLayout(mainbox)
        self.setCentralWidget(mainwidget)

window = MainWindow()
window.show()

app.exec()