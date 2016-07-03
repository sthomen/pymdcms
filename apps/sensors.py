# vim:ts=4:sw=4:

import os.path
from threading import Thread
from time import sleep
from datetime import datetime,timedelta
from easysnmp import Session,EasySNMPNoSuchObjectError
import json

from collections import deque,OrderedDict
from graph.line import LineGraph

from applet import Applet

class Sensors(Applet):
	sensors=None

	def __init__(self, config, menus):
		Applet.__init__(self, config, menus)

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
					config.get('sensors', 'oid'),
					polltime=300)

				Sensors.sensors.start()

	def dispatch(self, *args, **kwargs):
		self.metadata={
			'title':'Sensors',
			'css':	'apps/css/sensors.css'
		}

		if len(args)==2 and args[1]=='ajax':
			output=self.ajax_sensors()
		elif len(args)==3 and args[1]=='graph':
			output=self.graph(int(args[2]))
		else:
			output=self.show_sensors()

		return output

	def show_sensors(self):
		graphs=[]
		for i in range(len(self.sensors.data)):
			graphs.append(self.inline_graph(i+1))

		return self.render('display', {'data': self.sensors.data, 'updated': self.sensors.updated, 'graphs': graphs})

	def ajax_sensors(self):
		self.metadata['content-type']='application/json'
		self.metadata['template']='ajax'

		return json.dumps(self.sensors.data)

	def graph(self, index):
		self.metadata['content-type']='image/svg+xml'
		self.metadata['template']='ajax'

		return self.inline_graph(index)

	def inline_graph(self, index):
		data=OrderedDict([(date, value) for date, value in self.sensors.history[index] if date != None])

		graph=LineGraph(self.sensors.updated, max(data.values()) or 100, data=[data], granularity=self.sensors.polltime)
		graph.draw()

		return graph.write()
		
class SnmpSensors(Thread):
	# XXX poor man's MIB
	mib={
		'index':	1,
		'type': 	2,
		'value':	3
	}

	def __init__(self, hostname, community, version, oid, polltime=60, queuesize=10, dateformat='%Y-%m-%d %H:%M:%S'):
		Thread.__init__(self, name="SnmpSensors")

		self.daemon=True

		self.hostname=hostname
		self.community=community
		self.version=version
		self.oid=oid
		self.polltime=polltime
		self.queuesize=queuesize
		self.dateformat=dateformat

		self.updated=None
		self.data={}
		self.history={}

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
			self.store_history()

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

	def store_history(self):
		for index,datum in self.data.items():
			if not int(index) in self.history.keys():
				self.history[int(index)]=deque([(None,None),]*self.queuesize, self.queuesize)

			self.history[int(index)].appendleft((self.updated.strftime(self.dateformat), float(self.data[index].get(self.mib['value']) or 0) / 100),)
