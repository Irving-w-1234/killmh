import sys
import os
import psutil
import signal
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class MyApp(QWidget):
    count_backwards = ''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('定时关闭进程')
        # 创建两个输入框并设置默认值
        hb = QHBoxLayout()
        self.label1 = QLabel("要执行的进程")
        self.label1.setMinimumWidth(80)
        self.label1.setAlignment(Qt.AlignRight)
        self.le1 = QLineEdit('mhmain.exe', self)

        hb.addWidget(self.label1)
        hb.addWidget(self.le1)

        hb2 = QHBoxLayout()
        self.label2 = QLabel("时间(分钟)")
        self.label2.setMinimumWidth(80)
        self.label2.setAlignment(Qt.AlignRight)
        self.le2 = QLineEdit('240', self)

        hb2.addWidget(self.label2)
        hb2.addWidget(self.le2)

        # 创建一个按钮
        self.btn = QPushButton('执行', self)
        self.btn.clicked.connect(self.print_values)

        self.btn2 = QPushButton('停止', self)
        self.btn2.clicked.connect(self.func_stop_timer)
        self.btn2.setDisabled(True)
        self.count_backwards = self.le2.text()
        self.label3 = QLabel(f"{int(self.count_backwards) * 60}")

        # 使用垂直布局来放置这些部件
        layout = QVBoxLayout()
        layout.addLayout(hb)
        layout.addLayout(hb2)
        layout.addWidget(self.label3)
        layout.addWidget(self.btn)
        layout.addWidget(self.btn2)
        self.setLayout(layout)

    def print_values(self):
        print("开始定时器")
        self.le1.setDisabled(True)
        self.le2.setDisabled(True)
        self.btn.setDisabled(True)
        self.btn2.setDisabled(False)

        self.timer = QTimer()
        val = self.le2.text()

        self.timer.start(int(val) * 60 * 1000)  # 开始计时器

        # ---------------------定时执行-----------------------
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_kill_mh)  # 当时间间隔过去后，触发delayed_function

        # ---------------------倒计时-----------------------
        self.count_backwards = int(val) * 60
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.countdown)
        self.timer2.setInterval(1000)
        self.timer2.start()

    def func_stop_timer(self):
        self.le1.setDisabled(False)
        self.le2.setDisabled(False)
        self.btn.setDisabled(False)
        self.btn2.setDisabled(True)

        print("停止定时器")
        self.timer.stop()
        self.timer2.stop()

    def countdown(self, ):

        if self.count_backwards > 0:
            self.count_backwards -= 1
            self.label3.setText(f'{self.count_backwards}秒')
        else:
            self.le1.setDisabled(False)
            self.le2.setDisabled(False)
            self.btn.setDisabled(False)
            self.btn2.setDisabled(True)
            self.timer.stop()
            self.timer2.stop()
            self.label3.setText('已完成')

    def start_kill_mh(self):
        # 获取输入框的值并打印
        proc = []
        pros_name = self.le1.text()

        for p in psutil.process_iter(['pid', 'name']):

            if pros_name.lower() == p.name().lower():
                proc.append((p.pid, p.name()))

        if len(proc) == 0:
            QMessageBox.critical(self, '错误', '没有找到该进程')
            return

        for pid, name in proc:
            try:
                print(name, pid)
                os.kill(pid, signal.SIGTERM)
                break
            except OSError as e:
                print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
