import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
import os

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
        self.openFile1Label = QLabel('Select Input Images (.tiff):')
        self.fileLabel1 = QLabel()
        self.fileLabel1.setMaximumWidth(100)
        self.thresholdInput = QLineEdit()
        self.thresholdInput.setPlaceholderText("0.1 <= Threshold <= 0.9")
        self.thresholdLabel = QLabel('Input Threshold Value:') #Add a check that this is a float
        self.dropdown1 = QComboBox()
        self.dropdownLabel = QLabel('Select Colocalisation Statistic:')
        self.runButton = QPushButton("Run")
        self.cancelButton = QPushButton("Stop")
        
        self.tab1.layout.addWidget(self.openFile1, 1, 3)
        self.tab1.layout.addWidget(self.openFile1Label, 1, 2)
        self.tab1.layout.addWidget(self.fileLabel1, 1, 4)
        self.tab1.layout.addWidget(self.thresholdInput, 2, 3)
        self.tab1.layout.addWidget(self.thresholdLabel, 2, 2)
        self.tab1.layout.addWidget(self.dropdown1, 3, 3)
        self.tab1.layout.addWidget(self.dropdownLabel, 3, 2)
        self.tab1.layout.addWidget(self.runButton, 6, 6)
        self.tab1.layout.addWidget(self.cancelButton, 6, 5)
        self.tab1.setLayout(self.tab1.layout)

        self.dropdown1.addItems(["--Statistical Method--", "Pearson ", "Spearman", "Wilcoxon"])


        self.runButton.setDisabled(True)
        self.cancelButton.setDisabled(True)

        self.openFile1.clicked.connect(self.define_file_path)
        
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
        self.fileLabel1.setText('{}'.format(self.in_path))
        self.out_path = os.path.basename(self.in_path)
    
    def define_directory_path(self):
        self.out_path = QFileDialog.getExistingDirectory(self,"Choose Directory To Save","E:\\")
    
    def activate_save_output(self):
        if self.checkBox1.isChecked():
            self.openFile2.setDisabled(False)
            self.openFile2Label.setDisabled(False)
        else:
            self.openFile2.setDisabled(True)
            self.openFile2Label.setDisabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    