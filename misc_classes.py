from PyQt6.QtCore import QTimer, QTimerEvent
from PyQt6.QtWidgets import QLabel, QProgressBar, QApplication
from datetime import datetime
from time import process_time
import api_interact
import brek

class UserSettings():
    def __init__(self):
        self._b_i = 3600
        self._waka = False
        self._goal = 3600
        self._tracked = 0
        self._b_t = 300
    def setBreakInterval(self, interval: int):
        self._b_i = interval
    def breakInterval(self) -> int:
        return self._b_i
    def setBreakTime(self, breaktime: int):
        self._b_t = breaktime
    def breakTime(self):
        return self._b_t
    def setCallWakatime(self, v: bool):
        self._waka = v
    def callWakatime(self) -> bool:
        return self._waka
    def setGoal(self, goal: int):
        self._goal = goal
    def goal(self):
        return self._goal
    def setTracked(self, tracked: int):
        self._tracked = tracked
    def tracked(self):
        return self._tracked

class TimeTimer(QTimer):
    def __init__(self, parent, time: QLabel, hours: QLabel, brekl: QLabel, progress: QProgressBar, settings: UserSettings, app: QApplication):
        super().__init__(parent)
        self.time = time
        self.hours = hours
        self.brek = brekl
        self.progress = progress
        self.settings = settings
        self.selftime = 3590
        brek.pass_vars(app)
    def timerEvent(self, a0: QTimerEvent | None) -> None:
        string = ''
        string += str(datetime.now().hour)
        string += '\n'
        string += str(datetime.now().minute)
        self.time.setText(string)

        if self.settings.callWakatime():
            total, goal, tracked = api_interact.get_total_time_and_goal()
        else:
            total = self.selftime
            goal = self.settings.goal()
            tracked = self.settings.tracked()
        string = ''
        string += str(tracked//3600)
        string += '/'
        string += str(goal//3600)
        string += ' hours'
        self.hours.setText(string)

        string = 'Break in: '
        string += str((self.settings.breakInterval() - self.selftime % self.settings.breakInterval()) // 60)
        string += ' min'
        self.brek.setText(string)

        self.progress.setValue(int(tracked/goal*100))
        print(self.settings.breakInterval() - self.selftime % self.settings.breakInterval())
        if self.settings.breakInterval() - self.selftime % self.settings.breakInterval() == 3600 and\
        self.selftime != 0:
            brek.brek(self.settings.breakTime())
            self.selftime = -self.settings.breakInterval()
        self.selftime += 1
        if type(a0) == QTimerEvent:
            return a0.accept() #type: ignore
        else:
            return None