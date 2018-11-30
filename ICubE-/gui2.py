from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit,QInputDialog, QApplication

class ChooseNickname(QWidget):
    def __init__(self):
        super().__init__(self)
        self.initUI()

    def initUI(self):
        input_box = QLineEdit()

app = QApplication([])
dialog = QInputDialog()
dialog.show()
app.exec_()