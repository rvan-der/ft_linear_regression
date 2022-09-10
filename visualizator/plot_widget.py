from PySide6.QtCharts import QChartView, QChart, QValueAxis, QScatterSeries, QLineSeries


class PlotWidget(QChartView):

	def __init__(self, data, weights):
		super(PlotWidget).__init__()
		self.data = data
		self.weights = weights
		self.dataSeries = None
		self.setChart(QChart())
		self.chart = self.chart()
		self.plot_data()


	def plot_data(self):
		if self.dataSeries != None:
			self.chart.removeSeries(self.dataSeries)
			self.dataSeries = None
		self.dataSeries = QScatterSeries()
		for car in data:
			self.dataSeries.append(car["km"], car["price"])
		self.chart.addSeries(self.dataSeries)