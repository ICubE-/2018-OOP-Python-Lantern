#Layout
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel('zetdfjk', self)
        lbl1.move(15,10)
        
        lbl2 = QLabel('zetdfjk', self)
        lbl2.move(35,40)
        
        lbl3 = QLabel('zetdfjk', self)
        lbl3.move(45,70)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Absolute')
        self.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())