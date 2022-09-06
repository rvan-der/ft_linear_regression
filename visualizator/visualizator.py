from PySide6.QtWidgets import QApplication
from visualizator.main_window import MainWindow
from visualizator.plot_widget import PlotWidget



def launch_visualizator():
    app = QApplication([])

    central_widget = PlotWidget()
    main_window = MainWindow()
    main_window.show()

    app.exec()

if __name__ == "__main__":
    launch_visualizator()
