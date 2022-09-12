from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QScatterSeries, QLineSeries
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Slot, QThreadPool

from visualizer.command_widget import CommandWidget
from parsing_tools import *
from normalizer import normalize_data
from trainer_qrunnable import Trainer



class MainWidget(QWidget):
	def __init__(self, data, weights):
		QWidget.__init__(self)

		self.threadpool = QThreadPool()
		self.data = data
		self.weights = weights
		self.normalizedData = normalize_data(self.data, self.weights)
		self.theta0 = 0
		self.theta1 = 0
		self.calculate_thetas()

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
		self.dataSeries.setName("Car prices")
		self.dataSeries.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
		self.dataSeries.setColor(QColor("blue"))
		self.dataSeries.setMarkerSize(8)
		self.dataSeries.attachAxis(self.xAxis)
		self.dataSeries.attachAxis(self.yAxis)

		self.modelSeries = QLineSeries()
		self.chart.addSeries(self.modelSeries)
		self.modelSeries.setName("Model")
		self.modelSeries.setColor(QColor("red"))
		self.modelSeries.attachAxis(self.xAxis)
		self.modelSeries.attachAxis(self.yAxis)


		self.commandWidget = CommandWidget(self.theta0, self.theta1)
		self.commandWidget.trainButton.clicked.connect(self.launch_training)

		self.mainLayout.addWidget(self.commandWidget, stretch=1)
		self.mainLayout.addWidget(self.chartView, stretch=4)
		self.setLayout(self.mainLayout)
		self.plot_data()
		self.plot_model()


	@Slot()
	def launch_training(self):
		self.commandWidget.disableTrainButton()
		nbIterations = self.commandWidget.trainInput.value()
		trainer = Trainer(self.weights, self.normalizedData, nbIterations)
		trainer.signals.weights_updated.connect(self.update_weights)
		trainer.signals.job_finished.connect(self.update_weights)
		trainer.signals.job_finished.connect(self.commandWidget.enableTrainButton)
		self.threadpool.start(trainer)


	@Slot(dict)
	def update_weights(self, weights):
		self.weights = weights
		self.calculate_thetas()
		self.commandWidget.update_thetas(self.theta0, self.theta1)
		self.plot_model()


	def plot_data(self):
		self.dataSeries.clear()
		for car in self.data:
			self.dataSeries.append(car["km"], car["price"])


	def plot_model(self):
		self.modelSeries.clear()
		self.modelSeries.append(0, self.theta0)
		self.modelSeries.append(260000, self.theta1 * 260000 + self.theta0)
		# print(260000, self.theta1 * 260000 + self.theta0)
		# print(self.theta0, self.theta1)


	def calculate_thetas(self):
		self.theta0 = self.weights["theta0"] * self.weights["norm_factor"]
		endPointValue = (self.weights["theta1"] * (260000 / max(1,self.weights["norm_factor"])) + self.weights["theta0"]) * self.weights["norm_factor"]
		self.theta1 = (endPointValue - self.theta0) / 260000
