import sys
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget

#path to output files
filesPath = "/home/amit/auto-coloc-gui/coloc/gui/images"


class Widget(QWidget):
    def __init__(self, parent=None):
        '''
        Creates the objects and buttons that are displayed 
        and groups them into a grid
        '''
        super().__init__(parent)
        self._current_index = 0
        self._filenames = []
        
        #Creates objects to be displayed
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.label = QLabel()

        #Sets layout in grid format
        layout = QGridLayout(self)
        layout.addWidget(self.previous_button, 0, 0)
        layout.addWidget(self.next_button, 0, 2)
        layout.addWidget(self.label, 1, 1, 1, 2)

        #handles button click events
        self.previous_button.clicked.connect(self.handle_previous)
        self.next_button.clicked.connect(self.handle_next)
        self._update_button_status(False, True)

        #Loads data in from the filepath
        self.load_files(filesPath)

    def load_files(self, filesPath):
        '''
        Loads the files in from filesPath and
        sets the index counter to 0
        '''
        for file in os.listdir(filesPath):
            if file.endswith(".jpeg"):
                self._filenames.append(os.path.join(filesPath, file))

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())