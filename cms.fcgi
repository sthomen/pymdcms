#!/usr/bin/env python
# vim:ts=4:sw=4:

import os
import sys

from ConfigParser import ConfigParser
from flup.server.fcgi import WSGIServer
import cherrypy

from lib.dispatcher import Dispatcher

if __name__ == '__main__':
	config=ConfigParser(allow_no_value=True)
	config.read('cms.conf')

	cp_config={
		'/theme': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(
				os.path.dirname(os.path.realpath(__file__)),
				'theme'
			)
		}
	}

	if sys.stdin.isatty():

		cherrypy.config.update({
			'global': {
				'server.socket_host': '10.0.0.2',
				'server.socket_port': 8001
			}
		})

		cherrypy.quickstart(Dispatcher(config), config=cp_config)
	else:
		app = cherrypy.Application(Dispatcher(), config=config)

		cherrypy.config.update({
			'environment': 'embedded',
			'engine.autoreload.on': False
		})

		WSGIServer(app).run()

