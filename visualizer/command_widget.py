from PySide6.QtWidgets import QPushButton, QGridLayout, QLabel, QSpinBox, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Slot, Signal


class CommandWidget(QFrame):

	warning = Signal(str)

	def __init__(self, theta0, theta1):
		QFrame.__init__(self)

		self.theta0 = theta0
		self.theta1 = theta1

		self.setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.setLineWidth(3)

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.layout.setVerticalSpacing(50)
		self.layout.setContentsMargins(15, 80, 15, 80)

		self.trainLabel = QLabel("Number of iterations (max 10^8)")

		self.trainInput = QSpinBox()
		self.trainInput.setRange(0,100000000)
		self.trainInput.setSingleStep(50)

		self.trainButton = QPushButton("Launch Training")
		self.trainButton.setStyleSheet("background-color: green")
		self.trainButton.setMaximumHeight(50)
		self.trainButton.setMinimumHeight(50)
		self.trainButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.trainButton.clicked.connect(self.test)

		self.theta0Label = QLabel("<font size=25 color=red>θ<sub>0</sub> = %.3f</font>"%(self.theta0))
		self.theta0Label.setTextFormat(Qt.RichText)

		self.theta1Label = QLabel("<font size=25 color=red>θ<sub>1</sub> = %.3f</font>"%(self.theta1))
		self.theta1Label.setTextFormat(Qt.RichText)

		self.layout.addWidget(self.trainLabel, 0, 0, 1, 1, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.trainInput, 0, 1, 1, 1, alignment=Qt.AlignRight)
		self.layout.addWidget(self.trainButton, 1, 0, 1, 2)
		self.layout.setRowMinimumHeight(2, 80)
		self.layout.addWidget(self.theta0Label, 3, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.theta1Label, 4, 0, 1, 2, alignment=Qt.AlignLeft)
		
		self.setLayout(self.layout)


	def disableTrainButton(self):
		self.trainButton.setEnabled(False)


	def enableTrainButton(self):
		self.trainButton.setEnabled(True)


	def update_thetas(self, theta0, theta1):
		self.theta0 = theta0
		self.theta1 = theta1
		self.theta0Label.setText("<font size=30 color=red>θ<sub>0</sub> = %.3f</font>"%(self.theta0))
		self.theta1Label.setText("<font size=30 color=red>θ<sub>1</sub> = %.3f</font>"%(self.theta1))


	@Slot()
	def test(self):
		print("test")
		print(self.trainInput.value())
		self.warning.emit("This is a test")