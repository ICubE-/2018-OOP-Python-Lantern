#Menubar
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu
from PyQt5.QtCore import QCoreApplication

class Exam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()#create statusbar
        self.statusBar().showMessage("something")#take instance an showmessage

        menu = self.menuBar()#create menubar
        menu_file = menu.addMenu('File')#adding menu, creating group
        menu_edit = menu.addMenu('Edit')

        file_exit = QAction('Exit', self) #create instance
        file_exit.setShortcut('Ctrl+Q') #setting hot key
        file_exit.setStatusTip("something to quit")#view Tips

        file_exit.triggered.connect(QCoreApplication.instance().quit)#When it's selected

        file_new = QMenu('New', self)#make subgroup

        new_txt = QAction('text file', self)#make sub menu
        new_py = QAction('python file', self)

        file_new.addAction(new_py)#add sub menu
        file_new.addAction(new_txt)

        menu_file.addAction(file_exit)
        menu_file.addMenu(file_new)#creat Menu group
        self.resize(450,400)
        self.show()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())