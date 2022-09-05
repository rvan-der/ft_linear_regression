from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from plot_widget import PlotWidget


if __name__ == "__main__":
    app = QApplication([])

    central_widget = PlotWidget()
    main_window = MainWindow()
    main_window.show()

    app.exec()
