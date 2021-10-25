import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

filesPath = "/home/amit/auto-coloc-gui/coloc/gui/images"

images=[]

def getFiles(path):
    for file in os.listdir(path):
        if file.endswith(".jpeg"):
            images.append(os.path.join(path, file))

class App(QWidget):
    def __init__(self):
        super().__init__()

        getFiles(filesPath)
        images.reverse()

        layout = QGridLayout(self)
        pic = QLabel(self)
        pic.setAlignment(Qt.AlignCenter)
        text = QLabel("Original")
        text.setAlignment(Qt.AlignCenter)
        pic.setPixmap(QPixmap(images[0]))
        pic.move(20,90)
        text.move(20,0)
        layout.addWidget((pic), 0, 0)
        layout.addWidget((text), 1, 0)

        pic1 = QLabel(self)
        pic1.setPixmap(QPixmap(images[1]))
        pic1.setAlignment(Qt.AlignCenter)
        text1 = QLabel("Colocalised",)
        text1.setAlignment(Qt.AlignCenter)
        pic1.move(400,0)
        text1.move(400,0)
        layout.addWidget((pic1), 0, 1)
        layout.addWidget((text1), 1, 1)

        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) 