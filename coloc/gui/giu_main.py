import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'ACG Tools'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(600,300)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Setup")
        self.tabs.addTab(self.tab2,"View")
        
        # Create first tab
        self.tab1.layout = QGridLayout(self)

        self.openFile1 = QPushButton("Open File")
        self.openFile1Label = QLabel('Select Input File:')
        self.thresholdInput = QLineEdit()
        self.thresholdInput.setPlaceholderText("0.1 <= Threshold <= 0.9")
        self.thresholdLabel = QLabel('Input Threshold Value:') #Add a check that this is a float
        self.dropdown1 = QComboBox()
        self.dropdownLabel = QLabel('Select Colocalisation Statistic:')
        self.checkBox1 = QCheckBox()
        self.checkboxLabel = QLabel('Save Output?')
        self.openFile2 = QPushButton("Open Folder")
        self.openFile2Label = QLabel('Select Output Folder:')
        self.runButton = QPushButton("Run")
        self.cancelButton = QPushButton("Cancel")
        
        self.tab1.layout.addWidget(self.openFile1, 1, 3)
        self.tab1.layout.addWidget(self.openFile1Label, 1, 2)
        self.tab1.layout.addWidget(self.thresholdInput, 2, 3)
        self.tab1.layout.addWidget(self.thresholdLabel, 2, 2)
        self.tab1.layout.addWidget(self.dropdown1, 3, 3)
        self.tab1.layout.addWidget(self.dropdownLabel, 3, 2)
        self.tab1.layout.addWidget(self.checkBox1, 4, 3)
        self.tab1.layout.addWidget(self.checkboxLabel, 4,2)
        self.tab1.layout.addWidget(self.openFile2, 5, 3)
        self.tab1.layout.addWidget(self.openFile2Label, 5, 2)
        self.tab1.layout.addWidget(self.runButton, 6, 5)
        self.tab1.layout.addWidget(self.cancelButton, 6, 4)
        self.tab1.setLayout(self.tab1.layout)

        self.openFile1.clicked.connect(self.define_file_path)
        self.openFile2.clicked.connect(self.define_directory_path)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    def define_file_path(self):
        self.in_path = QFileDialog.getOpenFileName(self,"Choose TIF File To Open","E:\\")[0]
    
    def define_directory_path(self):
        self.out_path = QFileDialog.getExistingDirectory(self,"Choose Directory To Save","E:\\")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    