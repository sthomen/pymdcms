#!.ve/bin/python
# vim:ts=4:sw=4:

import os
import sys

from flup.server.fcgi import WSGIServer
import cherrypy

from pymdcms.dispatcher import Dispatcher
from pymdcms.config import Config

if __name__ == '__main__':
	Config('cms.conf')

	cp_config={}

	root=os.path.dirname(os.path.realpath(__file__))

	for name in Config.options('static'):
		cp_config.update({
			name: {
				'tools.staticdir.on': True,
				'tools.staticdir.root': root,
				'tools.staticdir.dir': Config.get('static', name)
			}
		})

	if sys.stdin.isatty():
		cherrypy.config.update({
			'global': {
				'server.socket_host': Config.get('test', 'host'),
				'server.socket_port': int(Config.get('test', 'port'))
			}
		})

		cherrypy.quickstart(Dispatcher(), config=cp_config)
	else:
		# Add script name to work with apache
		# note that the starting slash is important, or cherrypy will
		# replace the script name with 'i' for some reason

		app = cherrypy.Application(Dispatcher(), '/cms.fcgi', config=cp_config)

		cherrypy.config.update({
			'environment': 'embedded',
			'engine.autoreload.on': False
		})

		WSGIServer(app).run()

