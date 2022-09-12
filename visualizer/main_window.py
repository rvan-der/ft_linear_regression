from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, Slot


class MainWindow(QMainWindow):

    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.mainWidget = widget
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("ft_linear_regression")
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.6, geometry.height() * 0.7)
        self.displayStatusMsg("Ready to regress in a linear fashion !")
        self.mainWidget.commandWidget.warning.connect(self.displayWarningMsg)

        # self.menu = self.menuBar()
        # self.file_menu = self.menu.addMenu("File")


    def displayStatusMsg(self, message):
        self.statusBar.showMessage(message)


    @Slot(str)
    def displayWarningMsg(self, message):
        text = "<font color=yellow>Warning: "+message+"<font/>"
        self.displayStatusMsg(text)

