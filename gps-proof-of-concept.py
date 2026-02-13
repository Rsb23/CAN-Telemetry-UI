from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox


class SerialGPSUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupWindowAttributes()
        self.setupUI()
    
    def setupWindowAttributes(self):
        self.setWindowTitle("Serial GPS")
        self.setGeometry(1280, 720, 150, 300)
    
    def setupUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)

        # top section of app, port config
        self.settingsGroupBox = QGroupBox()
        self.settingsGroupBox.
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qgroupbox.html