import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn=QPushButton('Click', self)
        btn.resize(btn.sizeHint())#sizeHint : change by letters
        btn.move(20, 30)
        self.show()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())