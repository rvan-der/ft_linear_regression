import sys

from PySide6.QtWidgets import QApplication
from visualizer.main_window import MainWindow
from visualizer.main_widget import MainWidget
from io_tools import *



def launch_visualizer():
    try:
        data = read_csv("data.csv")
    except Exception as e:
        print_error_msg("Couldn't load the data:\n" + str(e) + "\nexiting...", _exit=True)

    try:
        weights = load_weights()
    except Exception as e:
        print_warning_msg("Warning:\n" + str(e) + " Weights are set to 0.")
        weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}

    app = QApplication([])
    central_widget = MainWidget(data, weights)
    main_window = MainWindow(central_widget)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    launch_visualizator()
