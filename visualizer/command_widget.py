from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QSpinBox
from PySide6.QtCore import Qt


class CommandWidget(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignTop)
		self.trainButton = QPushButton("Launch Training")
		self.trainLabel = QLabel("Number of iterations (max 10^8)")
		self.trainInput = QSpinBox()
		self.trainInput.setRange(1,100000000)
		self.trainInput.setSingleStep(50)
		self.layout.addWidget(self.trainLabel,0,0,1,1, alignment=Qt.AlignHCenter)
		self.layout.addWidget(self.trainInput,0,1,1,1, alignment=Qt.AlignHCenter)
		self.layout.addWidget(self.trainButton,2,0,1,2, alignment=Qt.AlignHCenter)
		self.layout.setRowMinimumHeight(1,30)
		self.layout.setContentsMargins(15,30,15,30)
		self.setLayout(self.layout)
