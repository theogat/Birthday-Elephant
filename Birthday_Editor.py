#!/usr/bin/python
#-*-coding: utf8-*-

'''   Copyright 2016-2017 Theodoros Gatsios

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''

from PySide import QtGui, QtCore
import sys, os, sqlite3
from donation import donate
from license import webLicense
from datetime import date, datetime

flag = os.path.isfile('birthdays.db')

if (not flag):
	con = sqlite3.connect('birthdays.db', detect_types = sqlite3.PARSE_DECLTYPES)
	
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE Birthdays(Name TEXT, Birthday DATE, Sex TEXT)")	

class main(QtGui.QMainWindow):
	def __init__(self):
		super(main, self).__init__()

		donation = QtGui.QAction(u'Κάνετε δωρεά', self)
		donation.triggered.connect(self.godonate)

		license = QtGui.QAction(u'Άδεια χρήσης', self)
		license.triggered.connect(self.goLicense)
		
		mainMenu=self.menuBar()
		donationmenu=mainMenu.addMenu(u'&Δωρεά')
		donationmenu.addAction(donation)
		aboutMenu = mainMenu.addMenu(u'&Σχετικά')
		aboutMenu.addAction(license)

		self.initUI()

	def initUI(self):
		global window
		window = QtGui.QWidget(self)
		self.setCentralWidget(window)

		upside = QtGui.QFrame(self)
		upside.setFrameShape(QtGui.QFrame.StyledPanel)

		downside = QtGui.QFrame(self)
		downside.setFrameShape(QtGui.QFrame.StyledPanel)

		self.setGeometry(300, 100, 600, 500)
		self.setWindowTitle('Birthday Editor')
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		
		namelbl = QtGui.QLabel(u'Όνοματεπώνυμο:', self)
		name = QtGui.QLineEdit()
		name.setFixedWidth(200)
				
		sexlbl = QtGui.QLabel(u'Φύλο:', self)
		male_button=QtGui.QRadioButton(u"Αρσενικό", self)
		male_button.clicked.connect(self.setmale)
		female_button=QtGui.QRadioButton(u"Θηλυκό", self)
		female_button.clicked.connect(self.setfemale)
		
		datelbl = QtGui.QLabel(u'Ημερομηνία Γέννησης:', self)
		datelbl.setFixedWidth(150)
		date = QtGui.QLineEdit()	
		date.setFixedWidth(200)
		date.setPlaceholderText(u'Έτος/Μήνας/Ημέρα')
		date.setInputMask('9999/99/99')
		date_example = QtGui.QLabel(u'Έτος/Μήνας/Ημέρα (π.χ. 2000/01/28)')

		addbtn = QtGui.QPushButton(u'Προσθήκη', self)
		addbtn.setFixedWidth(150)
		addbtn.clicked.connect(lambda: self.add(name, date, sextxt))
		empty = QtGui.QLabel('', self)

		rembtn = QtGui.QPushButton(u'Αφαίρεση', self)	
		rembtn.clicked.connect(self.remove)	
		
		con = sqlite3.connect('birthdays.db', detect_types=sqlite3.PARSE_DECLTYPES) 

		with con:
			cur = con.cursor()    
			cur.execute("SELECT * FROM Birthdays")
			al = cur.fetchall()
			cur.execute("SELECT Name FROM Birthdays")
			names = cur.fetchall()
			cur.execute("SELECT Sex FROM Birthdays")
			sexes = cur.fetchall()
			cur.execute("SELECT Birthday FROM Birthdays")
			birthdays = cur.fetchall()

		num=0
		for namee in names:
			num=num+1	

		global birthday_table
		birthday_table = QtGui.QTableWidget(num, 3, self)
		birthday_table.resize(500, 500)	
		
		global count
		count = 0
		for nam in al:
			
			n = nam[0].encode('utf8')
			birthday_table.setItem(count, 0, QtGui.QTableWidgetItem("%s" % nam[0]))
			s = nam[2].encode('utf8')
			birthday_table.setItem(count, 2, QtGui.QTableWidgetItem("%s" % nam[2]))
			bd = nam[1].strftime('%Y/%m/%d')
			birthday_table.setItem(count, 1, QtGui.QTableWidgetItem("%s" % bd))
			count = count + 1			
		birthday_table.resizeColumnsToContents()
		birthday_table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(u"Όνομα"))
		birthday_table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem(u"Ημερομηνία Γέννησης"))
		birthday_table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem(u"Φύλο"))
		birthday_table.horizontalHeader().setVisible(True)
		header = birthday_table.horizontalHeader()
		header.setResizeMode(0, QtGui.QHeaderView.Stretch)
		header.setResizeMode(1, QtGui.QHeaderView.Stretch)
		header.setResizeMode(2, QtGui.QHeaderView.Stretch)
		birthday_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		birthday_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

		form = QtGui.QFormLayout()
		form.addRow(namelbl, name)
		form.addRow(sexlbl, male_button)
		form.addRow(empty, female_button)
		form.addRow(datelbl, date)
		form.addRow(empty, date_example)
		form.addRow(empty, addbtn)

		upside.setLayout(form)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(birthday_table)
		vbox.addWidget(rembtn)
		downside.setLayout(vbox)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(upside)
		layout.addWidget(downside)

		window.setLayout(layout)		
		self.setWindowIcon(QtGui.QIcon('logo_editor.png'))
		self.show()

	def godonate(self):
		donate(self)

	def goLicense(self):
		webLicense(self)
		

	def setmale(self):
		global sextxt
		sextxt = u'Αρσενικό'

	def setfemale(self):
		global sextxt
		sextxt = u'Θηλυκό'

	def add(self, name, date, sextxt):
		global count
		count = count + 1
		nametxt = name.text()
		datetxt = date.text()
		dttxt = date.text()
		datetxt = datetime(year=(int(datetxt[0:4])), month=(int(datetxt[5:7])), day=(int(datetxt[8:10])))
		datetxt = datetxt.date()
		
		con = sqlite3.connect('birthdays.db')
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO Birthdays(Name, Birthday, Sex) VALUES(?, ?, ?)", (nametxt, datetxt, sextxt))
		self.initUI()

	def remove(self):
		texts = []
		global birthday_table
		k=0
		for item in birthday_table.selectedItems():
			i = item.row() + 1
			j = item.column()
			text = item.text()
			texts.append(text)
			print i, j, texts[k]
			k=k+1
		
			con = sqlite3.connect('birthdays.db')
			with con:
				cur = con.cursor()
				cur.execute('DELETE FROM Birthdays WHERE Name == ?', (texts[k-1],))
		self.initUI()	

application=QtGui.QApplication(sys.argv)
ui=main()
sys.exit(application.exec_())
