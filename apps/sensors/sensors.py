# vim:ts=4:sw=4:

import sys

import os.path
import json

from ..applet import Applet
from snmpsensors import SnmpSensors

class Sensors(Applet):
	sensors=None

	def __init__(self, config, menus):
		Applet.__init__(self, config, menus)

		self.base_path=os.path.dirname(__file__)
		self.base_url='apps/sensors'

		self.add_template_dir(os.path.join(self.base_path, 'templates'))

		# load sensor aliases from config
		self.load_aliases()

		# XXX
		# Reference class variable here to keep only one update thread per application.
		# There may well be multiple query threads however, since the wsgi app may be
		# launched multiple times by the hosting server if it decides it's not responding
		# quickly enough.
		# Fixing this would require more work than I feel like doing, so for now let's
		# settle with this approach.

		if not Sensors.sensors:
			config_ok=True

			for key in ('hostname', 'community', 'version', 'oid'):
				if not config.has_option('sensors', key):
					config_ok=False

			if config_ok:
				Sensors.sensors=SnmpSensors(config.get('sensors', 'hostname'),
					config.get('sensors', 'community'),
					config.get('sensors', 'version'),
					config.get('sensors', 'oid'),
					queuesize=15,
					polltime=1800)

				Sensors.sensors.start()

	def dispatch(self, method, *args, **kwargs):
		self.metadata={
			'title':'Sensors',
			'css':	'/'.join([self.base_url, 'css', 'sensors.css'])
		}

		if len(args)==2 and args[1]=='ajax':
			output=self.ajax_sensors()
		elif len(args)==3 and args[1]=='graph':
			output=self.graph(args[2])
		else:
			output=self.show_sensors()

		return output

	def show_sensors(self):
		self.metadata['js']='/'.join([self.base_url, 'js', 'sensors.js'])

		return self.render('display', {'history': self.sensors.history, 'updated': self.sensors.updated, 'graphs': self.sensors.graphs, 'aliases': self.aliases})

	def ajax_sensors(self):
		self.metadata['content-type']='application/json'
		self.metadata['template']='ajax'

		return json.dumps(self.sensors.data)

	def graph(self, datatype):
		self.metadata['content-type']='image/svg+xml'
		self.metadata['template']='ajax'

		return self.sensors.graphs.get(datatype)

	def load_aliases(self):
		self.aliases={}

		if not self.config.has_section('sensor aliases'):
			return

		self.aliases=dict(self.config.items('sensor aliases'))
