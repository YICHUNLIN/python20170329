# encoding=utf-8

import configparser
import numpy as np
from tkinter import *

class Parssini:

	def __init__(self,inifile):
		self.inifile = inifile

	def calData(self):
		file=configparser.ConfigParser()
		file.read(self.inifile)
		matrixdatatitle = file.options('data')
		dim = int(file['data']['n'])
		matrix = []
		for title in matrixdatatitle:
			dataraw = file['data'][title]
			if title[0] == 'r':
				raw = dataraw.split(',')
				row = []
				for r in raw:
					row.append(int(r))
				matrix.append(row)
		print(matrix)
		npmatrix = np.array(matrix)
		print('show A x A')
		print(np.dot(npmatrix,npmatrix))


class Point:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

class Shape:
	def __init__(self, p1, p2, name):
		self.p1 = p1
		self.p2 = p2
		self.shape = None
		self.name = name

	def draw(self, canvas):
		self.canvas = canvas
		print('shape')

class Line(Shape):
	def __init__(self, p1, p2, name):
		super().__init__(p1, p2, name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)

class Oval(Shape):
	def __init__(self, p1, p2, name):
		super().__init__(p1, p2, name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_oval(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill='red')

class Face(Shape):
	def __init__(self,p1,p2, name):
		super().__init__(p1,p2, name)

	def draw(self, canvas):
		super().draw(canvas)

		centerx = (self.p1.x + self.p2.x) / 2
		centery = self.p2.y - 20

		self.canvas.create_oval(self.p1.x,self.p1.y, self.p2.x,self.p2.y, fill='yellow')
		# l eye
		self.canvas.create_oval(self.p1.x + 15 + 10, self.p1.y+15 + 10,self.p1.x + 35 + 10, self.p1.y+35 + 10,fill='blue')
		# r eye
		self.canvas.create_oval(self.p1.x + 15 + 50, self.p1.y+15+10,self.p1.x + 35 + 50, self.p1.y+35 + 10,fill='blue')
		# m
		self.canvas.create_line(centerx,centery, centerx + 20, centery - 10)
		self.canvas.create_line(centerx,centery, centerx - 20, centery - 10)

class Text(Shape):
	def __init__(self,p1,p2, name):
		super().__init__(p1,p2, name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_text(self.p1.x, self.p1.y, text = self.name,fill='blue')

class Draw:

	def __init__(self, inifile):
		self.inifile = inifile
		self.shapes = []

	def draw(self):
		file = configparser.ConfigParser()
		file.read(self.inifile)
		self.width = int(file['graph']['width'])
		self.height = int(file['graph']['height'])
		self.bg = file['graph']['bg']
		shapeTitle = file.options('graph')

		for title in shapeTitle:
			if ('width' not in title) and  ('height' not in title) and ('bg' not in title):
				shape = file['graph'][title].split(',')
				if 'line' in title:
					line = Line(Point(shape[0], shape[1]),Point(shape[2], shape[3]),title)
					self.shapes.append(line)
				else:
					oval = Oval(Point(shape[0], shape[1]),Point(shape[2], shape[3]),title)
					self.shapes.append(oval)


		self.maxx = 0
		self.maxy = 0
		for shape in self.shapes:
			if shape.p1.x > self.maxx:
				self.maxx = shape.p1.x
			if shape.p2.x > self.maxx:
				self.maxx = shape.p2.x

			if shape.p1.y > self.maxy:
				self.maxy = shape.p1.y
			if shape.p2.y > self.maxy:
				self.maxy = shape.p2.y

		self.root = Tk()
		self.root.geometry("%dx%d" %(self.width,self.height))
		
		self.labelshows = Label(self.root)
		self.labelshows['text'] = "土木工程系"
		self.labelshows.grid(row=0, column = 1)

		self.entryInput = Entry(self.root)
		self.entryInput.grid(row=1,column = 1)

		self.btn1 = Button(self.root)
		self.btn1['text'] = "快點來按我吧"
		self.btn1.grid(row = 2, column = 1)
		self.btn1['command'] = self.e_button

		self.root.mainloop()

	def e_button(self):
		self.labelshows['text'] = self.entryInput.get()
		self.shapes.append(Text(Point(100,100), Point(100,100),self.entryInput.get()))
		self.shapes.append(Face(Point(200,200), Point(300,300),"Face1"))
		self.shapes.append(Face(Point(300,300), Point(400,400),"Face2"))

		self.canvas = Canvas(self.root,bg=self.bg)
		self.canvas.grid(row=3,column=1, rowspan = 5, columnspan = 5)





		self.canvas['width'] = self.maxx + 200
		self.canvas['height'] = self.maxy + 200
		self.root.geometry("%dx%d" %(self.maxx + 200,self.maxy + 300))

		for shape in self.shapes:
			shape.draw(self.canvas)





def main():
	p = Parssini('data.ini')
	p.calData()

	d = Draw('data.ini')
	d.draw()






if __name__ == "__main__":
	main()






