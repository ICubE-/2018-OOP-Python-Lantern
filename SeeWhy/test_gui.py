#button
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication

class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #create button
        btn=QPushButton('Click', self)
        btn.resize(btn.sizeHint())#sizeHint : change by letters
        btn.setToolTip('툴팁입니다.<br>Hello</br>')#when you put your mouse on the button
        btn.move(150, 200)#set button location

        btn.clicked.connect(QCoreApplication.instance().quit)#When button is clicked, the App ends

        self.setGeometry(300,300,400,500)#set window size... or self.resize()
        self.setWindowTitle('Floweytale')#set window name

        self.show()

    def closeEvent(self, QCloseEvent):#When the program shuts down
        ans = QMessageBox.question(self, "종료확인", "종료하시겠습니까?",#Event Window name, message
                                   QMessageBox.Yes|QMessageBox.No, QMessageBox.No)#buttons, initial selecting

        if ans==QMessageBox.Yes:
            QCloseEvent.accept()#make it off
        else:
            QCloseEvent.ignore()#keep it on

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())