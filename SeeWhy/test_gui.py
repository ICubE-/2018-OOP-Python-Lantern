import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #create button
        btn=QPushButton('Click', self)
        btn.resize(btn.sizeHint())#sizeHint : change by letters
        btn.setToolTip('툴팁입니다.<br>Hello</br>')#when you put your mouse on the button
        btn.move(20, 30)#set button location

        self.setGeometry(300,300,400,500)#set window size
        self.setWindowTitle('Floweytale')#set window name

        self.show()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())