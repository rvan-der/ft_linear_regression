import sys

from PySide6.QtWidgets import QApplication
from visualizer.main_window import MainWindow
from visualizer.main_widget import MainWidget
from parsing_tools import *



def launch_visualizer():
    try:
        data = read_csv("data.csv")
    except DataLoadingError as err:
        print_error_msg("Couldn't load the data:\n" + err.message + "\nexiting...", _exit=True)
    except:
        print_error_msg("Couldn't load the data.\nexiting...", _exit=True)

    try:
        weights = load_weights()
    except WeightsLoadingError as err:
        print_warning_msg("Warning:\n" + err.message + " Weights are set to 0.")
        weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}
    except:
        print_warning_msg("Warning:\nCouldn't load the weights. Weights are set to 0.")
        weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}

    app = QApplication([])
    central_widget = MainWidget(data, weights)
    main_window = MainWindow(central_widget)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    launch_visualizer()
