# vim:ts=4:sw=4:

from StringIO import StringIO
from math import ceil,floor

import svgwrite

class Graph(object):
	def __init__(self, max, min, width, data, filename):
		self.data=data
		self.max=int(max)
		self.min=int(min)
		self.height=self.max-self.min
		self.width=width

		self.drawing=svgwrite.Drawing(filename, profile='tiny')

		self.scale=self.width/200.0

		self.border(10)

		self.layers={}

	def add_data(self, data):
		self.data.append(data)

	def border(self, width=None):
		"""
		Get or set (scaling adjusted) border width (10 is a good number)
		"""
		if width:
			self._border=width
			self.translate_x=self._border/2
			self.translate_y=self._border/2

		return self._border

	def grid(self):
		grid=self.drawing.g()
		gridnumbers=self.drawing.g()

		# FIXME There should be some clever math to make this a single line, but I don't know it
		if self.height < 10:
			gridstep=1
		elif self.height < 50:
			gridstep=5 
		elif self.height < 100:
			gridstep=10
		elif self.height < 500:
			gridstep=50
		elif self.height < 1000:
			gridstep=100
		else:
			gridstep=500

		positive=range(0, self.max+1, gridstep)
		negative=[-x for x in range(0, -(self.min-1), gridstep)]
		
		# horizontal grid lines
		for y in list(set(positive + negative)):
			color='#ccc'
			width=0.1

			if y == 0:
				color='#000'
				width=0.3

			ypos=self.height-(y-self.min)

			texty=ypos+(3*self.scale)
			no=self.drawing.text(str(y), (0,texty), font_size=3*self.scale)
			glow=self.drawing.text(str(y), (0,texty), font_size=3*self.scale, stroke_width=0.5*self.scale, stroke='#fff')
			gridnumbers.add(glow)
			gridnumbers.add(no)

			grid.add(self.drawing.line((0,ypos),(self.width,ypos), stroke=color, stroke_width=width*self.scale))

		self.layers.update({-1: grid, 99: gridnumbers})

	def compose(self):
		graph=self.drawing.g()

		for layer in sorted(self.layers.items()):
			graph.add(layer[1])

		graph.translate(self.translate_x*self.scale, self.translate_y*self.scale)
		self.drawing.viewbox(width=self.width+(self._border*self.scale), height=self.height+(self._border*self.scale))

		self.drawing.add(graph)

	def save(self):
		"""
		Save svgwrite object to the filename set in __init__()
		"""
		self.drawing.save()

	def write(self):
		"""
		Returns the rendered svg file in a string
		"""
		svg=StringIO()
		self.drawing.write(svg)
		svg.seek(0)
		return svg.read()
