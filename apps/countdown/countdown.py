# vim:set ts=4 sw=4:

import os

import json

from ..applet import Applet
from time import time
from datetime import datetime

class Countdown(Applet):

	dateformat='%Y-%m-%d %H:%M:%S'

	def __init__(self, config, menus):
		Applet.__init__(self, config, menus)
		self.config = config

		self.base_path=os.path.dirname(__file__)
		self.base_url='apps/countdown'

		self.add_template_dir(os.path.join(self.base_path, 'templates'))

	def dispatch(self, method, *args, **kwargs):
		self.metadata={
			'title': 'Countdown to Unix Time form',
			'css':	'/'.join([self.base_url, 'css', 'countdown.css'])
		}

		if 'time' in kwargs:
			# FIXME Absolute URL
			self.redirect('/countdown/{}'.format(kwargs['time']))

		if len(args) > 2 and args[1] == 'ajax':
			return self.ajax_countdown(abs(int(args[2])))

		target=0
		output=''

		if len(args) > 1:
			target=abs(int(args[1]))

		current=int(time())

		if target > current:
			self.metadata.update({
				'title':	'Countdown to Unix Time {}'.format(target),
				'js':		'/'.join([self.base_url, 'js', 'countdown.js'])
			})

			output=self.countdown(target, current)

		output+=self.form(target)

		return output

	def ajax_countdown(self, target):
		current=int(time())

		self.metadata['template']='ajax';

		return json.dumps({'target': target, 'current': current});

	def countdown(self, target, current):
		tgtfmt=datetime.utcfromtimestamp(target)

		remaining=target - current

		return self.render('countdown', {
			'target': target,
			'current': current,
			'remaining': remaining,
			'formatted': tgtfmt.strftime(self.dateformat) + " UTC"
		})

	def form(self, target):
		return self.render('countdown-form', {'target': target})
