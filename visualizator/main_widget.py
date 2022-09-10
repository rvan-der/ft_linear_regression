from PySide6.QtWidgets import QWidget, QHBoxLayout
from parsing_tools import *



class MainWidget(QWidget):
	def __init__(self, data, weights):
		super(PlotWidget).__init__()
		self.layout = QHBoxLayout()
		self.plot = PlotWidget(self.data, self.weights)
		self.QHBoxLayout.addWidget(self.plot)