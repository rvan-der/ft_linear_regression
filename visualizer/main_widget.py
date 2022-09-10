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
		self.normalizedData = normalize_data(self.data, self.weights)
		self.dataSeries = None

		self.layout = QHBoxLayout()

		self.chartView = QChartView()
		self.chart = self.chartView.chart()

		self.yAxis = QValueAxis()
		self.yAxis.setRange(0, 10000)
		self.yAxis.setTickType(QValueAxis.TicksDynamic)
		self.yAxis.setTickAnchor(0)
		self.yAxis.setTickInterval(1000)

		self.xAxis = QValueAxis()
		self.xAxis.setRange(20000, 260000)
		self.xAxis.setTickType(QValueAxis.TicksDynamic)
		self.xAxis.setTickAnchor(20000)
		self.xAxis.setTickInterval(20000)

		self.chart.addAxis(self.xAxis, Qt.AlignBottom)
		self.chart.addAxis(self.yAxis, Qt.AlignLeft)

		self.commandWidget = CommandWidget()

		self.layout.addWidget(self.commandWidget, stretch=1)
		self.layout.addWidget(self.chartView, stretch=3)
		self.setLayout(self.layout)
		self.plot_data()


	def plot_data(self):
		if self.dataSeries != None:
			self.chart.removeSeries(self.dataSeries)
			self.dataSeries = None
		self.dataSeries = QScatterSeries()
		self.dataSeries.setName("Car prices")
		for car in self.data:
			self.dataSeries.append(car["km"], car["price"])
		self.chart.addSeries(self.dataSeries)
		self.dataSeries.attachAxis(self.xAxis)
		self.dataSeries.attachAxis(self.yAxis)
