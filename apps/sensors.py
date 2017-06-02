# vim:ts=4:sw=4:

import sys

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
					queuesize=15,
					polltime=1800)

				Sensors.sensors.start()

	def dispatch(self, method, *args, **kwargs):
		self.metadata={
			'title':'Sensors',
			'css':	'apps/css/sensors.css'
		}

		if len(args)==2 and args[1]=='ajax':
			output=self.ajax_sensors()
		elif len(args)==3 and args[1]=='graph':
			output=self.graph(args[2])
		else:
			output=self.show_sensors()

		return output

	def show_sensors(self):
		self.metadata['js']='apps/js/sensors.js'

		return self.render('display', {'data': self.sensors.data, 'updated': self.sensors.updated, 'graphs': self.sensors.graphs})

	def ajax_sensors(self):
		self.metadata['content-type']='application/json'
		self.metadata['template']='ajax'

		return json.dumps(self.sensors.data)

	def graph(self, index):
		self.metadata['content-type']='image/svg+xml'
		self.metadata['template']='ajax'

		return self.sensors.graphs.get(index)
		
class SnmpSensors(Thread):
	# XXX poor man's MIB
	mib={
		'index':	1,
		'type': 	2,
		'value':	3,
		'updated':	4,
		'id':		5
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

		self.graphs={}

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
			self.render_graphs()

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

	def render_graphs(self):
		"""
		This method renders SVG graphs from self.history

		Since self.graphs may be queried at any time, render first and then
		replace
		"""

		graphs={}
		for index in self.data.keys():
			graphs.update({index: self.render_graph(int(index))})

		self.graphs=graphs

	def render_graph(self, index):
		"""
		Render a single graph for self.history[index]
		"""

		data=OrderedDict([(date, value) for date, value in self.history[index] if date != None])

		if data.values():
			big=max(data.values())
			small=min(data.values())

			if small > 0:
				small=0

			if big < 0:
				big=0

		else:
			big=20
			small=0

		graph=LineGraph(self.updated, big, small, data=[data], granularity=self.polltime)
		graph.draw()

		return graph.write()
