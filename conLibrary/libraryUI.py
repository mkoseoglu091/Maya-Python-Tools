from .controllerLibrary import ControllerLibrary
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
import pprint
# from Qt import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """
    ControllerLibraryUI is a QDialog that lets users save and import controllers
    """

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')

        # an instance of the controller library
        self.library = ControllerLibrary()

        # automatically build and populate the library
        self.buildUI()
        self.populate()

    def buildUI(self):
        # master alyout
        layout = QtWidgets.QVBoxLayout(self)

        # child horizontal widget
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # Parameters for thumbnail size and spacing
        size = 64
        buffer = 12

        # Grid list widget that displays controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        layout.addWidget(self.listWidget)

        # child widget that holds all buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """
        Clears the list widget and repopulates it
        """
        self.library = ControllerLibrary()
        self.listWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        """
        Loads currently selected conrtoller into the scene
        """
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """
        Saves controller with provided file name
        """
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name")

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')


def showUI():
    """
    Shows and returns a handle for the UI
    :return: QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui
