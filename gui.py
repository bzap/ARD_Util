import sys
import random
from PySide6 import QtCore, QtSvgWidgets, QtWidgets, QtGui
from graph import create_samples
from web_scraper import web_scraper
from word_freq import word_cloud

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.samples = []
        self.setWindowTitle("Amazon Review Dataset Utility")
        self.layout = QtWidgets.QVBoxLayout(self)



        # need to make this div modular 

        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab1ui()
        self.tab2ui() 
        

        self.tabs.addTab(self.tab1, "ASIN Operations")
        self.tabs.addTab(self.tab2, "Word Cloud")
        self.layout.addWidget(self.tabs)



    def create_samples(self, asin): 
        return create_samples(asin)





    def create_div(self, name): 
        div = QtWidgets.QFrame() 
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setFrameShadow(QtWidgets.QFrame.Sunken)
        div.setObjectName(name)
        return div

    # CREATE METHODS FOR THE HEADER NAME AND THE INPUT BOX USING PARAMETERS LIKE THIS 
    def create_input(self, text): 
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel(text))   

    def tab1ui(self):

        lookupHeader = QtWidgets.QLabel("Translation to Name")
        lookupHeader.setAlignment(QtCore.Qt.AlignCenter)
        lookupHeader.setMargin(10)
        lookupHeader.setContentsMargins(0,10,0,0)


        inputLayout = QtWidgets.QHBoxLayout() 
       # inputLayout.setContentsMargins(0,20,0,0)
        inputLayout.addWidget(QtWidgets.QLabel("ASIN Lookup: "))
        self.textIn = QtWidgets.QLineEdit()
        inputLayout.addWidget(self.textIn)
        asinButton = QtWidgets.QPushButton(">")
        inputLayout.addWidget(asinButton)
        asinButton.clicked.connect(self.fetch_name)

        self.output = QtWidgets.QTextEdit(self) 
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(29)
        
        #inputLayout.addWidget

        queryLayout = QtWidgets.QHBoxLayout() 
        #queryLayout.setContentsMargins(0,30,0,0)
        queryLayout.addWidget(QtWidgets.QLabel("ASIN Query: "))
        self.textQe = QtWidgets.QLineEdit()
        queryLayout.addWidget(self.textQe)
        queryButton = QtWidgets.QPushButton(">")
        queryLayout.addWidget(queryButton)
        queryButton.clicked.connect(self.magic)        
        

        self.table = QtWidgets.QTableWidget()
        headers = [QtWidgets.QTableWidgetItem('Item ' + str(x + 1)) for x in range(0, 10)]

        self.table.setRowCount(10)
        self.table.setColumnCount(1)
        self.table.setAlternatingRowColors(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["ASIN"])
        self.table.setVerticalHeaderItem(1, QtWidgets.QTableWidgetItem("lol"))
        for i in range(0, len(headers)): 
            vitem = QtWidgets.QTableWidgetItem('Item ' + str(i + 1))
            vitem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setVerticalHeaderItem(i, vitem)
        self.table.show() 
        

        tableHeader = QtWidgets.QLabel("Related Items by Review Word Similarity")
        tableHeader.setAlignment(QtCore.Qt.AlignCenter)
        tableHeader.setMargin(10)
        tableHeader.setContentsMargins(0,20,0,0)

        lookupDiv = self.create_div("lookupDiv")
        queryDiv = self.create_div("queryDiv")

        layout = QtWidgets.QVBoxLayout() 
        layout.addWidget(lookupHeader)
        layout.addWidget(lookupDiv)
        layout.addLayout(inputLayout)
        layout.addWidget(self.output)
        layout.addWidget(tableHeader)
        layout.addWidget(queryDiv)
        layout.addLayout(queryLayout)
        layout.addWidget(self.table)
        layout.setContentsMargins(10,10,10,30)

        self.tab1.setLayout(layout)  

    def populate_table(self): 
        for i in range(len(self.samples)): 
            item = QtWidgets.QTableWidgetItem(self.samples[i])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(0, i, item)


    def tab2ui(self): 
        self.ilabel = QtWidgets.QLabel(self)
        self.ilabel.setContentsMargins(0,10,0,0)
        inputLayout = QtWidgets.QHBoxLayout() 
        inputLayout.addWidget(QtWidgets.QLabel("ASIN Lookup: "))
        self.textIn2 = QtWidgets.QLineEdit()
        inputLayout.addWidget(self.textIn2)
        asinButton = QtWidgets.QPushButton(">")
        inputLayout.addWidget(asinButton)
        asinButton.clicked.connect(self.gen_wordcloud)
        self.ilabel.setAlignment(QtCore.Qt.AlignCenter)
        
        lookupHeader = QtWidgets.QLabel("Generate a Wordcloud by Review Term Frequency")
        lookupHeader.setAlignment(QtCore.Qt.AlignCenter)    
        lookupHeader.setContentsMargins(0,20,0,10)
        
        layout = QtWidgets.QVBoxLayout() 
        layout.addWidget(lookupHeader)
        layout.addLayout(inputLayout)
        layout.addStretch(1)
        layout.addWidget(self.ilabel)
        layout.setContentsMargins(10,10,10,30)
        self.tab2.setLayout(layout)

    @QtCore.Slot()
    def magic(self):
        self.samples = create_samples('0001844423')
        #print(self.samples)
        self.populate_table()


    def fetch_name(self): 
        self.output.setText(web_scraper(self.textIn.text()))
        self.output.setAlignment(QtCore.Qt.AlignCenter)
    
    def fetch_books(self): 
        print("lol")

    def gen_wordcloud(self): 
        #print(self.textIn2.text())
        word_cloud(self.textIn2.text())
        pixmap = QtGui.QPixmap('word_cloud.png')
        self.ilabel.setPixmap(pixmap)
   # def enter(self,): 
   #     layout = QtWidgets.QFormLayout() 
   #     layout.addRow("Enter ASIN:", QtWidgets.QLineEdit())
    #    self.ilabel = QtWidgets.QLabel(self)
    #    pixmap = QtGui.QPixmap('word_cloud.png')#


       # self.ilabel.setPixmap(pixmap)
       # self.tab2.setLayout(layout)




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())