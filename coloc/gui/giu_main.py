import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont
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

        self.logo = QLabel()
        pixmap = QPixmap('acg_logo.png')
        self.logo.setPixmap(pixmap)
        self.introLabel1 = QLabel('Welcome to Auto-Colloc-GUI!')
        self.introLabel1.setFont(QFont('Ariel',weight=QFont.Bold))
        self.introLabel2 = QLabel('\nInput .tiff multiple channel fluorescent image data to run the automated colocalisation analysis:')
        self.introLabel2.setFont(QFont('Ariel',italic=True))
        self.introLabel3 = QLabel('\nDefine colocalisation parameters including clustering threshold and statistical analysis type:')
        self.introLabel3.setFont(QFont('Ariel',italic=True))
        # Input .tiff multiple channel fluorescent image data to run the automated colocalisation analysis:
        # self.introLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.openFile1 = QPushButton("Open File")
        self.openFile1Label = QLabel('Select Input Images (.tiff):')
        self.fileLabel1 = QLabel()
        self.fileLabel1.setMaximumWidth(100)
        self.thresholdDropdown = QComboBox()
        self.thresholdLabel = QLabel('Select Threshold Value:')
        self.statsDropdown = QComboBox()
        self.statsDropdownLabel = QLabel('Select Colocalisation Statistic:')
        self.runButton = QPushButton("Run")
        self.cancelButton = QPushButton("Stop")
        
        self.tab1.layout.addWidget(self.logo, 1, 3)
        self.tab1.layout.addWidget(self.introLabel1, 2, 3, 1, 2)
        self.tab1.layout.addWidget(self.introLabel2, 3, 2, 1, 2)
        self.tab1.layout.addWidget(self.openFile1, 4, 3)
        self.tab1.layout.addWidget(self.openFile1Label, 4, 2)
        self.tab1.layout.addWidget(self.fileLabel1, 4, 4, 1, 4)
        self.tab1.layout.addWidget(self.introLabel3, 5, 2, 1, 2)
        self.tab1.layout.addWidget(self.thresholdDropdown, 6, 3)
        self.tab1.layout.addWidget(self.thresholdLabel, 6, 2)
        self.tab1.layout.addWidget(self.statsDropdown, 7, 3)
        self.tab1.layout.addWidget(self.statsDropdownLabel, 7, 2)
        self.tab1.layout.addWidget(self.runButton, 8, 6)
        self.tab1.layout.addWidget(self.cancelButton, 8, 5)
        self.tab1.setLayout(self.tab1.layout)

        self.thresholdDropdown.addItems(["--Threshold Value--", "0.1 ", "0.2", "0.3", "0.4", "0.5 ", "0.6", "0.7", "0.8", "0.9"])
        self.statsDropdown.addItems(["--Statistical Method--", "Pearson ", "Spearman", "Wilcoxon"])

        #If all values are filled, activate run
        self.runButton.setDisabled(True)
        self.cancelButton.setDisabled(True)
        self.fileLabel1.setDisabled(True)

        self.openFile1.clicked.connect(self.define_file_path)
        # self.runButton.clicked.connect(self.run_program)
        
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
        self.out_path = self.in_path.replace(os.path.basename(self.in_path), "")
        # Changed in_path to out_path
        self.fileLabel1.setText('{}'.format(os.path.basename(self.in_path)))
        # print(self.in_path)
        # print(self.out_path)

    def create_dict(self):
        dict_data = {}
        dict_data["in_path"] = self.in_path
        dict_data["out_path"] = self.out_path
        dict_data["threshold"] = float(self.threshold)
        dict_data["statistic"] = self.statistics
    
    def run_program(self):
        self.create_dict()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    