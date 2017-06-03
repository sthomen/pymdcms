# vim:ts=4:sw=4:
#
# TODO
#
# - arbitrary time resolution

import sys

from datetime import datetime, timedelta
from math import ceil,floor
import copy
import json

from graph import Graph

class LineGraph(Graph):
	"""
	Amazing graph generator library, generates svg graphs from data of the form
	{
		date: count
		...
	}

	where date is an ascii representation of the date, in self.formats[self.DATE]
	format. Use set_format() before draw() to change.
	"""

	DATE=0
	SECOND=1
	MINUTE=2
	DAY=3
	MONTH=4
	YEAR=5

	PATH=0
	BIG=1
	SMALL=2	
	TINY=3

	def __init__(self, start, max, min=0, width=None, data=[], filename='drawing.svg', granularity=86400):
		"""
		Initialize a new graph

		- start is a datetime object of when you would like to start your graph

		- width and height specify the width and height of the SVG graph, note that
		this is merely the viewport of the graph, it will internally scale lines,
		fonts and dots to fit, so these could really be seen as a how many units
		high you wish to display the graph (max value is a good choice) and then
		width acts as a ratio adjustment of the resulting vector display.

		- filename is only used if you wish to save() the graph.

		- granularity defines the granularity of the graph in seconds
		"""

		if not width:
			width=(ceil(max) - floor(min)) * 4

		super(LineGraph, self).__init__(max, min, width, data, filename)

		# default values
		self.formats={
			self.DATE:	"%Y-%m-%d %H:%M:%S",
			self.SECOND: "%H:%M:%S",
			self.MINUTE: "%H:%M",
			self.DAY:	"%b %d",
			self.MONTH:	"%B",
			self.YEAR:	"%Y"
		}

		# stroke colors
		self.colors=[
			'#abc',
			'#cab',
			'#bca',
			'#cba',
			'#bac',
			'#acb'
		]

		self.widths={
			self.PATH:	1,
			self.BIG:	2,
			self.SMALL:	1,
			self.TINY:	0.5		# self.PATH/2
		}

		# input parameters
		self.granularity=granularity
		self.date_start=start

	def width(self, key, value=None):
		"""
		Get or set the (scaling adjusted) width of the PATH or BIG, SMALL or TINY circle
		"""
		if value:
			self.widths[key]=value

		return self.widths[key]

	def format(self, key, fmt=None):
		"""
		Get or set <key> format to <fmt>.
		"""
		if fmt:
			self.formats[key]=fmt

		return self.formats[key]

	def draw(self):
		"""
		Draw the graph, this method builds the svgwrite object
		"""
		self.grid()

		timestamps=self.drawing.g()
		vertlines=self.drawing.g()

		paths=[]
		graphs=[]

		for i in range(0, len(self.data)):
			paths.append(self.drawing.path(stroke_width=self.widths[self.PATH]*self.scale,
							stroke=self.colors[i], fill_opacity=0, stroke_linejoin='bevel'))

			graphs.append(self.drawing.g())
			graphs[i].update({'id': 'graph-{}'.format(i)})
			graphs[i].add(paths[i])

		pidx=0					# path index
		width=0.1				# stroke width for vertical lines XXX

		for data in self.data:
			delta=len(data.keys())
			tend=self.date_start-timedelta(seconds=delta*self.granularity)
			tdelta=self.date_start-tend

			idx=0				# index used for spacing of the date markers

			for key,value in data.items():
				date=datetime.strptime(key, self.formats[self.DATE])

				# local time delta
				ltdelta=self.date_start-date

				xpos=self.width-(self.width/(tdelta.total_seconds()/ltdelta.total_seconds()))
				ypos=self.max-value

				pointdata=json.dumps({'date': date.isoformat(), 'value': value})

				cur=(xpos, ypos)

				# - if we're showing less than 30 points, draw a circle
				# - if we're showing more than 30 but less than 60 points, draw a dot
				# - if we're showing even more, draw an invisible marker so we can still show instance data

				if delta <= 30:
					circle=self.drawing.circle(center=cur, r=self.widths[self.BIG]*self.scale, fill='#fff',
						stroke_width=0.5*self.scale, stroke=self.colors[pidx])

				elif delta <= 60:
					circle=self.drawing.circle(center=cur, r=self.widths[self.SMALL]*self.scale, fill=self.colors[pidx])

				else:
					circle=self.drawing.circle(center=cur, r=self.widths[self.TINY]*self.scale, fill=self.colors[pidx])

				circle.update({'id': 'circle-{}'.format(idx), 'class': 'datapoint'})
				circle.set_desc(desc=pointdata)
				graphs[pidx].add(circle)

				if idx==0:
					mode='M'
				else:
					mode='L'

				paths[pidx].push(mode)
				paths[pidx].push(list(cur))

				if self.granularity < 60:
					timestamps.add(self.drawing.text(date.strftime(self.formats[self.SECOND]),
						(xpos, self.height+(5*self.scale)), text_anchor='middle', font_size=3*self.scale))
				elif self.granularity < 3600:
					timestamps.add(self.drawing.text(date.strftime(self.formats[self.MINUTE]),
						(xpos, self.height+(5*self.scale)), text_anchor='middle', font_size=3*self.scale))
				elif self.granularity < 86400:
					timestamps.add(self.drawing.text(date.strftime(self.formats[self.DAY]),
						(xpos, self.height+(5*self.scale)), text_anchor='middle', font_size=3*self.scale))
				elif self.granularity < 2592000:
					timestamps.add(self.drawing.text(date.strftime(self.formats[self.MONTH]),
						(xpos, self.height+(5*self.scale)), text_anchor='middle', font_size=3*self.scale))
				elif self.granularity < 31104000:
					timestamps.add(self.drawing.text(date.strftime(self.formats[self.YEAR]),
						(xpos, self.height+(5*self.scale)), text_anchor='middle', font_size=3*self.scale))

				# (hidden) vertical grid lines
				vertlines.add(self.drawing.line((xpos,0),(xpos,self.height), stroke='#ccc', stroke_width=width*self.scale, visibility='hidden', id='line-{}'.format(idx)))

				idx+=1

			pidx+=1

		for i in range(0, len(self.data)):
			self.layers.update({i: graphs[i]})

		self.layers.update({97: vertlines, 98: timestamps})

		self.compose()
