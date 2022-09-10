from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self, widget=None):
        QMainWindow.__init__(self)
        self.setWindowTitle("ft_linear_regression")
        if widget:
            self.setCentralWidget(widget)
        self.status = self.statusBar()
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.6, geometry.height() * 0.7)
        self.displayStatusMsg("Ready to regress in a linear fashion !")

        # self.menu = self.menuBar()
        # self.file_menu = self.menu.addMenu("File")


    def displayStatusMsg(self, message):
        self.status.showMessage(message)

