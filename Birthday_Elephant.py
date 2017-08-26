#!/usr/bin/python
#-*-coding: utf8-*-

'''   Copyright 2016 Theodoros Gatsios

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
from datetime import datetime, date

flag=os.path.isfile('birthdays.db')
if flag:
	year = datetime.now().year
	month = datetime.now().month
	day = datetime.now().day
	b=[]
	s=[]
	counter=0
	i=0
	b_name=u''
	s_sex=u''
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
	
	for birthday in birthdays:
		if birthday[0].day==day and birthday[0].month==month:
			counter+=1
			b_flag=True
			if counter>1:
				b.append(names[i][0].encode('utf8'))
				s.append(sexes[i][0].encode('utf8'))	
			else:
				b_name = names[i][0].encode('utf8')
				s_sex = sexes[i][0].encode('utf8')
				b.append(names[i][0].encode('utf8'))
				s.append(sexes[i][0].encode('utf8'))
		else:
			pass
		i+=1

	if counter!=0:
		pass
	else:
		sys.exit()
else:
	con = sqlite3.connect('birthdays.db', detect_types = sqlite3.PARSE_DECLTYPES)
	with con:
		cur = con.cursor()
		cur.execute('CREATE TABLE Birthdays(Name TEXT, Birthday DATE, Sex TEXT)')

class main(QtGui.QMainWindow):
	def __init__(self):
		super(main, self).__init__()
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
		#self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		
		#Screen Resolution
		screen_resolution = app.desktop().screenGeometry()
		width = screen_resolution.width()
		height =  screen_resolution.height()
		self.setGeometry(width, height, 300, 100)

		#Background Colour
		p = QtGui.QPalette()
		gradient = QtGui.QLinearGradient(0, 0, 0, 100)
		gradient.setColorAt(0.0, QtGui.QColor(100, 100, 100))
		gradient.setColorAt(0.5, QtGui.QColor(0, 0, 0))
		gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
		p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
		self.setPalette(p)


		#Logo
		logo=QtGui.QPixmap('logo.png')
		logo_lbl=QtGui.QLabel(self)
		logo_lbl.setGeometry(QtCore.QRect(0, 0, 100, 100))
		logo_lbl.setMaximumSize(100,100)
		logo_lbl.setPixmap(logo) 

		#Database Interaction
		

		#Layout Initialization
		layout=QtGui.QVBoxLayout()

		
		#Label Customizing
		if counter>4:
			label=QtGui.QLabel(u'Σήμερα έχουν πάρα πολλοί\nγενέθλια!\n\nΔυστυχώς δεν έχω αρκετό \nχώρο να στους πω.', self)	
			label.setStyleSheet("QLabel { border-style: outset; border-width: 2px; border-color: red; color : white; }")
			logofont = QtGui.QFont("Ubuntu", 10)
			label.setFont(logofont)
			label.setGeometry(100, 0, 200, 100)
		else:
			if counter>1:
				label=QtGui.QLabel(u'Σήμερα έχουν γενέθλια οι: \n', self)
			elif counter==1:
				if s_sex==u'Αρσενικό'.encode('utf8'):
					arthro=u'ο'
				elif s_sex==u'Θηλυκό'.encode('utf8'):
					arthro=u'η'
				else:
					print 'code error'
				label=QtGui.QLabel(u'Σήμερα έχει γενέθλια %s \n' % (arthro), self)
			else:
				print 'code error counter'
			label.setStyleSheet("QLabel { color : white; }")
			logofont = QtGui.QFont("Ubuntu", 10)
			label.setFont(logofont)
			label.setGeometry(110, 0, 160, 70)
			
			e=[]
			w=1
			for names in b:
				if w<counter:			
					names_label=QtGui.QLabel(u'%s,\n' % (names.decode('utf8')), self)
				else:
					names_label=QtGui.QLabel(u'%s!\n' % (names.decode('utf8')), self)
				names_label.setStyleSheet("QLabel { color : white; }")
				names_label.setFont(logofont)
				e.append(names_label)
				w+=1
			q=0
			for n in e:
				if q<=counter:
					n.setGeometry(110, (q+1)*15, 180, 70)
				q+=1

		#Layout
			for name_label in e:
				layout.addWidget(name_label)


		layout.addWidget(label)
		self.setLayout(layout)

		#Timer 30sec
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.end)
		self.timer.start(30000)		

		#self.setStyleSheet("QWidget { border-style: outset; border-width: 2px; border-color: beige; }")
		self.show()

	def end(self):
		sys.exit()

app=QtGui.QApplication(sys.argv)
gui=main()
sys.exit(app.exec_())
