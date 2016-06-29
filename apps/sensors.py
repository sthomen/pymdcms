# vim:ts=4:sw=4:

import os.path
from threading import Thread
from time import sleep
from datetime import datetime
from easysnmp import Session,EasySNMPNoSuchObjectError
import json

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
			if config.has_option('sensors', 'hostname') and config.has_option('sensors', 'community') and config.has_option('sensors', 'version') and config.has_option('sensors', 'oid'):

				Sensors.sensors=SnmpSensors(config.get('sensors', 'hostname'),
					config.get('sensors', 'community'),
					config.get('sensors', 'version'),
					config.get('sensors', 'oid'))

				Sensors.sensors.start()

	def dispatch(self, *args, **kwargs):
		if len(args)>1 and args[1]=='ajax':
			return self.ajax_sensors()
		else:
			return self.show_sensors()

	def show_sensors(self):
		# because the ajax code below manipulates the object metadata
		if 'content-type' in self.metadata:
			del self.metadata['content-type']

		if 'template' in self.metadata:
			del self.metadata['template']

		return self.render('display', {'data': self.sensors.data, 'updated': self.sensors.updated})

	def ajax_sensors(self):
		self.metadata['content-type']='application/json'
		self.metadata['template']='ajax'

		return json.dumps(self.sensors.data)
		
class SnmpSensors(Thread):
	def __init__(self, hostname, community, version, oid, polltime=60):
		Thread.__init__(self, name="SnmpSensors")

		self.daemon=True

		self.hostname=hostname
		self.community=community
		self.version=version
		self.oid=oid
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
		if self.oid:
			session=Session(hostname=self.hostname, community=self.community, version=int(self.version))
			self.data=self.flip_snmp_data(session.walk(self.oid))
			self.updated=datetime.now()

	def flip_snmp_data(self, data):
		"""
		This method takes the data returned from the walk method (easysnmp.SNMPValue) and
		changes it from a bare list to a nested directory:
		{
			index: {
				module: value
				...
			}
		}
		"""

		result={}

		for sv in data:
			oid=sv.oid.split('.')
			value=sv.value

			key,index=oid[-2:]

			if not index in result.keys():
				result[index]={}

			result[index]['oid']='.'.join(oid)
			result[index][int(key)]=value

		return result
