# vim:ts=4:sw=4:

import os
import re
from email.parser import Parser
from datetime import datetime

class MessageList(object):
	def __init__(self, path=None):
		if not path:
			self.path='/var/msgs'

		self.load()

	def load(self):
		self.load_bounds()

		self.messages={}

		for index in range(self.bounds.get('lower'), self.bounds.get('upper')+1):
			path=os.path.join(self.path, str(index))

			if os.path.exists(path):
				self.messages[index]=Message(path)

	def load_bounds(self):
		lower = 0
		upper = 0

		with open(os.path.join(self.path, 'bounds')) as fp:
			lower, upper = fp.read().rstrip().split(' ')

		self.bounds={
			'lower': int(lower),
			'upper': int(upper)
		}

	def items(self):
		return self.messages.items()

	def has_message(self, id):
		return self.messages.has_key(id)

	def get_message(self, id):
		return self.messages.get(id)

class Message(object):
	def __init__(self, path):
		self.parse(path)
		
	def parse(self, path):
		with open(path) as fp:
			self.email=Parser().parse(fp)

		self.date = self.email.get('Date', '')
		self.title = self.email.get('Subject', '')
		self.message = self.reformat(self.email.get_payload())


	# TODO inelegant, rewrite me
	def reformat(self, raw):
		output=[]

		lines = raw.splitlines()

		line=''

		for row in lines:
			line=' '.join([line, re.sub('- *$', '', row)])

			if row == '':
				output.append(line)
				line=''

		output.append(line)

		return output

