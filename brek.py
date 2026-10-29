from PyQt6.QtCore import QObject, QTimerEvent, Qt, QTimer, QSize
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
from time import time

brekwindow = None
brektimer = None
app: QApplication = None #type: ignore
start = 0
end = 0

class BrekWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        global app
        super().__init__(parent) #type: ignore
        app.applicationStateChanged.connect(self.focusOut)
    def focusOut(self) -> None:
        close()

class BrekTimer(QTimer):
    def __init__(self, timel: QLabel, mover: QWidget, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.timel = timel
        self.mover = mover
    def timerEvent(self, a0: QTimerEvent | None) -> None:
        global start, end
        string = ''
        string += str(int((end-time())//60))
        string += 'min '
        string += str(round((end-time())%60))
        string += 's'
        self.timel.setText(string)
        if int(end-time()) % 400 <= 200:
            self.mover.setFixedSize(QSize(1, int(end-time()) % 400))
        else:
            self.mover.setFixedSize(QSize(1, 200 - int(end-time()) % 200))
        if end-time() < 0.5:
            brekwindow.close() #type: ignore
        if type(a0) == QTimerEvent:
            return a0.accept()
        else:
            return None


def pass_vars(vapp: QApplication):
    global app
    app = vapp

def brek(breaktime: int):
    global brekwindow, brektimer, start, end
    start = time()
    end = start+breaktime
    brekwindow = BrekWindow()
    brekwindow.setStyleSheet('background-color: black;')
    box = QVBoxLayout()
    box.setAlignment(Qt.AlignmentFlag.AlignTop)

    mover = QWidget()
    box.addWidget(mover)

    message = QLabel('Take a break and come back in:')
    font = message.font()
    font.setPixelSize(40)
    message.setFont(font)
    message.setStyleSheet('color: white;')
    box.addWidget(message)
    
    timel = QLabel('00min 00s')
    font = timel.font()
    font.setPixelSize(120)
    timel.setFont(font)
    timel.setStyleSheet('color: white;')
    box.addWidget(timel)

    brektimer = BrekTimer(timel, mover, brekwindow)
    brektimer.timerEvent(None)
    brektimer.startTimer(1000, Qt.TimerType.CoarseTimer)

    brekwindow.setLayout(box)
    brekwindow.showFullScreen()
    brekwindow.destroyed.connect(close)

def close():
    print('Caught')