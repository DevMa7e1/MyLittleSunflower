from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar,\
QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QCheckBox, QLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QCloseEvent, QPixmap
from PIL import Image
import sys
from misc_classes import *

app = QApplication(sys.argv)

settings = UserSettings()

please_dont_garbage_collect = None

def load_image(name: str, size: tuple[int, int]):
    img = Image.open(name)
    img = img.resize(size, Image.Resampling.NEAREST)
    return QPixmap.fromImage(img.toqimage())

class MainWindow(QMainWindow):
    def __init__(self):
        global settings

        super().__init__()
        self.setWindowTitle("MyLittleSunflower")
        self.setStyleSheet('background-color: lightblue;')
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
        font = time.font()
        font.setPixelSize(70)
        font.setFamily('monospace')
        time.setFont(font)
        box2.addWidget(time)

        label1 = QLabel()
        font = label1.font()
        font.setPixelSize(20)
        font.setBold(True)
        font.setFamily('monospace')
        label1.setFont(font)
        label1.setText("0/10 hours")
        box2.addWidget(label1)

        label2 = QLabel()
        label2.setText("Break in: 40min")
        font = label2.font()
        font.setPixelSize(14)
        font.setFamily('monospace')
        label2.setFont(font)
        box2.addWidget(label2)

        timer = TimeTimer(self, time, label1, label2, progress, settings, app)
        timer.timerEvent(None)
        timer.startTimer(1000, Qt.TimerType.CoarseTimer)

        settbtn = QPushButton()
        settbtn.setText('Settings')
        settbtn.clicked.connect(SettingsWindow.new_window)
        settbtn.setStyleSheet('margin-top: 39px; height: 23px;')
        box2.addWidget(settbtn)

        extra = QWidget()
        extra.setLayout(box2)
        mainbox.addWidget(extra)

        mainbox.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        mainwidget = QWidget()
        mainwidget.setLayout(mainbox)
        self.setCentralWidget(mainwidget)

class SettingsWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        global settings

        self.cw = None
        
        super().__init__(parent)
        self.setWindowTitle('Settings')
        mainbox = QVBoxLayout()
        mainbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        bigtext = QLabel('Settings')
        font = bigtext.font()
        font.setPixelSize(30)
        bigtext.setFont(font)
        mainbox.addWidget(bigtext)

        label = QLabel('Time between breaks:')
        label.setStyleSheet('margin-top: 8px;')
        mainbox.addWidget(label)
        tbbinput = QLineEdit()
        tbbinput.setInputMask('00:00')
        tbbinput.setText(self.sectostr(settings.breakInterval()))
        tbbinput.setStyleSheet('margin-bottom: 4px;')
        self.tbb = tbbinput
        mainbox.addWidget(tbbinput)

        label = QLabel('Break time:')
        mainbox.addWidget(label)
        btinput = QLineEdit()
        btinput.setInputMask('00 mi\\nutes')
        btinput.setText(f'{str(settings.breakTime()//60).zfill(2)} minutes')
        btinput.setStyleSheet('margin-bottom: 8px;')
        self.bt = btinput
        mainbox.addWidget(btinput)

        cwcheck = QCheckBox()
        cwcheck.setText('Sync with Hackatime/Wakatime')
        cwcheck.checkStateChanged.connect(self.checkStateChanged)
        cwcheck.setChecked(settings.callWakatime())
        self.cw = cwcheck
        mainbox.addWidget(cwcheck)

        self.mainbox = mainbox
        self.removable: list[QWidget] = []
        self.setLayout(mainbox)
        self.checkStateChanged()
        mainbox.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
    def sectostr(self, sec: int):
        hours = sec // 3600
        minutes = sec % 3600 // 60
        return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}'
    def new_window(self):
        global please_dont_garbage_collect
        if type(please_dont_garbage_collect) == SettingsWindow:
            please_dont_garbage_collect.close()
        w = SettingsWindow()
        please_dont_garbage_collect = w
        w.show()
    def checkStateChanged(self):
        if type(self.cw) == QCheckBox:
            if self.cw.isChecked():
                for i in self.removable:
                    i.hide()
                    self.mainbox.takeAt(self.mainbox.indexOf(i))
                self.removable.clear()
                label = QLabel('HT/WT API URL:')
                self.mainbox.addWidget(label)
                self.removable.append(label)
                urlinput = QLineEdit()
                urlinput.setText('http://localhost:8000/')
                urlinput.setStyleSheet('margin-bottom: 8px;')
                self.mainbox.addWidget(urlinput)
                self.removable.append(urlinput)

                label = QLabel('HT/WT API key:')
                self.mainbox.addWidget(label)
                self.removable.append(label)
                keyinput = QLineEdit()
                keyinput.setText('SECRET_API_KEY')
                self.mainbox.addWidget(keyinput)
                self.removable.append(keyinput)
            else:
                for i in self.removable:
                    i.hide()
                    self.mainbox.takeAt(self.mainbox.indexOf(i))
                self.removable.clear()
                label = QLabel('Goal:')
                self.mainbox.addWidget(label)
                self.removable.append(label)
                goalinput = QLineEdit()
                goalinput.setInputMask('00:00')
                goalinput.setText(self.sectostr(settings.goal()))
                self.mainbox.addWidget(goalinput)
                self.removable.append(goalinput)
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        val = self.tbb.text().split(':')
        settings.setBreakInterval(int(val[0])*3600 + int(val[1])*60)
        val = self.bt.text().removesuffix(' minutes')
        settings.setBreakTime(int(val)*60)
        if self.cw.isChecked(): #type: ignore
            if type(self.removable[1]) == QLineEdit:
                text = self.removable[1].text()
                if text.removeprefix('https://').removeprefix('http://') == text:
                    text = 'https://'+text
                if not text.endswith('/'):
                    text += '/'
                settings.setApiUrl(text)
            if type(self.removable[3]) == QLineEdit:
                settings.setApiKey(self.removable[3].text())
            settings.setCallWakatime(True)
        else:
            if type(self.removable[1]) == QLineEdit:
                val = self.removable[1].text().split(':')
                settings.setGoal(int(val[0])*3600 + int(val[1])*60)
            settings.setCallWakatime(False)
        settings.save()
        return super().closeEvent(a0)

window = MainWindow()
window.show()

app.exec()