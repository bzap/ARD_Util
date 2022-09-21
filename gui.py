import sys
from PySide6 import QtCore, QtWidgets, QtGui
from graph import create_samples
from web_scraper import web_scraper
from word_freq import word_cloud

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.samples = []
        self.setWindowTitle("ARD Util")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.tab_collection = QtWidgets.QTabWidget()
        self.asin_tab = QtWidgets.QWidget()
        self.cloud_tab = QtWidgets.QWidget()
        self.asin_tab_widgets()
        self.cloud_tab_widgets() 
        self.tab_collection.addTab(self.asin_tab, "ASIN Operations")
        self.tab_collection.addTab(self.cloud_tab, "Word Cloud")
        self.layout.addWidget(self.tab_collection)

    def asin_tab_widgets(self):
        lookup_header = self.create_header("Translation to Name", 10, 0, 10, 0, 0)
        lookup_input = self.create_input('lookup_text', "ASIN Lookup: ", self.fetch_name)
        self.lookup_text = lookup_input[0]
        lookup_layout = lookup_input[1]
        self.output = QtWidgets.QTextEdit(self) 
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(29)
        query_input = self.create_input('query_text', "ASIN Query: ", self.fetch_books)
        self.query_text = query_input[0]
        queryLayout = query_input[1]
        self.table = QtWidgets.QTableWidget()
        c_headers = [QtWidgets.QTableWidgetItem('Item ' + str(x + 1)) for x in range(0, 10)]
        self.table.setRowCount(10)
        self.table.setColumnCount(1)
        self.table.setAlternatingRowColors(True)
        h_header = self.table.horizontalHeader()
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["ASIN"])
        for i in range(0, len(c_headers)): 
            v_item = QtWidgets.QTableWidgetItem('Item ' + str(i + 1))
            v_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setVerticalHeaderItem(i, v_item)
        self.table.show() 
        table_header = self.create_header("Related Items by Review Word Similarity", 10, 0, 20, 0, 0)
        lookup_div = self.create_div("lookup_div")
        query_div = self.create_div("query_div")
        layout = QtWidgets.QVBoxLayout() 
        layout.addWidget(lookup_header)
        layout.addWidget(lookup_div)
        layout.addLayout(lookup_layout)
        layout.addWidget(self.output)
        layout.addWidget(table_header)
        layout.addWidget(query_div)
        layout.addLayout(queryLayout)
        layout.addWidget(self.table)
        layout.setContentsMargins(10,10,10,30)
        self.asin_tab.setLayout(layout) 

    def cloud_tab_widgets(self): 
        lookup_input = self.create_input('cloud_text', "ASIN Lookup: ", self.gen_wordcloud)
        lookup_layout = lookup_input[1]
        self.cloud_text = lookup_input[0]
        self.image = QtWidgets.QLabel(self)
        self.image.setContentsMargins(0,10,0,0)
        self.image.setAlignment(QtCore.Qt.AlignCenter)        
        lookup_header = self.create_header("Generate a Wordcloud by Review Term Frequency", 0, 0, 20, 0, 10)
        cloud_div = self.create_div("cloud_div")
        layout = QtWidgets.QVBoxLayout() 
        layout.addWidget(lookup_header)
        layout.addWidget(cloud_div)
        layout.addLayout(lookup_layout)
        layout.addStretch(1)
        layout.addWidget(self.image)
        layout.setContentsMargins(10,10,10,30)
        self.cloud_tab.setLayout(layout)

    def create_samples(self, asin): 
        return create_samples(asin)

    def create_div(self, name): 
        div = QtWidgets.QFrame() 
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setFrameShadow(QtWidgets.QFrame.Sunken)
        div.setObjectName(name)
        return div

    def create_header(self, name, margin, left, top, bottom, right): 
        header = QtWidgets.QLabel(name)
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setObjectName(name)
        header.setMargin(margin)
        header.setContentsMargins(left, top, bottom, right)
        return header

    def create_input(self, name, text, func): 
        layout = QtWidgets.QHBoxLayout()
        input = QtWidgets.QLineEdit()
        input.setObjectName(name)
        button = QtWidgets.QPushButton(">")
        layout.addWidget(QtWidgets.QLabel(text)) 
        layout.addWidget(input)
        layout.addWidget(button)
        button.clicked.connect(func)
        return [input, layout]

    def populate_table(self): 
        for i in range(len(self.samples)): 
            item = QtWidgets.QTableWidgetItem(self.samples[i])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(0, i, item)

    @QtCore.Slot()
    def fetch_name(self): 
        self.output.setText(web_scraper(self.lookup_text.text()))
        self.output.setAlignment(QtCore.Qt.AlignCenter)
    
    @QtCore.Slot()
    def fetch_books(self): 
        self.samples = create_samples(self.query_text.text())
        self.populate_table()

    @QtCore.Slot()
    def gen_wordcloud(self): 
        word_cloud(self.cloud_text.text())
        pixmap = QtGui.QPixmap('word_cloud.png')
        self.image.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())