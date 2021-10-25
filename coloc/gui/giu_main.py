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
        self.thresholdDropdown = QComboBox()
        self.thresholdLabel = QLabel('Select Threshold Value:') #Add a check that this is a float
        self.statsDropdown = QComboBox()
        self.statsDropdownLabel = QLabel('Select Colocalisation Statistic:')
        self.runButton = QPushButton("Run")
        self.cancelButton = QPushButton("Stop")
        
        self.tab1.layout.addWidget(self.openFile1, 1, 3)
        self.tab1.layout.addWidget(self.openFile1Label, 1, 2)
        self.tab1.layout.addWidget(self.fileLabel1, 1, 4)
        self.tab1.layout.addWidget(self.thresholdDropdown, 2, 3)
        self.tab1.layout.addWidget(self.thresholdLabel, 2, 2)
        self.tab1.layout.addWidget(self.statsDropdown, 3, 3)
        self.tab1.layout.addWidget(self.statsDropdownLabel, 3, 2)
        self.tab1.layout.addWidget(self.runButton, 6, 6)
        self.tab1.layout.addWidget(self.cancelButton, 6, 5)
        self.tab1.setLayout(self.tab1.layout)

        self.thresholdDropdown.addItems(["--Threshold Value--", "0.1 ", "0.2", "0.3", "0.4", "0.5 ", "0.6", "0.7", "0.8", "0.9"])
        self.statsDropdown.addItems(["--Statistical Method--", "Pearson ", "Spearman", "Wilcoxon"])

        #If all values are filled, activate run
        self.runButton.setDisabled(True)
        self.cancelButton.setDisabled(True)

        self.openFile1.clicked.connect(self.define_file_path)
        self.runButton.clicked.connect(self.run_program)
        
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
    
    def run_program(self):
        #create dict
            # path_in; path_out; flt(threshold); stats
        #Start spinny wheel/ progress bar
        #Activate cancel 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    