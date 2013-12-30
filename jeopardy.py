#!/usr/bin/python

import sys, json
from PyQt4 import QtGui, QtCore, Qt

name = 'ZaPF-Jeopardy (v0.1)'
points_factor = 1

class Jeopardy_Wall(QtGui.QWidget):

	def set_categories(self,categories):
		for i in range(len(categories)):
			self.wall_category_boxes[i].setTitle(categories[i])


	def present_text_answer(self,type,answer):
		if type == 'text':
			self.jeopardy_wall_box.setHidden(True)
			self.answer_box.setHidden(False)
			self.answer_label.setText(answer)


	def clear_answer_section(self,type):
		if type == 'text':
			self.answer_box.setHidden(True)
			self.jeopardy_wall_box.setHidden(False)

	def __init__(self):
		super(Jeopardy_Wall,self).__init__()
		self.grid = QtGui.QGridLayout(self)
		
		jeopardy_wall_layout = QtGui.QHBoxLayout(None)

		self.wall_button = []
		self.wall_category_boxes = []
		self.wall_category_layouts = []

		for i in range(5):
			self.wall_button.append([])
			self.wall_category_layouts.append(QtGui.QVBoxLayout(None))
			self.wall_category_boxes.append(QtGui.QGroupBox(''))
			self.wall_category_boxes[i].setLayout(self.wall_category_layouts[i])
			jeopardy_wall_layout.addWidget(self.wall_category_boxes[i])
			for j in range(5):
				self.wall_button[i].append(QtGui.QPushButton(str((j+1)*points_factor)))
				self.wall_button[i][j].setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
				self.wall_category_layouts[i].addWidget(self.wall_button[i][j])
			
		self.player_wall_layout = QtGui.QHBoxLayout(None)

		self.jeopardy_wall_box = QtGui.QGroupBox('Jeopardy board')
		self.jeopardy_wall_box.setLayout(jeopardy_wall_layout)


		player_wall_box = QtGui.QGroupBox('Player')
		player_wall_box.setLayout(self.player_wall_layout)

		answer_layout = QtGui.QVBoxLayout(None)
		self.answer_label = QtGui.QLabel('')
		self.answer_label.setAlignment(QtCore.Qt.AlignCenter)
		self.answer_label.setMaximumWidth(800)
		answer_layout.addWidget(self.answer_label)
		self.answer_box = QtGui.QGroupBox('Answer')
		self.answer_box.setLayout(answer_layout)
		self.answer_box.setHidden(True)

		self.grid.addWidget(self.answer_box,0,0,8,0)
		self.grid.addWidget(self.jeopardy_wall_box,0,0,8,0)
		self.grid.addWidget(player_wall_box,9,0)


