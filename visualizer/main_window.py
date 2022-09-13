from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, Slot


class MainWindow(QMainWindow):

    def __init__(self, widget):
        super(MainWindow, self).__init__()
        self.mainWidget = widget
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("ft_linear_regression")
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.7, geometry.height() * 0.7)
        self.displayStatusMsg("Ready to regress in a linear fashion !", 10000)
        self.mainWidget.status_msg.connect(self.displayStatusMsg)

        # self.menu = self.menuBar()
        # self.file_menu = self.menu.addMenu("File")


    @Slot(str, int)
    def displayStatusMsg(self, message, timeoutms):
        self.statusBar.showMessage(message, timeoutms)
