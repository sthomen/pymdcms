# vim:ts=4:sw=4:

import sys

from threading import Thread
from time import sleep
from datetime import datetime,timedelta
from easysnmp import Session,EasySNMPNoSuchObjectError

from collections import deque,OrderedDict

from graph.line import LineGraph

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
			if not index in self.history.keys():
				self.history[index]=deque([(None,None),]*self.queuesize, self.queuesize)

			self.history[index].appendleft((self.updated.strftime(self.dateformat), float(self.data[index].get(self.mib['value']) or 0) / 100),)

	def render_graphs(self):
		"""
		This method renders SVG graphs from self.history

		Since self.graphs may be queried at any time, render first and then
		replace
		"""

		graphs={}
		for index in self.data.keys():
			graphs.update({index: self.render_graph(index)})

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
