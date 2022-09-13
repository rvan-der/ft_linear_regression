from PySide6.QtWidgets import QPushButton, QGridLayout, QLabel, QSpinBox, QFrame, QSizePolicy, QAbstractSpinBox
from PySide6.QtCore import Qt, Slot, Signal


class SpinboxEnter(QSpinBox):

	enter_pressed = Signal()

	def __init__(self, _min, _max):
		super(SpinboxEnter, self).__init__()
		self.setRange(_min, _max)
		self.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

	def keyReleaseEvent(self, event):
		if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
			self.enter_pressed.emit()
		super(SpinboxEnter, self).keyReleaseEvent(event)



class CommandWidget(QFrame):

	def __init__(self, theta0, theta1, modelError, gradient_t0, gradient_t1):
		super(CommandWidget, self).__init__()

		self.modelError = modelError
		self.theta0 = theta0
		self.theta1 = theta1
		self.gradient_t0 = gradient_t0
		self.gradient_t1 = gradient_t1
		self.modelFontSize = 5

		self.setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.setLineWidth(3)

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.layout.setVerticalSpacing(30)
		self.layout.setContentsMargins(15, 60, 15, 60)

		self.trainLabel = QLabel("Iterations (max 10^8)")

		self.trainInput = SpinboxEnter(0, 100000000)

		self.trainButton = QPushButton("Launch Training")
		self.trainButton.setStyleSheet("background-color: green")
		trainButtonFont = self.font()
		trainButtonFont.setPointSize(16)
		self.trainButton.setFont(trainButtonFont)
		self.trainButton.setMaximumHeight(50)
		self.trainButton.setMinimumHeight(50)
		self.trainButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		self.theta0Label = QLabel("<font size=%d color=red>θ<sub>0</sub> = %.3f</font>"%(self.modelFontSize, self.theta0))
		self.theta0Label.setTextFormat(Qt.RichText)

		self.theta1Label = QLabel("<font size=%d color=red>θ<sub>1</sub> = %.3f</font>"%(self.modelFontSize, self.theta1))
		self.theta1Label.setTextFormat(Qt.RichText)

		self.gradient_t0Label = QLabel("<font size=%d>dE/dθ<sub>0</sub> = %.3f</font>"%(self.modelFontSize, self.gradient_t0))
		self.gradient_t0Label.setTextFormat(Qt.RichText)

		self.gradient_t1Label = QLabel("<font size=%d>dE/dθ<sub>1</sub> = %.3f</font>"%(self.modelFontSize, self.gradient_t1))
		self.gradient_t1Label.setTextFormat(Qt.RichText)

		self.modelErrorLabel = QLabel("<font size=%d>E = %.3f</font>"%(self.modelFontSize, self.modelError))
		self.modelErrorLabel.setToolTip("Mean Squared Error")

		self.layout.addWidget(self.trainLabel, 0, 0, 1, 1, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.trainInput, 0, 1, 1, 1, alignment=Qt.AlignRight)
		self.layout.addWidget(self.trainButton, 1, 0, 1, 2)
		self.layout.setRowMinimumHeight(2, 30)
		self.layout.addWidget(QLabel("<font size=%d><u>Model:</u></font>"%(self.modelFontSize)), 3, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.theta0Label, 4, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.theta1Label, 5, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.modelErrorLabel, 6, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.gradient_t0Label, 7, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.gradient_t1Label, 8, 0, 1, 2, alignment=Qt.AlignLeft)
		
		self.setLayout(self.layout)


	def disableTrainButton(self):
		self.trainButton.setEnabled(False)


	def enableTrainButton(self):
		self.trainButton.setEnabled(True)


	def update_thetas(self, theta0, theta1):
		self.theta0 = theta0
		self.theta1 = theta1
		self.theta0Label.setText("<font size=%d color=red>θ<sub>0</sub> = %.3f</font>"%(self.modelFontSize, self.theta0))
		self.theta1Label.setText("<font size=%d color=red>θ<sub>1</sub> = %.3f</font>"%(self.modelFontSize, self.theta1))

	
	def update_error(self, modelError):
		self.modelError = modelError
		self.modelErrorLabel.setText("<font size=%d>E = %.3f</font>"%(self.modelFontSize, self.modelError))

	
	def update_gradients(self, gradient_t0, gradient_t1):
		self.gradient_t0 = gradient_t0
		self.gradient_t1 = gradient_t1
		self.gradient_t0Label.setText("<font size=%d>dE/dθ<sub>0</sub> = %.3f</font>"%(self.modelFontSize, self.gradient_t0))
		self.gradient_t1Label.setText("<font size=%d>dE/dθ<sub>1</sub> = %.3f</font>"%(self.modelFontSize, self.gradient_t1))
