from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QScatterSeries, QLineSeries
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt
# from visualizer.plot_widget import PlotWidget
from visualizer.command_widget import CommandWidget
from parsing_tools import *
from normalizer import normalize_data
# from trainer import Trainer



class MainWidget(QWidget):
	def __init__(self, data, weights):
		QWidget.__init__(self)

		self.data = data
		self.weights = weights
		self.theta0 = 0
		self.theta1 = 0
		self.calculate_thetas()
		self.normalizedData = normalize_data(self.data, self.weights)
		self.dataSeries = None
		self.modelSeries = None

		self.mainLayout = QHBoxLayout()

		self.chartView = QChartView()
		self.chart = self.chartView.chart()

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

		tickLabelsFont = self.font()
		tickLabelsFont.setPointSize(7)
		self.xAxis.setLabelsFont(tickLabelsFont)
		self.yAxis.setLabelsFont(tickLabelsFont)

		self.chart.addAxis(self.xAxis, Qt.AlignBottom)
		self.chart.addAxis(self.yAxis, Qt.AlignLeft)

		self.commandWidget = CommandWidget(self.theta0, self.theta1)

		self.mainLayout.addWidget(self.commandWidget, stretch=1)
		self.mainLayout.addWidget(self.chartView, stretch=3)
		self.setLayout(self.mainLayout)
		self.plot_data()
		self.plot_model()


	def plot_data(self):
		if self.dataSeries != None:
			self.chart.removeSeries(self.dataSeries)
			self.dataSeries = None
		self.dataSeries = QScatterSeries()
		self.dataSeries.setName("Car prices")
		self.dataSeries.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
		self.dataSeries.setMarkerSize(8)
		for car in self.data:
			self.dataSeries.append(car["km"], car["price"])
		self.chart.addSeries(self.dataSeries)
		self.dataSeries.attachAxis(self.xAxis)
		self.dataSeries.attachAxis(self.yAxis)
		self.dataSeries.setColor(QColor("blue"))


	def plot_model(self):
		if self.modelSeries != None:
			self.chart.removeSeries(self.modelSeries)
			self.modelSeries = None
		self.modelSeries = QLineSeries()
		self.modelSeries.setName("Model")
		self.modelSeries.append(0, self.theta0)
		self.modelSeries.append(260000, self.theta1 * 260000 + self.theta0)
		# print(260000, self.theta1 * 260000 + self.theta0)
		# print(self.theta0, self.theta1)
		self.chart.addSeries(self.modelSeries)
		self.modelSeries.attachAxis(self.xAxis)
		self.modelSeries.attachAxis(self.yAxis)
		self.modelSeries.setColor(QColor("red"))


	def calculate_thetas(self):
		self.theta0 = self.weights["theta0"] * self.weights["norm_factor"]
		endPointValue = (self.weights["theta1"] * (260000 / max(1,self.weights["norm_factor"])) + self.weights["theta0"]) * self.weights["norm_factor"]
		self.theta1 = (endPointValue - self.theta0) / 260000
