from PySide6.QtWidgets import QMainWindow, QStyle
from PySide6.QtCore import Slot, QUrl
from PySide6.QtGui import QDesktopServices, QKeySequence


class MainWindow(QMainWindow):

    def __init__(self, widget):

        super(MainWindow, self).__init__()

        self.setWindowTitle("ft_linear_regression")

        self.mainWidget = widget
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.status_msg.connect(self.displayStatusMsg)

        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)

        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.7, geometry.height() * 0.7)
        self.displayStatusMsg("Ready to regress in a linear fashion !", 10000)

        self.menuBar = self.menuBar()
        
        self.fileMenu = self.menuBar.addMenu("File")
        resetIcon = self.style().standardIcon(QStyle.SP_BrowserReload)
        self.resetAction = self.fileMenu.addAction(resetIcon, "Reset model to zero", self.mainWidget.reset_model, shortcut=QKeySequence.Refresh)
        quitIcon = self.style().standardIcon(QStyle.SP_BrowserStop)
        self.quitAction = self.fileMenu.addAction(quitIcon, "Quit", self.close, shortcut=QKeySequence.Close)
        
        self.infoMenu = self.menuBar.addMenu("Info")
        self.infoMenu.setStyleSheet("color:blue")
        self.regressionLinkAction = self.infoMenu.addAction("Linear regression", self.open_regression_link)
        self.mseLinkAction = self.infoMenu.addAction("Mean Squared Error", self.open_mse_link)
        self.descentLinkAction = self.infoMenu.addAction("Gradient descent", self.open_descent_link)

        linkFont = self.mseLinkAction.font()
        linkFont.setUnderline(True)
        linkFont.setItalic(True)
        self.mseLinkAction.setFont(linkFont)
        self.regressionLinkAction.setFont(linkFont)
        self.descentLinkAction.setFont(linkFont)



    @Slot(str, int)
    def displayStatusMsg(self, message, timeoutms):
        self.statusBar.showMessage(message, timeoutms)

    @Slot()
    def open_mse_link(self):
        QDesktopServices.openUrl(QUrl("https://en.wikipedia.org/wiki/Mean_squared_error"))


    @Slot()
    def open_regression_link(self):
        QDesktopServices.openUrl(QUrl("https://en.wikipedia.org/wiki/Linear_regression"))


    @Slot()
    def open_descent_link(self):
        QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=3wh_TLzuiRI&list=PL10NOnsbP5Q7wNrYItE2GhKq05cVov97e"))
