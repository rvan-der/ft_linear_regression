from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QScatterSeries, QLineSeries
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Slot, Signal, QThreadPool

from visualizer.command_widget import CommandWidget
from parsing_tools import *
from normalizer import normalize_data
from trainer_qrunnable import Trainer



class MainWidget(QWidget):

	status_msg = Signal(str, int)

	def __init__(self, data, weights):
		super(MainWidget, self).__init__()

		self.threadpool = QThreadPool()
		self.data = data
		self.weights = weights
		self.normalizedData = normalize_data(self.data, self.weights)
		self.theta0 = 0
		self.theta1 = 0
		self.calculate_thetas()
		self.modelError = 0
		self.calculate_error()
		self.gradient_t0 = 0
		self.gradient_t1 = 0
		self.calculate_gradients()

		self.mainLayout = QHBoxLayout()

		self.chartView = QChartView()
		self.chart = self.chartView.chart()
		self.chartView.setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.chartView.setLineWidth(3)
		self.chart.layout().setContentsMargins(0,0,0,0)

		self.yAxis = QValueAxis()
		self.yAxis.setTitleText("Price")
		self.yAxis.setLabelFormat("%d")
		self.yAxis.setRange(-1000, 10000)
		self.yAxis.setTickType(QValueAxis.TicksDynamic)
		self.yAxis.setTickAnchor(-1000)
		self.yAxis.setTickInterval(1000)

		self.xAxis = QValueAxis()
		self.xAxis.setTitleText("Distance (km)")
		self.xAxis.setLabelFormat("%d")
		self.xAxis.setLabelsAngle(-45)
		self.xAxis.setRange(0, 260000)
		self.xAxis.setTickType(QValueAxis.TicksDynamic)
		self.xAxis.setTickAnchor(0)
		self.xAxis.setTickInterval(20000)

		axesLabelsFont = self.font()
		axesLabelsFont.setPointSize(7)
		self.xAxis.setLabelsFont(axesLabelsFont)
		self.yAxis.setLabelsFont(axesLabelsFont)

		self.chart.addAxis(self.xAxis, Qt.AlignBottom)
		self.chart.addAxis(self.yAxis, Qt.AlignLeft)

		self.dataSeries = QScatterSeries()
		self.chart.addSeries(self.dataSeries)
		self.dataSeries.setName("Car prices (data) ")
		self.dataSeries.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
		self.dataSeries.setColor(QColor("blue"))
		self.dataSeries.setMarkerSize(8)
		self.dataSeries.attachAxis(self.xAxis)
		self.dataSeries.attachAxis(self.yAxis)

		self.modelSeries = QLineSeries()
		self.chart.addSeries(self.modelSeries)
		self.modelSeries.setName("Y = θ<sub>1</sub>X + θ<sub>0</sub> (model)")
		self.modelSeries.setColor(QColor("red"))
		self.modelSeries.attachAxis(self.xAxis)
		self.modelSeries.attachAxis(self.yAxis)

		self.commandWidget = CommandWidget(self.theta0, self.theta1, self.modelError, self.gradient_t0, self.gradient_t1)
		self.commandWidget.trainButton.clicked.connect(self.launch_training)
		self.commandWidget.trainInput.enter_pressed.connect(self.launch_training)

		self.mainLayout.addWidget(self.commandWidget, stretch=1)
		self.mainLayout.addWidget(self.chartView, stretch=5)
		self.setLayout(self.mainLayout)
		self.plot_data()
		self.plot_model()


	@Slot()
	def launch_training(self):
		self.status_msg.emit("Training the model...", 0)
		self.commandWidget.disableTrainButton()
		nbIterations = self.commandWidget.trainInput.value()
		trainer = Trainer(self.weights, self.normalizedData, nbIterations)
		trainer.signals.weights_updated.connect(self.update_weights)
		trainer.signals.job_finished.connect(self.update_weights)
		trainer.signals.job_finished.connect(self.training_finished)
		self.threadpool.start(trainer)

	@Slot(dict)
	def update_weights(self, weights):
		self.weights = weights
		self.calculate_thetas()
		self.commandWidget.update_thetas(self.theta0, self.theta1)
		self.calculate_error()
		self.commandWidget.update_error(self.modelError)
		self.calculate_gradients()
		self.commandWidget.update_gradients(self.gradient_t0, self.gradient_t1)
		self.plot_model()


	@Slot()
	def training_finished(self):
		self.status_msg.emit("Training finished !", 5000)
		try:
			save_weights(self.weights)
		except Exception as e:
			self.status_msg("WARNING ! " + str(e), 10000)
			print_warning_msg("WARNING ! " + str(e))
		self.commandWidget.enableTrainButton()


	def plot_data(self):
		self.dataSeries.clear()
		for car in self.data:
			self.dataSeries.append(car["km"], car["price"])


	def plot_model(self):
		self.modelSeries.clear()
		self.modelSeries.append(0, self.theta0)
		self.modelSeries.append(260000, self.theta1 * 260000 + self.theta0)


	def calculate_thetas(self):
		self.theta0 = self.weights["theta0"] * self.weights["norm_factor"]
		endPointValue = (self.weights["theta1"] * (260000 / max(1,self.weights["norm_factor"])) + self.weights["theta0"]) * self.weights["norm_factor"]
		self.theta1 = (endPointValue - self.theta0) / 260000


	def calculate_error(self):
		self.modelError = sum([(car["price"] - (self.theta1 * car["km"] + self.theta0))**2 for car in self.data]) / len(self.data)

	def calculate_gradients(self):
		dataSize = len(self.data)
		gradient_t0, gradient_t1 = 0, 0
		for car in self.data:
			estimation = self.theta1 * car["km"] + self.theta0
			gradient_t0 += estimation - car["price"]
			gradient_t1 += (estimation - car["price"]) * car["km"]
		gradient_t0 /= -dataSize
		gradient_t1 /= -dataSize
		self.gradient_t0 = gradient_t0
		self.gradient_t1 = gradient_t1
