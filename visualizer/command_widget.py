from PySide6.QtWidgets import QPushButton, QGridLayout, QLabel, QSpinBox, QFrame, QSizePolicy, QAbstractSpinBox, QDoubleSpinBox
from PySide6.QtCore import Qt, Signal
from io_tools import condensed_notation


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
		self.totalIterations = 0

		self.setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.setLineWidth(3)

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.layout.setVerticalSpacing(25)
		self.layout.setContentsMargins(15, 40, 15, 40)

		self.learningRateLabel = QLabel("Learning rate")
		self.learningRateInput = QDoubleSpinBox()
		self.learningRateInput.setDecimals(3)
		self.learningRateInput.setRange(0.001, 2)
		self.learningRateInput.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
		self.learningRateInput.setValue(0.1)

		self.trainLabel = QLabel("Iterations (max 10^8)  ")
		self.trainInput = SpinboxEnter(0, 100000000)
		self.trainInput.setValue(1)

		self.trainButton = QPushButton("Launch Training")
		self.trainButton.setStyleSheet("background-color: green")
		trainButtonFont = self.font()
		trainButtonFont.setPointSize(16)
		self.trainButton.setFont(trainButtonFont)
		self.trainButton.setMaximumHeight(50)
		self.trainButton.setMinimumHeight(50)
		self.trainButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		self.totalIterationsLabel = QLabel("Total iterations: 0")

		self.theta0Label = QLabel("<font size=%d color=red>θ<sub>0</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.theta0, 12)))
		self.theta0Label.setTextFormat(Qt.RichText)

		self.theta1Label = QLabel("<font size=%d color=red>θ<sub>1</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.theta1, 12)))
		self.theta1Label.setTextFormat(Qt.RichText)

		self.modelErrorLabel = QLabel("<font size=%d>Err = %s</font>"%(self.modelFontSize, condensed_notation(self.modelError, 10)))
		self.modelErrorLabel.setToolTip("Mean Squared Error")

		self.gradient_t0Label = QLabel("<font size=%d>dErr/dθ<sub>0</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.gradient_t0, 9)))
		self.gradient_t0Label.setTextFormat(Qt.RichText)

		self.gradient_t1Label = QLabel("<font size=%d>dErr/dθ<sub>1</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.gradient_t1, 9)))
		self.gradient_t1Label.setTextFormat(Qt.RichText)

		self.layout.addWidget(self.learningRateLabel, 0, 0, 1, 1, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.learningRateInput, 0, 1, 1, 1, alignment=Qt.AlignRight)
		self.layout.addWidget(self.trainLabel, 1, 0, 1, 1, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.trainInput, 1, 1, 1, 1, alignment=Qt.AlignRight)
		self.layout.addWidget(self.trainButton, 2, 0, 1, 2)
		self.layout.addWidget(self.totalIterationsLabel, 3, 0, 1, 1, alignment=Qt.AlignLeft)
		self.layout.setRowMinimumHeight(4, 30)
		self.layout.addWidget(QLabel("<font size=%d><u>Model:</u></font>"%(self.modelFontSize)), 4, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.theta0Label, 6, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.theta1Label, 7, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.modelErrorLabel, 8, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.gradient_t0Label, 9, 0, 1, 2, alignment=Qt.AlignLeft)
		self.layout.addWidget(self.gradient_t1Label, 10, 0, 1, 2, alignment=Qt.AlignLeft)
		
		self.setLayout(self.layout)


	def disableTrainButton(self):
		self.trainButton.setEnabled(False)


	def enableTrainButton(self):
		self.trainButton.setEnabled(True)


	def update_thetas(self, theta0, theta1):
		self.theta0 = theta0
		self.theta1 = theta1
		self.theta0Label.setText("<font size=%d color=red>θ<sub>0</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.theta0, 12)))
		self.theta1Label.setText("<font size=%d color=red>θ<sub>1</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.theta1, 12)))

	
	def update_error(self, modelError):
		self.modelError = modelError
		self.modelErrorLabel.setText("<font size=%d>Err = %s</font>"%(self.modelFontSize, condensed_notation(self.modelError, 10)))

	
	def update_gradients(self, gradient_t0, gradient_t1):
		self.gradient_t0 = gradient_t0
		self.gradient_t1 = gradient_t1
		self.gradient_t0Label.setText("<font size=%d>dErr/dθ<sub>0</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.gradient_t0,9)))
		self.gradient_t1Label.setText("<font size=%d>dErr/dθ<sub>1</sub> = %s</font>"%(self.modelFontSize, condensed_notation(self.gradient_t1,9)))


	def update_total_iterations(self, iterations):
		self.totalIterations = iterations
		self.totalIterationsLabel.setText("Total iterations: %d"%(self.totalIterations))


	def increment_total_iterations(self, increment):
		self.update_total_iterations(self.totalIterations + increment)