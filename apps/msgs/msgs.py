# vim:ts=4:sw=4:

import os

from ..applet import Applet
from message import MessageList
from datetime import datetime
from ConfigParser import ConfigParser # for NoOptionError

class Msgs(Applet):
	def __init__(self, config, menus):
		Applet.__init__(self, config, menus)
		self.config = config

		self.updated = None
		self.cachetime = 60

		self.base_path=os.path.dirname(__file__)
		self.base_url='apps/msgs'

		self.add_template_dir(os.path.join(self.base_path, 'templates'))

	def dispatch(self, method, *args, **kwargs):
		output=None

		self.load_messagelist()

		self.metadata={}

		if len(args) == 3 and args[1] == 'message':
			output=self.message(int(args[2]))
		else:
			output=self.list()

		return output

	def list(self):
		self.metadata['title']='Messages'

		return self.render('list', { 'list': self.messagelist })

	def message(self, id):
		if self.messagelist.has_message(id):
			message=self.messagelist.get_message(id)

			self.metadata['title']=message.title

			return self.render('message', { 'message': message })

		self.metadata['code']=404

		return self.render('notfound', { 'id': id })

	def load_messagelist(self):
		path=None

		try:
			if self.config.has_section('messages'):
				path=self.config.get('messages', 'path')
		except:
			pass
			
		if self.updated == None or (datetime.now() - self.updated).total_seconds() > self.cachetime:
			self.messagelist=MessageList()
			self.updated=datetime.now()
