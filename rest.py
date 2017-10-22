#!/usr/bin/env python
import web
import json
import busstime

urls = (
    '/route/(.*)', 'get_route'
)

app = web.application(urls, globals())

class get_route:
    def GET(self, route):
		web.header('Access-Control-Allow-Origin', '*')
		return json.dumps(busstime.get_stop_list(route))

if __name__ == "__main__":
    app.run()
