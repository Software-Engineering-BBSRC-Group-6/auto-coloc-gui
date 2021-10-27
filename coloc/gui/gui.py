import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
import os
import time

#path to output files - change this with the filepath received from the input script
filesPath = "/Users/cameronanderson/Documents/AA_Oxford_Notes/DPhil_Oxford/Courses_Year1/Software_Dev/coloc-gui/auto-coloc-gui/data/output"

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
        self._current_index = 0
        self._filenames = []
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(600,300)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Setup")
        self.tabs.addTab(self.tab2,"View")
        
        # TAB 1

        # Create Tab 1 - Setup
        self.tab1.layout = QGridLayout(self)

        # Define logo label
        self.logo = QLabel()
        pixmap = QPixmap('acg_logo.png')
        self.logo.setPixmap(pixmap)

        # Set instruction labels
        self.introLabel1 = QLabel('Welcome to Auto-Colloc-GUI!')
        self.introLabel1.setFont(QFont('Ariel',weight=QFont.Bold))
        self.introLabel2 = QLabel('\nInput .tif multiple channel fluorescent image data to run the automated colocalisation analysis:')
        self.introLabel2.setFont(QFont('Ariel',italic=True))
        self.introLabel3 = QLabel('\nDefine colocalisation parameters including clustering threshold and statistical analysis type:')
        self.introLabel3.setFont(QFont('Ariel',italic=True))

        # Create widgets for the setup tab inlcuding: labels, buttons, dropdowns, checkboxes, int input windows.
        self.openFile1 = QPushButton("Open File")
        self.openFile1Label = QLabel('Select Input Images (.tif):')
        self.fileLabel1 = QLabel()
        self.fileLabel1.setMaximumWidth(300)
        self.thresholdDropdown = QComboBox()
        self.thresholdLabel = QLabel('Select Threshold Value:')
        self.thresholdDropdown.addItems(["--Threshold Value--", "0.1 ", "0.2", "0.3", "0.4", "0.5 ", "0.6", "0.7", "0.8", "0.9"])
        self.channelsDropdown = QComboBox()
        self.channelsDropdownLabel = QLabel('Select Number of Channels:')
        self.channelsDropdown.addItems(["--Channel Number--", "1 ", "2", "3"])
        self.scaleDropdown = QComboBox()
        self.scaleDropdownLabel = QLabel("Select rough scale of image (in 'mu: \u03BC'):")
        self.scaleDropdown.addItems(["--Image Scale--", "1 ", "10", "50", "100", "500"])
        self.inputClusterNo = QPushButton("Select Value")
        self.inputClusterNoLabel = QLabel('Input Cluster Number:')
        self.clusterNoLabel = QLabel()
        self.clusterNoLabel.setMaximumWidth(300)
        self.intensitycorrCheckbox = QCheckBox()
        self.intensitycorrLabel = QLabel('Run Intensity Correlation Analysis:')
        self.kmeansCheckbox = QCheckBox()
        self.kmeansLabel = QLabel('Run KMeans Analysis:')
        self.runButton = QPushButton("Run")
        self.cancelButton = QPushButton("Stop")

        # Add widgets and define positioning on QGridLayout
        self.tab1.layout.addWidget(self.logo, 1, 3)
        self.tab1.layout.addWidget(self.introLabel1, 2, 3, 1, 2)
        self.tab1.layout.addWidget(self.introLabel2, 3, 2, 1, 2)
        self.tab1.layout.addWidget(self.openFile1, 4, 3)
        self.tab1.layout.addWidget(self.openFile1Label, 4, 2)
        self.tab1.layout.addWidget(self.fileLabel1, 4, 4, 1, 4)
        self.tab1.layout.addWidget(self.introLabel3, 5, 2, 1, 2)
        self.tab1.layout.addWidget(self.thresholdDropdown, 6, 3)
        self.tab1.layout.addWidget(self.thresholdLabel, 6, 2)
        self.tab1.layout.addWidget(self.channelsDropdown, 7, 3)
        self.tab1.layout.addWidget(self.channelsDropdownLabel, 7, 2)
        self.tab1.layout.addWidget(self.scaleDropdown, 8, 3)
        self.tab1.layout.addWidget(self.scaleDropdownLabel, 8, 2)
        self.tab1.layout.addWidget(self.inputClusterNo, 9, 3)
        self.tab1.layout.addWidget(self.inputClusterNoLabel, 9, 2)
        self.tab1.layout.addWidget(self.clusterNoLabel, 9, 4, 1, 4)
        self.tab1.layout.addWidget(self.intensitycorrCheckbox, 10, 3)
        self.tab1.layout.addWidget(self.intensitycorrLabel, 10, 2)
        self.tab1.layout.addWidget(self.kmeansCheckbox, 11, 3)
        self.tab1.layout.addWidget(self.kmeansLabel, 11, 2)
        self.tab1.layout.addWidget(self.runButton, 12, 6)
        self.tab1.layout.addWidget(self.cancelButton, 12, 5)
        self.tab1.setLayout(self.tab1.layout)

        # Disable/'grey-out' widgets
        self.cancelButton.setDisabled(True)
        self.fileLabel1.setDisabled(True)
        self.clusterNoLabel.setDisabled(True)
            
        # Define path as empty for later use
        self.in_path = 'Empty'

        # Connect GUI buttons to respective functions
        self.openFile1.clicked.connect(self.define_file_path)
        self.inputClusterNo.clicked.connect(self.define_cluster_number)
        self.runButton.clicked.connect(self.run_program)

        #TAB 2

        #Create Tab 2 - View
        self.tab2.layout = QGridLayout(self)

        #Creates objects to be displayed
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.label = QLabel()

        # Add widgets and define positioning on QGridLayout
        self.tab2.layout.addWidget(self.previous_button, 0, 0)
        self.tab2.layout.addWidget(self.next_button, 0, 3)
        self.tab2.layout.addWidget(self.label, 1, 1, 1, 2)
        self.tab2.setLayout(self.tab2.layout)

        #handles button click events
        self.previous_button.clicked.connect(self.handle_previous)
        self.next_button.clicked.connect(self.handle_next)
        self._update_button_status(False, True)

        #Loads data in from the filepath
        self.load_files(filesPath) #Make this into the outpath after testing

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    # TAB 1 - INPUT FUNCTIONS

    def define_file_path(self):
        '''
        This function uses the file path that the user selects as input to define in_path and out_path variables
        as well as labelling the GUI with the selected file name to confirm file selection.
        '''
        self.in_path = QFileDialog.getOpenFileName(self,"Choose TIF File To Open","E:\\")[0]
        self.out_path = self.in_path.replace(os.path.basename(self.in_path), "")
        self.fileLabel1.setText('{}'.format(os.path.basename(self.in_path)))
    
    def define_cluster_number(self):
        '''
        This cluster labels the GUI with the user's cluster number input to confirm data entry.
        '''
        self.clusterInput, bool_info = QInputDialog.getInt(self, 'Integer Input Dialog', 'Enter cluster number:', 1, 10, 50, 10)
        self.clusterNoLabel.setText(str(self.clusterInput))

    def start_animation(self):
        '''
        This function loads the loading.gif file as a movie attached to a label widget. The function adds the 
        widget and then starts the .gif file to create movement.
        '''
        self.loading = QLabel()
        self.gif = QMovie('loading.gif')
        self.loading.setMovie(self.gif)
        self.tab1.layout.addWidget(self.loading, 12, 7)
        self.gif.start()

    def stop_animation(self):
        '''
        This function stops the loading.gif movie and deletes the loading gif label so that the loading 
        sign disappears.
        '''
        self.gif.stop()
        self.tab1.layout.removeWidget(self.loading)
        self.loading = None

    def create_channels(self):
        '''
        This function creates the attribute channel_list from the user inputted number of channels from the
        dropdown menu. 
        '''
        self.channel_list = []
        for i in range(int(self.channels_value)):
            self.channel_list.append(int(i))
        
    def create_dict(self):
        '''
        This file creates a dictionary of the user inputs which can be fed to the model and visualiser functions.
        '''
        dict_data = {}
        dict_data["in_path"] = self.in_path
        dict_data["out_path"] = self.out_path
        dict_data["threshold"] = float(self.thresholdDropdown.currentText())
        self.create_channels()
        dict_data["channels"] = self.channel_list
        dict_data["num_clusts"] = int(self.clusterInput)
        dict_data["min_dist"] = 10/float(self.scaleDropdown.currentText()) #This converts scale in microns to pixel distance between clusters
        dict_data["visualise"] = True
        if self.kmeansCheckbox.isChecked():
            dict_data["Run KMeans"] = "Y"
        else:
            dict_data["Run KMeans"] = "N"
        if self.intensitycorrCheckbox.isChecked():
            dict_data["Run Intensity Correlation Analysis"] = "Y"
        else:
            dict_data["Run Intensity Correlation Analysis"] = "N"

        self.dict_data = dict_data

    def check_errors(self):
        '''
        This function ensures that the user inputs are all complete. It checks that an input .tif file has been selected. It
        also checks that necessary parameters have been selected for the model to run.
        '''
        # Access threshold and chennels inputs
        threshold_value = str(self.thresholdDropdown.currentText())
        channels_value = str(self.channelsDropdown.currentText())
        scale_value = str(self.scaleDropdown.currentText())

        # Create Error message widgets
        inputMsg = QMessageBox()
        parameterMsg = QMessageBox()
        analysisMsg = QMessageBox()

        inputMsg.setIcon(QMessageBox.Critical)
        inputMsg.setText("Input Error")
        inputMsg.setInformativeText('Please ensure a valid .tif file input is selected')
        inputMsg.setWindowTitle("Input Error")

        parameterMsg.setIcon(QMessageBox.Critical)
        parameterMsg.setText("Input Error")
        parameterMsg.setInformativeText('Please ensure all parameters have been selected')
        parameterMsg.setWindowTitle("Input Error")

        analysisMsg.setIcon(QMessageBox.Critical)
        analysisMsg.setText("Input Error")
        analysisMsg.setInformativeText('Please ensure at least one statistical analysis has been checked/selected')
        analysisMsg.setWindowTitle("Input Error")

        # Set conditions for error messages to be delivered. Set booleans for check_error function to read. 
        if self.in_path is 'Empty' or os.path.splitext(self.in_path)[1] not in ['.tif']:
            inputMsg.exec_()
            return False
        elif threshold_value in ['--Threshold Value--'] or channels_value in ['--Channel Number--'] or scale_value in ['--Image Scale--'] or len(self.clusterNoLabel.text()) == 0:
            parameterMsg.exec_()
            return False
        elif self.kmeansCheckbox.isChecked() == False and self.intensitycorrCheckbox.isChecked() == False:
            analysisMsg.exec_()
            return False
        else:
            return True

    def cancel_clicked(self):
        ''' 
        This function is activated when the cancel button is clicked. It switches the activation of the run/cancel buttons and terminates
        the loading .gif animation.
        '''
        self.runButton.setDisabled(False)
        self.cancelButton.setDisabled(True)
        self.stop_animation()

    def run_program(self):
        '''
        This function is the overall controller of the script. It checks for input errors by calling the check_errors function. 
        If this passes, the function creates the input dictionary, calls the model and the visualiser to display the results.
        '''
        if self.check_errors() is False:
            return
        else:
            self.start_animation()
            self.runButton.setDisabled(True)
            self.cancelButton.setDisabled(False)
            self.cancelButton.clicked.connect(self.cancel_clicked)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            self.out_path = self.out_path + "acg_output_{}".format(timestamp)
            os.mkdir(self.out_path)
            self.out_path = self.out_path + "/"
            self.create_dict()
            print(self.dict_data)
            """
            danFunction(self.dict_data)
            amitFunction(self.out_path)
            """


    # TAB 2 - VISUALISER FUNCTIONS

    def load_files(self, filesPath):
        '''
        Loads the files in from filesPath and
        sets the index counter to 0
        '''
        for file in os.listdir(filesPath):
            if file.endswith(".png"):
                self._filenames.append(os.path.join(filesPath, file))
        self._filenames = sorted(self._filenames)
        print (self._filenames)
        self.current_index = 0

    def handle_next(self):
        '''
        Adds one to the index counter
        (moves forward in directory)
        '''
        self.current_index += 1

    def handle_previous(self):
        '''
        Subtracts one from the index
        (moves backward in directory)
        '''
        self.current_index -= 1

    @property
    def current_index(self):
        '''
        Determines what the current index is
        '''
        return self._current_index

    @current_index.setter
    def current_index(self, index):
        '''
        Allows for movement between the 
        files and greying out of buttons
        '''
        if index <= 0:
            self._update_button_status(False, True)
        elif index >= (len(self._filenames) - 1):
            self._update_button_status(True, False)
        else:
            self._update_button_status(True, True)

        if 0 <= index < len(self._filenames):
            self._current_index = index
            filename = self._filenames[self._current_index]
            pixmap = QPixmap(filename)
            self.label.setPixmap(pixmap)

    def _update_button_status(self, previous_enable, next_enable):
        '''
        Updates the button state
        '''
        self.previous_button.setEnabled(previous_enable)
        self.next_button.setEnabled(next_enable)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())