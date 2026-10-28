from PyQt6.QtCore import QTimer, QTimerEvent
from PyQt6.QtWidgets import QLabel, QProgressBar
from datetime import datetime
import api_interact

class UserSettings():
    def __init__(self):
        self._b_i = 3600
    def breakInterval(self) -> int:
        return self._b_i

class TimeTimer(QTimer):
    def __init__(self, parent, time: QLabel, hours: QLabel, brek: QLabel, progress: QProgressBar, settings: UserSettings):
        super().__init__(parent)
        self.time = time
        self.hours = hours
        self.brek = brek
        self.progress = progress
        self.bi = settings.breakInterval()
    def timerEvent(self, a0: QTimerEvent | None) -> None:
        string = ''
        string += str(datetime.now().hour)
        string += '\n'
        string += str(datetime.now().minute)
        self.time.setText(string)

        total, goal, tracked = api_interact.get_total_time_and_goal()
        string = ''
        string += str(tracked//3600)
        string += '/'
        string += str(goal//3600)
        string += ' hours'
        self.hours.setText(string)

        string = 'Break in: '
        string += str(total % self.bi)
        string += ' min'
        self.brek.setText(string)

        self.progress.setValue(int(tracked/goal*100))
        if type(a0) == QTimerEvent:
            return a0.accept() #type: ignore
        else:
            return None