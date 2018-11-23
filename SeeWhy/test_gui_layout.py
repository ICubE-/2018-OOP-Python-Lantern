#Layout
import sys
from PyQt5.QyWidgets import QWidget, QLabel, QApplication

class Example(QWidget):
    def __init_(self):
        super().__init__()
        self.iniUI()

    def initUI(self):
        lbl1 = QLabel('zetdfjk', self)
        lbl1.move(15,10)
        
        lbl2 = QLabel('zetdfjk', self)
        lbl2.move(35,40)
        
        lbl3 = QLabel('zetdfjk', self)
        lbl3.move(45,70)