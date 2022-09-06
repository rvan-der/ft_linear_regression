from PySide6.QtWidgets import QWidget, QHBoxLayout



class PlotWidget(QWidget):
	def __init__(self):
		QWidget.__init__()
		self.layout = QHBoxLayout()