class Jeopardy(QtGui.QWidget):

	class Player:

		def rename(self):
			text, ok = QtGui.QInputDialog.getText(None,'rename '+self.name, 'enter new name:')
			if ok and text != '':
				self.name = text
				self.name_text.setText(self.name)
				self.wall_box.setTitle(self.name)


		def bonus(self):
			bonus_points, ok = QtGui.QInputDialog.getText(None,'bouns points','give '+self.name+' bonus points:')
			if ok and bonus_points != '':
				try:
					self.add_points(int(bonus_points))
				except ValueError:
					message = QtGui.QMessageBox(3,'ValueError','points must be integer!\nnoting will happen')
					message.exec_()

		def add_points(self,points):
			self.points += points
			self.points_text.setText(str(self.points))
			self.wall_points_text.setText(str(self.points))

		def __init__(self,app,name,color,points=0):
			self.app = app
			self.name = name
			self.points = points
			self.color = QtGui.QPalette(QtGui.QColor(color[0],color[1],color[2]))

			layout = QtGui.QGridLayout(None)
			name_label = QtGui.QLabel('Name')
			points_label = QtGui.QLabel('Points')
			self.name_text = QtGui.QLineEdit()
			self.name_text.setText(self.name)
			self.name_text.setReadOnly(True)
			self.points_text = QtGui.QLineEdit()
			self.points_text.setReadOnly(True)
			self.points_text.setText(str(self.points))
			rename_button = QtGui.QPushButton('rename')
			bonus_button = QtGui.QPushButton('bonus')
			
			layout.addWidget(name_label,0,0)
			layout.addWidget(self.name_text,0,1,1,2)
			layout.addWidget(points_label,1,0)
			layout.addWidget(self.points_text,1,1,1,2)
			layout.addWidget(rename_button,2,0)
			layout.addWidget(bonus_button,2,1)
	
			self.box = QtGui.QGroupBox(name)
			self.box.setLayout(layout)
			self.box.setAutoFillBackground(True)
			self.box.setPalette(self.color)

			wall_layout = QtGui.QHBoxLayout(None)
			wall_points_label = QtGui.QLabel('points')
			self.wall_points_text = QtGui.QLineEdit()
			self.wall_points_text.setReadOnly(True)
			self.wall_points_text.setText(str(self.points))
			wall_layout.addWidget(wall_points_label)
			wall_layout.addWidget(self.wall_points_text)

			self.wall_box = QtGui.QGroupBox(name)
			self.wall_box.setLayout(wall_layout)
			self.wall_box.setAutoFillBackground(True)
			self.wall_box.setPalette(self.color)

			self.app.connect(rename_button,Qt.SIGNAL('pressed()'),lambda: self.rename())
			self.app.connect(bonus_button,Qt.SIGNAL('pressed()'),lambda: self.bonus())


	def quit(self):
		message = message = QtGui.QMessageBox(4,'quit Jeoarpardy?','you really think, you might\nbe allowed to quit Jeopardy?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		resp = message.exec_()
		if resp == 16384:
			self.app.quit()


	def select_field(self,category_id,level):
		self.current_field = [category_id,level]
		self.jeopardy_button[category_id][level].setPalette(QtGui.QPalette(QtGui.QColor(255,255,255)))
		self.listen = True
		self.set_field_activity(False)
		self.reopen_button.setEnabled(True)
		if self.game_data[category_id]['level'][level]['type'] == 'text':
			self.wall.present_text_answer(self.game_data[category_id]['level'][level]['type'],self.game_data[category_id]['level'][level]['answer'])
			self.answer_label.setText(self.game_data[category_id]['level'][level]['answer'])
			self.question_label.setText(self.game_data[category_id]['level'][level]['question'])


	def player_pressed(self,player_id):
		if self.listen:
			self.listen = False
			self.set_response(True)
			self.active_player = player_id
			for i in self.player:
				if i != player_id:
					self.player[i].wall_box.setPalette(self.palette())
					self.player[i].box.setPalette(self.palette())


	def reset_player_color(self):
		for i in self.player:
			self.player[i].wall_box.setPalette(self.player[i].color)
			self.player[i].box.setPalette(self.player[i].color)


	def clear_answer_section(self):
		self.reset_player_color()
		if self.game_data[self.current_field[0]]['level'][self.current_field[1]]['type'] == 'text':
			self.answer_label.setText('')
			self.question_label.setText('')
			self.wall.clear_answer_section(self.game_data[self.current_field[0]]['level'][self.current_field[1]]['type'])


	def correct(self):
		self.set_response(False)
		self.set_field_activity(True)
		self.reopen_button.setEnabled(False)
		button = self.jeopardy_button[self.current_field[0]][self.current_field[1]]
		wall_button = self.wall.wall_button[self.current_field[0]][self.current_field[1]]
		player = self.player[self.active_player]
		title = str(button.text())+'\n'+player.name+' [✓]'
		button.setPalette(player.color)
		button.setText(title)
		wall_button.setPalette(player.color)
		wall_button.setText(title)
		player.add_points((self.current_field[1]+1)*points_factor)
		self.clear_answer_section()


	def wrong(self):
		self.set_response(False)
		self.set_field_activity(False)
		self.listen = True
		player = self.player[self.active_player]
		button = self.jeopardy_button[self.current_field[0]][self.current_field[1]]
		title = str(button.text())+'\n'+player.name+' [✗]'
		button.setText(title)
		self.wall.wall_button[self.current_field[0]][self.current_field[1]].setText(title)
		player.add_points((self.current_field[1]+1)*points_factor*-1)


	def reopen(self):
		if self.listen:
			self.set_response(False)
			self.set_field_activity(True)
			self.reopen_button.setEnabled(False)
			self.clear_answer_section()
		else:
			self.reset_player_color()
			self.listen = True
			self.set_response(False)


	def set_response(self,a):
		self.correct_button.setEnabled(a)
		self.wrong_button.setEnabled(a)


	def set_field_activity(self,a):
		for i in self.jeopardy_button:
			for j in i:
				j.setEnabled(a)


	def __init__(self,app,game_file):
		super(Jeopardy,self).__init__()
		print(name)
		self.app = app

		game_str = ''
		with open(game_file,'r') as file:
			game_str = file.read()
		self.game_data = json.loads(game_str)

		jeopardy_categories = []
		for i in self.game_data:
			jeopardy_categories.append(i['category'])

		self.grid = QtGui.QGridLayout(self)

		# Create the Jeopardy window
		jeopardy_window = QtGui.QHBoxLayout(None)
		jeopardy_board_box = QtGui.QGroupBox('Jeopardy board')
		jeopardy_board_box.setLayout(jeopardy_window)
		jeopardy_category_layouts = []
		self.jeopardy_category_boxes = []

		# Create the Jeopardy buttons
		self.jeopardy_button = []
		for i in range(5):
			jeopardy_category_layouts.append(QtGui.QVBoxLayout(None))
			self.jeopardy_category_boxes.append(QtGui.QGroupBox(jeopardy_categories[i]))
			self.jeopardy_button.append([])
			for j in range(5):
				self.jeopardy_button[i].append(QtGui.QPushButton(str((j+1)*points_factor)))
				self.jeopardy_button[i][j].setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
				jeopardy_category_layouts[i].addWidget(self.jeopardy_button[i][j])
				self.app.connect(self.jeopardy_button[i][j],Qt.SIGNAL('pressed()'),lambda i=[i,j]: self.select_field(i[0],i[1]))
			#jeopardy_category_layouts[i].addWidget(self.jeopardy_category_boxes[i])
			self.jeopardy_category_boxes[i].setLayout(jeopardy_category_layouts[i])
			jeopardy_window.addWidget(self.jeopardy_category_boxes[i])

		# Create the Answer section
		self.answer_label = QtGui.QLabel('')
		self.answer_label.setAlignment(QtCore.Qt.AlignCenter)
		answer_layout = QtGui.QHBoxLayout(None)
		answer_layout.addWidget(self.answer_label)
		answer_box = QtGui.QGroupBox('presented answer')
		answer_box.setLayout(answer_layout)

		self.question_label = QtGui.QLabel('')
		self.question_label.setAlignment(QtCore.Qt.AlignCenter)
		question_layout = QtGui.QHBoxLayout(None)
		question_layout.addWidget(self.question_label)
		question_box = QtGui.QGroupBox('suggested question')
		question_box.setLayout(question_layout)

		answer_section_layout = QtGui.QVBoxLayout(None)
		answer_section_layout.addWidget(answer_box)
		answer_section_layout.addWidget(question_box)

		# Create the Repsonse section
		response_section_layout = QtGui.QVBoxLayout(None)
		self.correct_button = QtGui.QPushButton('CORRECT')
		self.correct_button.setPalette(QtGui.QPalette(QtGui.QColor(0,255,0)))
		self.wrong_button = QtGui.QPushButton('WRONG')
		self.wrong_button.setPalette(QtGui.QPalette(QtGui.QColor(255,0,0)))
		self.reopen_button = QtGui.QPushButton('REOPEN')
		self.set_response(False)
		self.reopen_button.setEnabled(False)

		response_section_layout.addWidget(self.correct_button)
		response_section_layout.addWidget(self.wrong_button)
		response_section_layout.addWidget(self.reopen_button)

		# Create the Player section
		player_section_layout = QtGui.QVBoxLayout(None)
		player_box = QtGui.QGroupBox('Player')
		player_box.setLayout(player_section_layout)

		self.player = {}
		self.player['p1'] = self.Player(self.app,'Player 1',[0,0,255])
		self.player['p2'] = self.Player(self.app,'Player 2',[255,0,0])
		self.player['p3'] = self.Player(self.app,'Player 3',[0,255,0])
		self.player['p4'] = self.Player(self.app,'Player 4',[255,255,0])

		player_section_layout.addWidget(self.player['p1'].box)
		player_section_layout.addWidget(self.player['p2'].box)
		player_section_layout.addWidget(self.player['p3'].box)
		player_section_layout.addWidget(self.player['p4'].box)

		# Create the Global Butten section
		global_button_layout = QtGui.QVBoxLayout(None)

		quit = QtGui.QPushButton('quit')
		global_button_layout.addWidget(quit)

		# Add everything to the grid
		self.grid.addWidget(jeopardy_board_box,0,0,4,4)
		self.grid.addLayout(answer_section_layout,5,1,1,3)
		self.grid.addWidget(player_box,0,5,4,1)
		self.grid.addLayout(global_button_layout,5,5)
		self.grid.addLayout(response_section_layout,5,0)

		# Create the KeyActions
		self.listen = False
		player_1_key_event = QtGui.QShortcut(QtGui.QKeySequence('1'),self)
		player_2_key_event = QtGui.QShortcut(QtGui.QKeySequence('2'),self)
		player_3_key_event = QtGui.QShortcut(QtGui.QKeySequence('3'),self)
		player_4_key_event = QtGui.QShortcut(QtGui.QKeySequence('4'),self)

		# Connecitong stuff to functions
		self.app.connect(quit,Qt.SIGNAL('pressed()'),lambda: self.quit())
		self.app.connect(self.correct_button,Qt.SIGNAL('pressed()'),lambda: self.correct())
		self.app.connect(self.wrong_button,Qt.SIGNAL('pressed()'),lambda: self.wrong())
		self.app.connect(self.reopen_button,Qt.SIGNAL('pressed()'),lambda: self.reopen())

		self.app.connect(player_1_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p1'))
		self.app.connect(player_2_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p2'))
		self.app.connect(player_3_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p3'))
		self.app.connect(player_4_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p4'))

		self.setLayout(self.grid)
		self.setWindowTitle(name)

		self.wall = Jeopardy_Wall()
		self.wall.set_categories(jeopardy_categories)

		self.wall.player_wall_layout.addWidget(self.player['p1'].wall_box)
		self.wall.player_wall_layout.addWidget(self.player['p2'].wall_box)
		self.wall.player_wall_layout.addWidget(self.player['p3'].wall_box)
		self.wall.player_wall_layout.addWidget(self.player['p4'].wall_box)

		self.show()
#		self.showMaximized()
		self.wall.show()


def main():
	app = QtGui.QApplication(sys.argv)
	if len(sys.argv) == 2:
		jeopardy = Jeopardy(app,sys.argv[1])
		sys.exit(app.exec_())


if __name__ == '__main__':
	main()
