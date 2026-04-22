import matplotlib.pyplot as plt

from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from ui.plot_tab import PlotTab
from ui.hist2d_tab import Hist2dTab
from ui.fonts_tab import FontsTab


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure(figsize=(12.8, 9.6))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Matplotlib properties viewer')

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        tabs.addTab(PlotTab(MplCanvas()), 'Plot')
        tabs.addTab(Hist2dTab(MplCanvas()), 'Hist2D')
        tabs.addTab(FontsTab(MplCanvas()), 'Fonts')

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()

        width = int(geometry.width() * 0.8)
        height = int(geometry.height() * 0.8)

        self.resize(width, height)
