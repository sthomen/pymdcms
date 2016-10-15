#!/usr/bin/env python
# vim:ts=4:sw=4:

import os
import sys

from ConfigParser import ConfigParser
from flup.server.fcgi import WSGIServer
import cherrypy

from lib.dispatcher import Dispatcher

if __name__ == '__main__':
	config=ConfigParser()
	config.read('cms.conf')

	cp_config={}

	root=os.path.dirname(os.path.realpath(__file__))

	for name in config.options('static'):
		cp_config.update({
			name: {
				'tools.staticdir.on': True,
				'tools.staticdir.root': root,
				'tools.staticdir.dir': config.get('static', name)
			}
		})

	if sys.stdin.isatty():
		cherrypy.config.update({
			'global': {
				'server.socket_host': config.get('test', 'host'),
				'server.socket_port': int(config.get('test', 'port'))
			}
		})

		cherrypy.quickstart(Dispatcher(config), config=cp_config)
	else:
		app = cherrypy.Application(Dispatcher(config), config=cp_config)

		cherrypy.config.update({
			'environment': 'embedded',
			'engine.autoreload.on': False
		})

		WSGIServer(app).run()

