from PySide6.QtWidgets import QWidget
from PySide6.Qt import QHBoxLayout



class PlotWidget(QWidget):
	def __init__(self):
		QWidget.__init__()
		self.layout = QHBoxLayout()
