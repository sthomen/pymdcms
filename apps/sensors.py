# vim:ts=4:sw=4:

import os.path
from threading import Thread
from time import sleep
from datetime import datetime
from easysnmp import Session,EasySNMPNoSuchObjectError

from applet import Applet

class Sensors(Applet):
	sensors=None

	def __init__(self, config, menus):
		Applet.__init__(self, config, menus)

		self.metadata={
			'title':'Sensors',
			'css':	'apps/css/sensors.css'
		}

		self.add_template_dir(os.path.join(os.path.dirname(__file__), 'templates', 'sensors'))

		# XXX
		# Reference class variable here to keep only one update thread per application.
		# There may well be multiple query threads however, since the wsgi app may be
		# launched multiple times by the hosting server if it decides it's not responding
		# quickly enough.
		# Fixing this would require more work than I feel like doing, so for now let's
		# settle with this approach.

		if not Sensors.sensors:
			if config.has_option('sensors', 'hostname') and config.has_option('sensors', 'community') and config.has_option('sensors', 'version') and config.has_option('sensors', 'mib'):

				Sensors.sensors=SnmpSensors(config.get('sensors', 'hostname'),
					config.get('sensors', 'community'),
					config.get('sensors', 'version'),
					config.get('sensors', 'mib'))

				Sensors.sensors.start()

	def dispatch(self, *args, **kwargs):
		if len(args)>1 and args[1]=='ajax':
			return self.ajax_sensors()
		else:
			return self.show_sensors()

	def show_sensors(self):

		return self.render('display', {'data': self.sensors.data, 'updated': self.sensors.updated})

	def ajax_sensors(self):
		self.metadata['template']='ajax'

		return self.sensors.data
		
class SnmpSensors(Thread):
	def __init__(self, hostname, community, version, mib, polltime=60):
		Thread.__init__(self, name="SnmpSensors")

		self.daemon=True

		self.hostname=hostname
		self.community=community
		self.version=version
		self.mib=mib
		self.polltime=polltime

		self.updated=None
		self.data={}

		self.done=False

	def run(self):
		while not self.done:
			self.query_sensors()
			self.idle()

	def terminate(self):
		self.done=True

	def idle(self):
		for _ in range(self.polltime):
			sleep(1)
			if self.done:
				break

	def query_sensors(self):
		if self.mib:
			session=Session(hostname=self.hostname, community=self.community, version=int(self.version))
			self.data=session.walk(self.mib)
			self.updated=datetime.now()
